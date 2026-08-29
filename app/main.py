import os
from pathlib import Path
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.core.seed_data import seed_database
from app.api import (
    auth_router,
    categories_router,
    products_router,
    cart_router,
    checkout_router,
    profile_router,
    favorites_router,
    admin_stats_router,
    admin_products_router,
    admin_categories_router,
    admin_orders_router,
    admin_users_router,
    admin_uploads_router
)

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

from fastapi.staticfiles import StaticFiles

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional Static files mount for local dev
try:
    if settings.STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")
    elif settings.PUBLIC_DIR.exists() and (settings.PUBLIC_DIR / "static").exists():
        app.mount("/static", StaticFiles(directory=str(settings.PUBLIC_DIR / "static")), name="static")
except Exception:
    pass

def get_template_html(filename: str) -> str:
    template_path = settings.TEMPLATES_DIR / filename
    if template_path.is_file():
        return template_path.read_text(encoding="utf-8")
    public_path = settings.PUBLIC_DIR / filename
    if public_path.is_file():
        return public_path.read_text(encoding="utf-8")
    return f"<!DOCTYPE html><html><body><h1>{filename} not found</h1></body></html>"

# Include API Routers
app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(checkout_router)
app.include_router(profile_router)
app.include_router(favorites_router)
app.include_router(admin_stats_router)
app.include_router(admin_products_router)
app.include_router(admin_categories_router)
app.include_router(admin_orders_router)
app.include_router(admin_users_router)
app.include_router(admin_uploads_router)

# Auto-initialize database tables and seed data
def ensure_db_initialized():
    if settings.AUTO_CREATE_TABLES:
        try:
            Base.metadata.create_all(bind=engine)
            db = SessionLocal()
            try:
                from app.models.category import Category
                if db.query(Category).count() == 0:
                    seed_database(db)
            finally:
                db.close()
        except Exception as e:
            print(f"[DB Init Warning] Initialization note: {e}")

# Run once on module import
ensure_db_initialized()

@app.on_event("startup")
def startup_event():
    ensure_db_initialized()

# HTML Pages Routes
@app.get("/", response_class=HTMLResponse)
def page_home():
    return HTMLResponse(content=get_template_html("index.html"))

@app.get("/catalog", response_class=HTMLResponse)
def page_catalog():
    return HTMLResponse(content=get_template_html("catalog.html"))

@app.get("/product/{slug}", response_class=HTMLResponse)
def page_product(slug: str):
    return HTMLResponse(content=get_template_html("product.html"))

@app.get("/cart", response_class=HTMLResponse)
def page_cart():
    return HTMLResponse(content=get_template_html("cart.html"))

@app.get("/checkout", response_class=HTMLResponse)
def page_checkout():
    return HTMLResponse(content=get_template_html("checkout.html"))

@app.get("/order-success", response_class=HTMLResponse)
def page_order_success():
    return HTMLResponse(content=get_template_html("order-success.html"))

@app.get("/profile", response_class=HTMLResponse)
def page_profile():
    return HTMLResponse(content=get_template_html("profile.html"))

@app.get("/login", response_class=HTMLResponse)
def page_login():
    return HTMLResponse(content=get_template_html("login.html"))

@app.get("/admin", response_class=HTMLResponse)
def page_admin():
    return HTMLResponse(content=get_template_html("admin.html"))

# SEO Routes
@app.get("/robots.txt", response_class=PlainTextResponse)
def get_robots_txt():
    robots_path = settings.TEMPLATES_DIR / "robots.txt"
    if robots_path.is_file():
        content = robots_path.read_text(encoding="utf-8")
        return PlainTextResponse(content.replace("http://localhost:8000", settings.SITE_URL))
    return PlainTextResponse(f"User-agent: *\nAllow: /\nDisallow: /admin\nDisallow: /profile\nDisallow: /checkout\nSitemap: {settings.SITE_URL}/sitemap.xml")

@app.get("/sitemap.xml", response_class=Response)
def get_sitemap_xml():
    sitemap_path = settings.TEMPLATES_DIR / "sitemap.xml"
    if sitemap_path.is_file():
        content = sitemap_path.read_text(encoding="utf-8")
        return Response(content=content.replace("http://localhost:8000", settings.SITE_URL), media_type="application/xml")
    return Response(content=f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>{settings.SITE_URL}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>
    <url><loc>{settings.SITE_URL}/catalog</loc><changefreq>daily</changefreq><priority>0.9</priority></url>
</urlset>""", media_type="application/xml")

# Catch-all: proxy static assets to Cloudflare Workers Static Assets binding when running in Worker
@app.get("/{path:path}", include_in_schema=False)
async def static_asset_proxy(path: str, request: Request):
    env = request.scope.get("env")
    if env and hasattr(env, "ASSETS"):
        asset_url = f"https://assets.local/{path}"
        resp = await env.ASSETS.fetch(asset_url)
        body = await resp.bytes()
        headers = dict(resp.headers)
        return Response(content=body, status_code=resp.status, headers=headers)

    static_file = settings.STATIC_DIR / path
    if static_file.is_file():
        return FileResponse(str(static_file))
    
    pub_static = settings.PUBLIC_DIR / path
    if pub_static.is_file():
        return FileResponse(str(pub_static))

    raise HTTPException(status_code=404, detail="Not Found")

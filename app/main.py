import os
from pathlib import Path
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

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

# Startup event: create tables and seed DB
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

# HTML Pages Routes
@app.get("/", response_class=HTMLResponse)
def page_home():
    path = settings.TEMPLATES_DIR / "index.html"
    return HTMLResponse(content=path.read_text(encoding="utf-8"))

@app.get("/catalog", response_class=HTMLResponse)
def page_catalog():
    path = settings.TEMPLATES_DIR / "catalog.html"
    return HTMLResponse(content=path.read_text(encoding="utf-8"))

@app.get("/product/{slug}", response_class=HTMLResponse)
def page_product(slug: str):
    path = settings.TEMPLATES_DIR / "product.html"
    return HTMLResponse(content=path.read_text(encoding="utf-8"))

@app.get("/cart", response_class=HTMLResponse)
def page_cart():
    path = settings.TEMPLATES_DIR / "cart.html"
    return HTMLResponse(content=path.read_text(encoding="utf-8"))

@app.get("/checkout", response_class=HTMLResponse)
def page_checkout():
    path = settings.TEMPLATES_DIR / "checkout.html"
    return HTMLResponse(content=path.read_text(encoding="utf-8"))

@app.get("/order-success", response_class=HTMLResponse)
def page_order_success():
    path = settings.TEMPLATES_DIR / "order-success.html"
    return HTMLResponse(content=path.read_text(encoding="utf-8"))

@app.get("/profile", response_class=HTMLResponse)
def page_profile():
    path = settings.TEMPLATES_DIR / "profile.html"
    return HTMLResponse(content=path.read_text(encoding="utf-8"))

@app.get("/login", response_class=HTMLResponse)
def page_login():
    path = settings.TEMPLATES_DIR / "login.html"
    return HTMLResponse(content=path.read_text(encoding="utf-8"))

@app.get("/admin", response_class=HTMLResponse)
def page_admin():
    path = settings.TEMPLATES_DIR / "admin.html"
    return HTMLResponse(content=path.read_text(encoding="utf-8"))

# SEO Routes
@app.get("/robots.txt", response_class=PlainTextResponse)
def get_robots_txt():
    robots_path = settings.TEMPLATES_DIR / "robots.txt"
    if robots_path.exists():
        return PlainTextResponse(robots_path.read_text(encoding="utf-8"))
    return PlainTextResponse("User-agent: *\nAllow: /\nDisallow: /admin\nDisallow: /profile\nDisallow: /checkout\nSitemap: http://localhost:8000/sitemap.xml")

@app.get("/sitemap.xml", response_class=Response)
def get_sitemap_xml():
    sitemap_path = settings.TEMPLATES_DIR / "sitemap.xml"
    if sitemap_path.exists():
        return Response(content=sitemap_path.read_text(encoding="utf-8"), media_type="application/xml")
    return Response(content="""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>http://localhost:8000/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>
    <url><loc>http://localhost:8000/catalog</loc><changefreq>daily</changefreq><priority>0.9</priority></url>
</urlset>""", media_type="application/xml")

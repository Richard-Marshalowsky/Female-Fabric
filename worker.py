from app.main import app
from workers import asgi

# Cloudflare Python Workers ASGI Entrypoint for FastAPI
Default = asgi.entrypoint(app)

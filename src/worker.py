import sys
from pathlib import Path

# Ensure root directory and src directory are in sys.path
root_dir = Path(__file__).resolve().parent.parent
src_dir = Path(__file__).resolve().parent

if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from app.main import app
from workers import asgi

# Cloudflare Python Workers ASGI Entrypoint for FastAPI
Default = asgi.entrypoint(app)

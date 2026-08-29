import sys
from pathlib import Path

# Add project root to sys.path so 'app' is always resolvable on Vercel
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.main import app, ensure_db_initialized

# Ensure tables & seed data are created on cold start
ensure_db_initialized()

# Export both app and handler for maximum Vercel compatibility
handler = app

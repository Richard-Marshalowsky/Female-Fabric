import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IS_VERCEL = bool(os.getenv('VERCEL'))
IS_WORKER = bool(os.getenv('CF_WORKER') or os.getenv('CF_PAGES'))

if IS_VERCEL or IS_WORKER:
    TMP_DIR = Path('/tmp')
    UPLOAD_DIR = TMP_DIR / 'uploads'
else:
    UPLOAD_DIR = BASE_DIR / 'app' / 'static' / 'uploads'

STATIC_DIR = BASE_DIR / 'app' / 'static'
TEMPLATES_DIR = BASE_DIR / 'app' / 'templates'
PUBLIC_DIR = BASE_DIR / 'public'

try:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    pass

class Settings:
    PROJECT_NAME: str = 'Female-Fabric'
    PROJECT_DESCRIPTION: str = 'Интернет-магазин современной женской одежды Female-Fabric'
    VERSION: str = '1.0.0'
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    
    SITE_URL: str = os.getenv('SITE_URL', 'https://female-fabric.workers.dev').rstrip('/')
    
    # Secret Key: require from environment, or generate secure random key if not provided
    SECRET_KEY: str = os.getenv('SECRET_KEY') or secrets.token_hex(32)
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    CORS_ORIGINS: list[str] = [o.strip() for o in os.getenv('CORS_ORIGINS', '*').split(',') if o.strip()]
    
    # Database
    default_db = f'sqlite:////tmp/female_fabric.db' if (IS_VERCEL or IS_WORKER) else f'sqlite:///{BASE_DIR}/female_fabric.db'
    DATABASE_URL: str = os.getenv('DATABASE_URL', default_db)
    AUTO_CREATE_TABLES: bool = os.getenv('AUTO_CREATE_TABLES', 'false').lower() in ('true', '1', 't', 'yes')
    
    # Uploads & Assets
    UPLOAD_DIR: Path = UPLOAD_DIR
    STATIC_DIR: Path = STATIC_DIR
    TEMPLATES_DIR: Path = TEMPLATES_DIR
    PUBLIC_DIR: Path = PUBLIC_DIR
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5 MB
    ALLOWED_IMAGE_TYPES: list[str] = ['image/jpeg', 'image/png', 'image/webp', 'image/avif']
    
    # Supabase Integration
    SUPABASE_URL: str = os.getenv('SUPABASE_URL', '').rstrip('/')
    SUPABASE_KEY: str = os.getenv('SUPABASE_KEY', '')
    SUPABASE_STORAGE_BUCKET: str = os.getenv('SUPABASE_STORAGE_BUCKET', 'uploads')
    
    # Store settings
    FREE_SHIPPING_THRESHOLD: float = 5000.0
    DEFAULT_SHIPPING_COST: float = 390.0

settings = Settings()

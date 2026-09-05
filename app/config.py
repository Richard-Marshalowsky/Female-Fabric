import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Check if running in Vercel serverless environment
IS_VERCEL = (
    os.getenv('VERCEL', '0') == '1'
    or os.getenv('VERCEL_ENV') is not None
    or os.getenv('AWS_LAMBDA_FUNCTION_NAME') is not None
    or 'LAMBDA_TASK_ROOT' in os.environ
    or os.getenv('VERCEL_URL') is not None
)

SEED_DB_PATH = BASE_DIR / 'app' / 'data' / 'female_fabric.db'

if IS_VERCEL:
    UPLOAD_DIR = Path('/tmp/uploads')
    STATIC_DIR = BASE_DIR / 'app' / 'static'
    TEMPLATES_DIR = BASE_DIR / 'app' / 'templates'
    PUBLIC_DIR = BASE_DIR / 'public'
    DEFAULT_DB_PATH = '/tmp/female_fabric.db'
    
    # Auto-copy pre-seeded SQLite database to writable /tmp
    try:
        target_db = Path(DEFAULT_DB_PATH)
        if SEED_DB_PATH.exists():
            import shutil
            target_db.parent.mkdir(parents=True, exist_ok=True)
            # Copy always on container start to guarantee latest data & hashes
            shutil.copyfile(SEED_DB_PATH, target_db)
            print("[Vercel Init] Seed database copied to /tmp/female_fabric.db")
    except Exception as e:
        print(f"[Vercel Init Warning] Could not copy seed DB: {e}")
else:
    UPLOAD_DIR = BASE_DIR / 'app' / 'static' / 'uploads'
    STATIC_DIR = BASE_DIR / 'app' / 'static'
    TEMPLATES_DIR = BASE_DIR / 'app' / 'templates'
    PUBLIC_DIR = BASE_DIR / 'public'
    DEFAULT_DB_PATH = str(BASE_DIR / 'female_fabric.db')

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class Settings:
    PROJECT_NAME: str = 'Female-Fabric'
    PROJECT_DESCRIPTION: str = 'Інтернет-магазин сучасної жіночої одежды Female-Fabric'
    VERSION: str = '1.0.0'
    
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'female-fabric-super-secure-secret-key-2026-xyz987')
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    DATABASE_URL: str = os.getenv('DATABASE_URL', f'sqlite:///{DEFAULT_DB_PATH}')
    SITE_URL: str = os.getenv('SITE_URL', 'http://localhost:8000')
    CORS_ORIGINS: list[str] = ['*']
    
    # Uploads & Paths
    UPLOAD_DIR: Path = UPLOAD_DIR
    STATIC_DIR: Path = STATIC_DIR
    TEMPLATES_DIR: Path = TEMPLATES_DIR
    PUBLIC_DIR: Path = PUBLIC_DIR
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5 MB
    ALLOWED_IMAGE_TYPES: list[str] = ['image/jpeg', 'image/png', 'image/webp', 'image/avif']
    AUTO_CREATE_TABLES: bool = os.getenv('AUTO_CREATE_TABLES', '1') in ('1', 'true', 'True', 'yes')

    # Supabase (Optional storage/database)
    SUPABASE_URL: str = os.getenv('SUPABASE_URL', '')
    SUPABASE_KEY: str = os.getenv('SUPABASE_KEY', '')
    SUPABASE_STORAGE_BUCKET: str = os.getenv('SUPABASE_STORAGE_BUCKET', 'female-fabric-images')
    
    # Store settings (in UAH ₴)
    FREE_SHIPPING_THRESHOLD: float = 2500.0  # Безкоштовна доставка від 2500 грн
    DEFAULT_SHIPPING_COST: float = 120.0     # Стандартна доставка 120 грн

settings = Settings()

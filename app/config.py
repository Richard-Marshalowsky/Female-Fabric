import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / 'app' / 'static' / 'uploads'
STATIC_DIR = BASE_DIR / 'app' / 'static'
TEMPLATES_DIR = BASE_DIR / 'app' / 'templates'

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class Settings:
    PROJECT_NAME: str = 'Female-Fabric'
    PROJECT_DESCRIPTION: str = 'Интернет-магазин современной женской одежды Female-Fabric'
    VERSION: str = '1.0.0'
    
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'female-fabric-super-secure-secret-key-2026-xyz987')
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    DATABASE_URL: str = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/female_fabric.db')
    
    # Uploads
    UPLOAD_DIR: Path = UPLOAD_DIR
    STATIC_DIR: Path = STATIC_DIR
    TEMPLATES_DIR: Path = TEMPLATES_DIR
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5 MB
    ALLOWED_IMAGE_TYPES: list[str] = ['image/jpeg', 'image/png', 'image/webp', 'image/avif']
    
    # Store settings
    FREE_SHIPPING_THRESHOLD: float = 5000.0  # Бесплатная доставка от 5000 руб
    DEFAULT_SHIPPING_COST: float = 390.0

settings = Settings()

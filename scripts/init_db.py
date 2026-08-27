import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import Base, engine, SessionLocal
from app.core.seed_data import seed_database
from app.config import settings

def init_and_seed():
    print("=" * 60)
    print(" Female-Fabric Database Initialization / Migration")
    print(f" Target Database: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else settings.DATABASE_URL}")
    print("=" * 60)

    print("Creating all tables in database...")
    Base.metadata.create_all(bind=engine)
    print("[OK] Tables created successfully.")

    print("Seeding initial data (categories, admin user, products)...")
    db = SessionLocal()
    try:
        seed_database(db)
        print("[OK] Database seeded successfully.")
    finally:
        db.close()

if __name__ == '__main__':
    init_and_seed()

import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

db_url = settings.DATABASE_URL
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql+pg8000://', 1)
elif db_url.startswith('postgresql://') and not db_url.startswith('postgresql+'):
    db_url = db_url.replace('postgresql://', 'postgresql+pg8000://', 1)

connect_args = {}
if 'sqlite' in db_url:
    connect_args['check_same_thread'] = False

try:
    engine = create_engine(
        db_url,
        connect_args=connect_args
    )
except Exception:
    engine = create_engine('sqlite:////tmp/female_fabric.db', connect_args={'check_same_thread': False})

if 'sqlite' in str(engine.url):
    @event.listens_for(engine, 'connect')
    def set_sqlite_pragma(dbapi_connection, connection_record):
        try:
            cursor = dbapi_connection.cursor()
            cursor.execute('PRAGMA foreign_keys=ON')
            cursor.close()
        except Exception:
            pass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

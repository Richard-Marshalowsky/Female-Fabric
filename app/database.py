import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Detect if running in Cloudflare Workers (Pyodide)
IS_WORKERS = os.getenv("CF_PAGES") == "1" or os.getenv("CF_WORKER") == "1" or "pyodide" in os.sys.executable.lower()

if IS_WORKERS:
    # In Workers: use Supabase REST API (PostgREST) via httpx
    # SQLAlchemy engine/session not used; models will need HTTP adapters
    engine = None
    SessionLocal = None
    Base = declarative_base()
    
    # Placeholder for HTTP-based database access
    class SupabaseHTTP:
        def __init__(self):
            import httpx
            self.url = settings.SUPABASE_URL.rstrip('/')
            self.key = settings.SUPABASE_KEY
            self.headers = {
                "apikey": self.key,
                "Authorization": f"Bearer {self.key}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
            self.client = httpx.AsyncClient(base_url=f"{self.url}/rest/v1", headers=self.headers, timeout=30.0)
        
        async def request(self, method: str, table: str, **kwargs):
            params = kwargs.get('params', {})
            json_data = kwargs.get('json')
            headers = kwargs.get('headers', {})
            resp = await self.client.request(method, f"/{table}", params=params, json=json_data, headers=headers)
            resp.raise_for_status()
            return resp.json()
        
        async def select(self, table: str, columns: str = "*", filters: dict = None, limit: int = None, offset: int = None, order: str = None):
            params = {"select": columns}
            if filters:
                for k, v in filters.items():
                    params[k] = f"eq.{v}"
            if limit:
                params["limit"] = str(limit)
            if offset:
                params["offset"] = str(offset)
            if order:
                params["order"] = order
            return await self.request("GET", table, params=params)
        
        async def insert(self, table: str, data: dict):
            return await self.request("POST", table, json=data)
        
        async def update(self, table: str, data: dict, filters: dict):
            params = {}
            for k, v in filters.items():
                params[k] = f"eq.{v}"
            return await self.request("PATCH", table, params=params, json=data)
        
        async def delete(self, table: str, filters: dict):
            params = {}
            for k, v in filters.items():
                params[k] = f"eq.{v}"
            return await self.request("DELETE", table, params=params)
    
    supabase_http = SupabaseHTTP()
    
    def get_db():
        # Not used in Workers; endpoints should use supabase_http directly
        yield None

else:
    # Local development: normal SQLAlchemy with SQLite or pg8000
    db_url = settings.DATABASE_URL
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql+pg8000://', 1)
    elif db_url.startswith('postgresql://') and not db_url.startswith('postgresql+'):
        db_url = db_url.replace('postgresql://', 'postgresql+pg8000://', 1)

    connect_args = {}
    if 'sqlite' in db_url:
        connect_args['check_same_thread'] = False

    engine = create_engine(
        db_url,
        connect_args=connect_args
    )

    # Enable foreign keys for SQLite
    if 'sqlite' in db_url:
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

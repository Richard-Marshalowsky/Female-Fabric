import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_admin_real_persistence():
    print("=" * 60)
    print(" Testing Admin Backend Persistence & CRUD Operations")
    print("=" * 60)

    # 1. Login as Admin
    login_res = client.post("/api/auth/login", json={
        "email": "admin@female-fabric.ua",
        "password": "wPSg*3@wQ@k)AcpU)xx4nddK"
    })
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("  [OK] Admin authenticated successfully")

    # 2. Get Categories to get a valid category_id
    cats_res = client.get("/api/categories")
    cat_id = cats_res.json()[0]["id"]

    # 3. Create a new Product as Admin
    import time
    sku_val = f"FF-TEST-{int(time.time())}"
    new_prod_payload = {
        "name": "Тестова шовкова сукня Couture 2026",
        "sku": sku_val,
        "category_id": cat_id,
        "price": 4200.0,
        "old_price": 5000.0,
        "description": "Ексклюзивна сукня, створена через адмін-панель.",
        "details_json": '{"composition": "100% шовк", "care": "Суха хімчистка"}',
        "is_active": True,
        "is_featured": True,
        "is_new": True,
        "images": [
            "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=1000"
        ],
        "variants": [
            {"size": "XS", "color": "Чорний", "color_code": "#000000", "stock": 5, "sku": "FF-TEST-XS"},
            {"size": "S", "color": "Чорний", "color_code": "#000000", "stock": 10, "sku": "FF-TEST-S"},
            {"size": "M", "color": "Чорний", "color_code": "#000000", "stock": 8, "sku": "FF-TEST-M"}
        ]
    }

    create_res = client.post("/api/admin/products", json=new_prod_payload, headers=headers)
    assert create_res.status_code == 200, f"Create product failed: {create_res.text}"
    created_prod = create_res.json()
    prod_id = created_prod["id"]
    prod_slug = created_prod["slug"]
    print(f"  [OK] Created product id={prod_id}, slug='{prod_slug}'")

    # 4. Read product via public API to verify it is live in SQLite
    public_res = client.get(f"/api/products/{created_prod['slug']}")
    assert public_res.status_code == 200
    assert public_res.json()["price"] == 4200.0
    assert len(public_res.json()["variants"]) == 3
    print("  [OK] Product instantly visible in public catalog with 3 size variants!")

    # 5. Update Product as Admin (change price, description, and add size L)
    update_payload = {
        "price": 3950.0,
        "description": "Оновлений опис товару через панель адміністратора.",
        "variants": [
            {"size": "XS", "color": "Чорний", "color_code": "#000000", "stock": 5, "sku": "FF-TEST-XS"},
            {"size": "S", "color": "Чорний", "color_code": "#000000", "stock": 10, "sku": "FF-TEST-S"},
            {"size": "M", "color": "Чорний", "color_code": "#000000", "stock": 8, "sku": "FF-TEST-M"},
            {"size": "L", "color": "Чорний", "color_code": "#000000", "stock": 12, "sku": "FF-TEST-L"}
        ]
    }
    update_res = client.put(f"/api/admin/products/{prod_id}", json=update_payload, headers=headers)
    assert update_res.status_code == 200
    print("  [OK] Updated product price to 3950.0 and added size L")

    # 6. Verify update in DB
    verify_res = client.get(f"/api/products/{created_prod['slug']}")
    assert verify_res.json()["price"] == 3950.0
    assert len(verify_res.json()["variants"]) == 4
    print("  [OK] Verified: Updated price (3950.0) and 4 sizes (XS, S, M, L) are persistent!")

    # 7. Clean up test product
    del_res = client.delete(f"/api/admin/products/{prod_id}", headers=headers)
    assert del_res.status_code == 200
    print(f"  [OK] Cleaned up test product id={prod_id}")

    print("\n[SUCCESS] Admin backend is 100% active, reactive, and persistent in the database!")

if __name__ == "__main__":
    test_admin_real_persistence()

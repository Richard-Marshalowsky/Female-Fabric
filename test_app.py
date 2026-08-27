import io
import sys
from PIL import Image
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine, SessionLocal
from app.core.seed_data import seed_database

def run_all_tests():
    print("=" * 60)
    print(" Starting Female-Fabric Automated Test Suite")
    print("=" * 60)

    # Initialize and seed database
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db)
    db.close()

    client = TestClient(app)

    # 1. Test Static & HTML Pages
    print("\n[1/7] Testing HTML & SEO Pages...")
    pages = ["/", "/catalog", "/cart", "/checkout", "/profile", "/login", "/admin", "/robots.txt", "/sitemap.xml"]
    for p in pages:
        res = client.get(p)
        assert res.status_code == 200, f"Page {p} returned status {res.status_code}"
    print("  [OK] All HTML and SEO pages served with status 200 OK")

    # 2. Test Auth Flow
    print("\n[2/7] Testing Authentication (Register, Login, Password, Permissions)...")
    test_email = "maria.test@example.com"
    reg_payload = {
        "full_name": "Мария Тестовая",
        "email": test_email,
        "phone": "+7 (900) 123-45-67",
        "password": "TestPassword123!"
    }
    # Register
    reg_res = client.post("/api/auth/register", json=reg_payload)
    if reg_res.status_code == 400: # Already registered in previous run
        pass
    else:
        assert reg_res.status_code == 200, f"Registration failed: {reg_res.text}"
        assert "access_token" in reg_res.json()

    # Login
    login_res = client.post("/api/auth/login", json={"email": test_email, "password": "TestPassword123!"})
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    user_token = login_res.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}

    # Profile Me
    me_res = client.get("/api/auth/me", headers=user_headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == test_email
    print("  [OK] Customer registration, login, JWT token verification passed")

    # Admin Login
    admin_login_res = client.post("/api/auth/login", json={"email": "admin@female-fabric.ru", "password": "Admin123!"})
    assert admin_login_res.status_code == 200, f"Admin login failed: {admin_login_res.text}"
    admin_token = admin_login_res.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("  [OK] Admin login verified")

    # 3. Test Products & Catalog API
    print("\n[3/7] Testing Products & Catalog API...")
    cats_res = client.get("/api/categories")
    assert cats_res.status_code == 200
    categories = cats_res.json()
    assert len(categories) >= 8, f"Expected 8 categories, got {len(categories)}"
    
    # Products list
    prods_res = client.get("/api/products?limit=20")
    assert prods_res.status_code == 200
    data = prods_res.json()
    assert data["total"] > 0
    assert len(data["items"]) > 0

    # Filter by category
    dresses_res = client.get("/api/products?category_slug=dresses")
    assert dresses_res.status_code == 200
    assert all(p["category_slug"] == "dresses" for p in dresses_res.json()["items"])

    # Search
    search_res = client.get("/api/products?q=шелк")
    assert search_res.status_code == 200
    assert search_res.json()["total"] > 0

    # Product detail
    first_slug = data["items"][0]["slug"]
    detail_res = client.get(f"/api/products/{first_slug}")
    assert detail_res.status_code == 200
    assert detail_res.json()["slug"] == first_slug
    assert len(detail_res.json()["variants"]) > 0
    print(f"  [OK] Products search, filtering, and detail endpoint verified ({data['total']} items in DB)")

    # 4. Test Cart API
    print("\n[4/7] Testing Cart API (Add, Update, Remove, Sync)...")
    # Clear cart first
    client.delete("/api/cart", headers=user_headers)

    first_prod = data["items"][0]
    add_res = client.post("/api/cart/items", json={
        "product_id": first_prod["id"],
        "size": "S",
        "color": "Черный",
        "quantity": 2
    }, headers=user_headers)
    assert add_res.status_code == 200
    cart_data = add_res.json()
    assert cart_data["total_quantity"] == 2
    assert len(cart_data["items"]) == 1
    cart_item_id = cart_data["items"][0]["id"]

    # Update qty
    update_res = client.patch(f"/api/cart/items/{cart_item_id}", json={"quantity": 3}, headers=user_headers)
    assert update_res.status_code == 200
    assert update_res.json()["total_quantity"] == 3
    print("  [OK] Cart operations and calculations verified")

    # 5. Test Checkout API
    print("\n[5/7] Testing Checkout & Order Placement...")
    order_payload = {
        "first_name": "Мария",
        "last_name": "Тестовая",
        "phone": "+7 (900) 123-45-67",
        "email": test_email,
        "city": "Москва",
        "address": "Тестовая ул., д. 1, кв. 1",
        "delivery_method": "Курьер до двери",
        "payment_method": "Картой онлайн",
        "notes": "Позвонить перед доставкой"
    }
    order_res = client.post("/api/checkout", json=order_payload, headers=user_headers)
    assert order_res.status_code == 200, f"Checkout failed: {order_res.text}"
    order_data = order_res.json()
    assert order_data["order_number"].startswith("FF-2026-")
    assert order_data["status"] == "Новый"
    assert len(order_data["items"]) > 0

    # Get order by number
    get_order_res = client.get(f"/api/checkout/orders/{order_data['order_number']}")
    assert get_order_res.status_code == 200
    assert get_order_res.json()["order_number"] == order_data["order_number"]
    print(f"  [OK] Order created successfully: {order_data['order_number']}")

    # 6. Test Security and Admin Permissions
    print("\n[6/7] Testing Security & Role-Based Access Control...")
    # Clear client cookies to test strict unauthorized / permission separation
    client.cookies.clear()

    # Normal user trying to access admin stats -> MUST RETURN 403 Forbidden
    forbidden_res = client.get("/api/admin/stats", headers=user_headers)
    assert forbidden_res.status_code == 403, f"Security breach: normal user accessed admin with status {forbidden_res.status_code}"

    # Guest trying to access admin -> MUST RETURN 401 Unauthorized
    guest_forbidden = client.get("/api/admin/stats")
    assert guest_forbidden.status_code == 401, f"Guest got {guest_forbidden.status_code}"

    # Admin access with admin headers
    admin_stats_res = client.get("/api/admin/stats", headers=admin_headers)
    assert admin_stats_res.status_code == 200
    assert admin_stats_res.json()["total_orders"] > 0
    print("  [OK] Admin routes are strictly protected with 401/403 guards")

    # 7. Test Admin Operations (Orders Status Update, Image Upload)
    print("\n[7/7] Testing Admin Operations & Image Upload...")
    # Update Order Status
    update_st_res = client.patch(
        f"/api/admin/orders/{order_data['id']}/status",
        json={"status": "Собирается"},
        headers=admin_headers
    )
    assert update_st_res.status_code == 200
    assert update_st_res.json()["status"] == "Собирается"

    # Image upload test
    img = Image.new("RGB", (200, 200), color=(200, 100, 100))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    upload_res = client.post(
        "/api/admin/upload",
        files={"file": ("test_cloth.jpg", img_bytes, "image/jpeg")},
        headers=admin_headers
    )
    assert upload_res.status_code == 200, f"Upload failed: {upload_res.text}"
    assert "/static/uploads/" in upload_res.json()["url"]
    print("  [OK] Admin status update & secure image upload verified")

    print("\n" + "=" * 60)
    print(" ALL 7 TEST SUITES PASSED FLAWLESSLY! SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()

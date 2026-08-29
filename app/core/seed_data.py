import json
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.category import Category
from app.models.product import Product, ProductImage, ProductVariant
from app.models.order import Order, OrderItem
from app.models.address import Address
from app.core.security import get_password_hash

def seed_database(db: Session):
    # 1. Admin User
    admin = db.query(User).filter(User.email == "admin@female-fabric.ru").first()
    if not admin:
        admin = User(
            email="admin@female-fabric.ru",
            hashed_password=get_password_hash("Admin123!"),
            full_name="Олена Коваленко (Адмін)",
            phone="+380971234567",
            role="admin",
            is_active=True
        )
        db.add(admin)

    # 2. Customer User
    customer = db.query(User).filter(User.email == "user@female-fabric.ru").first()
    if not customer:
        customer = User(
            email="user@female-fabric.ru",
            hashed_password=get_password_hash("User123!"),
            full_name="Марія Мельник",
            phone="+380509876543",
            role="customer",
            is_active=True
        )
        db.add(customer)
        db.flush()

        addr = Address(
            user_id=customer.id,
            title="Домашня адреса",
            city="Київ",
            address="вул. Хрещатик, буд. 15, кв. 42",
            is_default=True
        )
        db.add(addr)

    db.commit()

    # 3. Categories
    categories_data = [
        {"name": "Сукні та шовк", "slug": "dresses", "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800", "sort_order": 1},
        {"name": "Блузи та сорочки", "slug": "blouses", "image_url": "https://images.unsplash.com/photo-1598554747436-c9293d6a588f?w=800", "sort_order": 2},
        {"name": "Костюми та жакети", "slug": "suits", "image_url": "https://images.unsplash.com/photo-1584273143981-41c073dfe8f8?w=800", "sort_order": 3},
        {"name": "Штани та джинси", "slug": "trousers", "image_url": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800", "sort_order": 4},
        {"name": "Верхній одяг", "slug": "outerwear", "image_url": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=800", "sort_order": 5},
        {"name": "Спідниці", "slug": "skirts", "image_url": "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=800", "sort_order": 6},
        {"name": "Трикотаж та светри", "slug": "knitwear", "image_url": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=800", "sort_order": 7},
        {"name": "Аксесуари", "slug": "accessories", "image_url": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=800", "sort_order": 8},
    ]

    category_map = {}
    for cat_d in categories_data:
        existing = db.query(Category).filter(Category.slug == cat_d["slug"]).first()
        if not existing:
            cat = Category(
                name=cat_d["name"],
                slug=cat_d["slug"],
                image_url=cat_d["image_url"],
                sort_order=cat_d["sort_order"]
            )
            db.add(cat)
            db.flush()
            category_map[cat_d["slug"]] = cat.id
        else:
            existing.name = cat_d["name"]
            category_map[cat_d["slug"]] = existing.id

    db.commit()

    # 4. Products
    products_data = [
        {
            "name": "Шовкова сукня Velvet Night",
            "slug": "silk-dress-velvet-night",
            "sku": "FF-DR-001",
            "category_slug": "dresses",
            "price": 3850.0,
            "old_price": 4500.0,
            "description": "Вишукана сукня-комбінація з натурального шовку Mulberry. Лаконічний крій підкреслює силует, а регульовані бретелі забезпечують ідеальну посадку.",
            "details_json": json.dumps({"composition": "100% шовк Mulberry", "fit": "Струмуючий силует", "season": "Всесезон", "care": "Делікатне сухе чищення"}),
            "is_featured": True,
            "is_new": True,
            "images": [
                "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=1000",
                "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=1000"
            ],
            "colors": [{"name": "Чорний", "code": "#000000"}, {"name": "Нюд", "code": "#E3C2B0"}],
            "sizes": ["XS", "S", "M", "L"]
        },
        {
            "name": "Двобортний шерстяний жакет Royal Classic",
            "slug": "wool-blazer-royal-classic",
            "sku": "FF-ST-002",
            "category_slug": "suits",
            "price": 5400.0,
            "old_price": 6200.0,
            "description": "Двобортний жакет із преміальної тонкої вовни Super 120s. Чітка лінія плечей, шовкова підкладка та ґудзики з рогового матеріалу.",
            "details_json": json.dumps({"composition": "95% вовна, 5% еластан", "fit": "Оверсайз крій", "season": "Осінь/Весна", "care": "Хімчистка"}),
            "is_featured": True,
            "is_new": True,
            "images": [
                "https://images.unsplash.com/photo-1584273143981-41c073dfe8f8?w=1000",
                "https://images.unsplash.com/photo-1548624313-0396c75e4b1a?w=1000"
            ],
            "colors": [{"name": "Бежевий", "code": "#C5A880"}, {"name": "Чорний", "code": "#000000"}],
            "sizes": ["S", "M", "L"]
        },
        {
            "name": "Шовкова блуза з бантом Ivory Grace",
            "slug": "silk-blouse-ivory-grace",
            "sku": "FF-BL-003",
            "category_slug": "blouses",
            "price": 2900.0,
            "old_price": 3400.0,
            "description": "Класична блуза з ніжним коміром-бантом. Виконана з шовкового крепу, чудово поєднується як з діловими костюмами, так і з джинсами.",
            "details_json": json.dumps({"composition": "100% натуральний шовк", "fit": "Прямий крій", "season": "Всесезон", "care": "Ручне прання 30°C"}),
            "is_featured": True,
            "is_new": False,
            "images": [
                "https://images.unsplash.com/photo-1598554747436-c9293d6a588f?w=1000"
            ],
            "colors": [{"name": "Молочний", "code": "#FAF8F5"}, {"name": "Шампань", "code": "#F7E7CE"}],
            "sizes": ["XS", "S", "M", "L"]
        },
        {
            "name": "Кашемірове пальто-халат Cashmere Touch",
            "slug": "cashmere-coat-touch",
            "sku": "FF-OW-004",
            "category_slug": "outerwear",
            "price": 12500.0,
            "old_price": 14900.0,
            "description": "Розкішне пальто фасону халат з м'якого кашеміру з додаванням шерсті альпака. Глибокий захід, поясок та місткі кишені.",
            "details_json": json.dumps({"composition": "70% кашемір, 30% шерсть альпака", "fit": "Вільний", "season": "Осінь/Зима", "care": "Спеціалізована хімчистка"}),
            "is_featured": True,
            "is_new": True,
            "images": [
                "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=1000"
            ],
            "colors": [{"name": "Кемел", "code": "#C19A6B"}, {"name": "Графіт", "code": "#383838"}],
            "sizes": ["S", "M", "L"]
        },
        {
            "name": "Класичні штани палаццо High Style",
            "slug": "palazzo-pants-high-style",
            "sku": "FF-TR-005",
            "category_slug": "trousers",
            "price": 3100.0,
            "old_price": None,
            "description": "Штани палаццо високої посадки зі стрілками. Вони візуально подовжують силует і створюють елегантний образ.",
            "details_json": json.dumps({"composition": "65% віскоза, 30% вовна, 5% еластан", "fit": "Широкий", "season": "Всесезон", "care": "Делікатне прання"}),
            "is_featured": False,
            "is_new": True,
            "images": [
                "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=1000"
            ],
            "colors": [{"name": "Чорний", "code": "#000000"}, {"name": "Молочний", "code": "#FAF8F5"}],
            "sizes": ["XS", "S", "M", "L"]
        },
        {
            "name": "Трикотажний джемпер Soft Cashmere Blend",
            "slug": "knit-jumper-cashmere-blend",
            "sku": "FF-KN-006",
            "category_slug": "knitwear",
            "price": 2600.0,
            "old_price": 3100.0,
            "description": "Ніжний та теплий джемпер з суміші мериносової вовни та кашеміру. М'який комір та манжети у резинку.",
            "details_json": json.dumps({"composition": "80% меринос, 20% кашемір", "fit": "Вільний", "season": "Осінь/Зима", "care": "Ручне прання"}),
            "is_featured": True,
            "is_new": False,
            "images": [
                "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=1000"
            ],
            "colors": [{"name": "Бежевий", "code": "#D2B48C"}, {"name": "Сірий", "code": "#808080"}],
            "sizes": ["S", "M", "L"]
        }
    ]

    for p_data in products_data:
        existing = db.query(Product).filter((Product.slug == p_data["slug"]) | (Product.sku == p_data["sku"])).first()
        if not existing:
            cat_id = category_map.get(p_data["category_slug"])
            product = Product(
                name=p_data["name"],
                slug=p_data["slug"],
                sku=p_data["sku"],
                category_id=cat_id,
                price=p_data["price"],
                old_price=p_data.get("old_price"),
                description=p_data["description"],
                details_json=p_data["details_json"],
                is_featured=p_data["is_featured"],
                is_new=p_data["is_new"],
                is_active=True
            )
            db.add(product)
            db.flush()

            for idx, img_url in enumerate(p_data["images"]):
                img = ProductImage(
                    product_id=product.id,
                    image_url=img_url,
                    is_primary=(idx == 0),
                    sort_order=idx
                )
                db.add(img)

            for c in p_data["colors"]:
                for s in p_data["sizes"]:
                    variant = ProductVariant(
                        product_id=product.id,
                        sku=f"{product.sku}-{s}-{c['name'][:2].upper()}",
                        size=s,
                        color=c["name"],
                        color_code=c["code"],
                        stock=12,
                        price_override=None
                    )
                    db.add(variant)

    db.commit()

    # 5. Sample Order
    sample_order = db.query(Order).filter(Order.order_number == "FF-2026-0001").first()
    if not sample_order:
        first_prod = db.query(Product).first()
        if first_prod:
            sample_order = Order(
                order_number="FF-2026-0001",
                user_id=customer.id,
                status="Підтверджений",
                subtotal_amount=first_prod.price,
                discount_amount=0.0,
                delivery_fee=0.0,
                total_amount=first_prod.price,
                first_name="Марія",
                last_name="Мельник",
                phone="+380509876543",
                email="user@female-fabric.ru",
                city="Київ",
                address="вул. Хрещатик, буд. 15, кв. 42",
                delivery_method="Нова Пошта (Пункт видачі)",
                payment_method="Карткою онлайн",
                payment_status="Оплачено",
                notes="Дзвінок кур'єра за 30 хвилин"
            )
            db.add(sample_order)
            db.flush()

            item = OrderItem(
                order_id=sample_order.id,
                product_id=first_prod.id,
                product_name=first_prod.name,
                sku=first_prod.sku,
                size="S",
                color="Чорний",
                price=first_prod.price,
                quantity=1,
                image_url="https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=300"
            )
            db.add(item)
            db.commit()

    print("Database successfully seeded with Ukrainian dataset!")

import json
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.category import Category
from app.models.product import Product, ProductImage, ProductVariant
from app.models.address import Address
from app.models.order import Order, OrderItem
from app.core.security import hash_password

def seed_database(db: Session):
    if db.query(Category).count() > 0:
        return

    print('Starting database seeding...')

    admin_user = User(
        email='admin@female-fabric.ru',
        password_hash=hash_password('Admin123!'),
        full_name='Анастасия Романова (Администратор)',
        phone='+7 (999) 000-00-01',
        role='admin',
        is_active=True
    )
    db.add(admin_user)

    demo_user = User(
        email='user@female-fabric.ru',
        password_hash=hash_password('User123!'),
        full_name='Екатерина Смирнова',
        phone='+7 (916) 123-45-67',
        role='user',
        is_active=True
    )
    db.add(demo_user)
    db.commit()

    demo_address = Address(
        user_id=demo_user.id,
        title='Домашний адрес',
        city='Москва',
        address='Кутузовский проспект, д. 24, кв. 85',
        postal_code='121151',
        is_default=True
    )
    db.add(demo_address)
    db.commit()

    categories_data = [
        {'name': 'Платья', 'slug': 'dresses', 'description': 'Элегантные вечерние, коктейльные и повседневные платья из натуральных тканей.', 'image_url': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&q=80', 'sort_order': 1},
        {'name': 'Блузки и рубашки', 'slug': 'blouses', 'description': 'Шелковые блузы, хлопковые оверсайз рубашки и женственные топы.', 'image_url': 'https://images.unsplash.com/photo-1608234808654-2a8875fa74ec?w=800&q=80', 'sort_order': 2},
        {'name': 'Костюмы и жакеты', 'slug': 'suits', 'description': 'Идеально скроенные брючные костюмы, твидовые жакеты и оверсайз блейзеры.', 'image_url': 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=800&q=80', 'sort_order': 3},
        {'name': 'Брюки и джинсы', 'slug': 'trousers', 'description': 'Широкие брюки палаццо, классические прямые модели и премиальный деним.', 'image_url': 'https://images.unsplash.com/photo-1509551388413-e18d0ac5d495?w=800&q=80', 'sort_order': 4},
        {'name': 'Верхняя одежда', 'slug': 'outerwear', 'description': 'Кашемировые пальто, тренчи из непромокаемого хлопка и стильные дубленки.', 'image_url': 'https://images.unsplash.com/photo-1544923246-77307dd654cb?w=800&q=80', 'sort_order': 5},
        {'name': 'Юбки', 'slug': 'skirts', 'description': 'Шелковые миди-юбки, плиссированные модели и юбки-карандаш высокой посадки.', 'image_url': 'https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=800&q=80', 'sort_order': 6},
        {'name': 'Трикотаж', 'slug': 'knitwear', 'description': 'Уютные джемперы из мериносовой шерсти, кашемировые кардиганы и базовые лонгсливы.', 'image_url': 'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=800&q=80', 'sort_order': 7},
        {'name': 'Аксессуары', 'slug': 'accessories', 'description': 'Кожаные ремни, шелковые платки, сумки-багеты и дизайнерские украшения.', 'image_url': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=800&q=80', 'sort_order': 8}
    ]

    cat_map = {}
    for cdata in categories_data:
        cat = Category(**cdata, is_active=True)
        db.add(cat)
        db.flush()
        cat_map[cat.slug] = cat.id

    products_seed = [
        {
            'category_slug': 'dresses',
            'name': 'Шелковое платье-комбинация в длине миди',
            'slug': 'silk-slip-midi-dress',
            'sku': 'FF-DR-001',
            'price': 12990.0,
            'old_price': 15990.0,
            'is_featured': True,
            'is_new': True,
            'description': 'Культовое шелковое платье-комбинация полуприлегающего силуэта на тонких бретелях. Струящийся шелк деликатно подчеркивает линии фигуры.',
            'details': {
                'composition': '92% натуральный шелк Mulberry, 8% эластан',
                'fit': 'Полуприлегающий крой по косой, длина миди',
                'season': 'Мультисезон',
                'care': 'Деликатная сухая чистка или ручная стирка 30°C'
            },
            'images': [
                'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&q=80',
                'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=800&q=80'
            ],
            'variants': [
                {'size': 'XS', 'color': 'Изумрудный', 'color_code': '#0f4c3a', 'stock': 5, 'sku': 'FF-DR-001-EM-XS'},
                {'size': 'S', 'color': 'Изумрудный', 'color_code': '#0f4c3a', 'stock': 8, 'sku': 'FF-DR-001-EM-S'},
                {'size': 'M', 'color': 'Изумрудный', 'color_code': '#0f4c3a', 'stock': 6, 'sku': 'FF-DR-001-EM-M'},
                {'size': 'L', 'color': 'Изумрудный', 'color_code': '#0f4c3a', 'stock': 3, 'sku': 'FF-DR-001-EM-L'},
                {'size': 'S', 'color': 'Шампань', 'color_code': '#f7e7ce', 'stock': 7, 'sku': 'FF-DR-001-CH-S'},
                {'size': 'M', 'color': 'Шампань', 'color_code': '#f7e7ce', 'stock': 4, 'sku': 'FF-DR-001-CH-M'},
                {'size': 'S', 'color': 'Черный', 'color_code': '#111111', 'stock': 10, 'sku': 'FF-DR-001-BK-S'},
                {'size': 'M', 'color': 'Черный', 'color_code': '#111111', 'stock': 9, 'sku': 'FF-DR-001-BK-M'}
            ]
        },
        {
            'category_slug': 'dresses',
            'name': 'Платье-жакет прямого кроя с поясом',
            'slug': 'blazer-dress-with-belt',
            'sku': 'FF-DR-002',
            'price': 16490.0,
            'old_price': 18990.0,
            'is_featured': True,
            'is_new': False,
            'description': 'Структурированное платье-блейзер с двубортной застежкой на акцентные пуговицы. В комплекте съемный ремень с пряжкой.',
            'details': {
                'composition': '65% шерсть, 30% вискоза, 5% эластан',
                'fit': 'Двубортный прямой крой',
                'season': 'Демисезон',
                'care': 'Химчистка'
            },
            'images': [
                'https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=800&q=80',
                'https://images.unsplash.com/photo-1502716119720-b23a93e5fe1b?w=800&q=80'
            ],
            'variants': [
                {'size': 'XS', 'color': 'Песочный', 'color_code': '#c2b280', 'stock': 4, 'sku': 'FF-DR-002-SD-XS'},
                {'size': 'S', 'color': 'Песочный', 'color_code': '#c2b280', 'stock': 7, 'sku': 'FF-DR-002-SD-S'},
                {'size': 'M', 'color': 'Песочный', 'color_code': '#c2b280', 'stock': 5, 'sku': 'FF-DR-002-SD-M'},
                {'size': 'S', 'color': 'Черный графит', 'color_code': '#2b2b2b', 'stock': 8, 'sku': 'FF-DR-002-BK-S'}
            ]
        },
        {
            'category_slug': 'dresses',
            'name': 'Трикотажное платье-макси с открытой спиной',
            'slug': 'knit-maxi-dress-open-back',
            'sku': 'FF-DR-003',
            'price': 11200.0,
            'old_price': None,
            'is_featured': False,
            'is_new': True,
            'description': 'Эффектное облегающее платье в пол из плотного эластичного трикотажа с овальным вырезом на спине.',
            'details': {
                'composition': '70% вискоза, 30% нейлон',
                'fit': 'Slim fit, длина макси',
                'season': 'Все сезоны',
                'care': 'Стирка 30°C'
            },
            'images': [
                'https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=800&q=80'
            ],
            'variants': [
                {'size': 'XS', 'color': 'Шоколадный', 'color_code': '#3d2314', 'stock': 5, 'sku': 'FF-DR-003-CH-XS'},
                {'size': 'S', 'color': 'Шоколадный', 'color_code': '#3d2314', 'stock': 12, 'sku': 'FF-DR-003-CH-S'},
                {'size': 'M', 'color': 'Шоколадный', 'color_code': '#3d2314', 'stock': 8, 'sku': 'FF-DR-003-CH-M'}
            ]
        },
        {
            'category_slug': 'blouses',
            'name': 'Оверсайз рубашка из органического хлопка',
            'slug': 'oversized-organic-cotton-shirt',
            'sku': 'FF-BL-001',
            'price': 7490.0,
            'old_price': 8990.0,
            'is_featured': True,
            'is_new': False,
            'description': 'Базовая рубашка свободной посадки со спущенным плечом из плотного хлопка.',
            'details': {
                'composition': '100% органический хлопок GOTS',
                'fit': 'Oversize',
                'season': 'Всесезонный',
                'care': 'Машинная стирка 40°C'
            },
            'images': [
                'https://images.unsplash.com/photo-1608234808654-2a8875fa74ec?w=800&q=80'
            ],
            'variants': [
                {'size': 'XS', 'color': 'Белоснежный', 'color_code': '#ffffff', 'stock': 15, 'sku': 'FF-BL-001-WH-XS'},
                {'size': 'S', 'color': 'Белоснежный', 'color_code': '#ffffff', 'stock': 12, 'sku': 'FF-BL-001-WH-S'},
                {'size': 'M', 'color': 'Белоснежный', 'color_code': '#ffffff', 'stock': 10, 'sku': 'FF-BL-001-WH-M'},
                {'size': 'S', 'color': 'Голубой', 'color_code': '#87ceeb', 'stock': 9, 'sku': 'FF-BL-001-BL-S'}
            ]
        },
        {
            'category_slug': 'blouses',
            'name': 'Шелковая блузка с воротником аскот',
            'slug': 'silk-tie-neck-blouse',
            'sku': 'FF-BL-002',
            'price': 11990.0,
            'old_price': 14500.0,
            'is_featured': False,
            'is_new': True,
            'description': 'Женственная блуза из натурального шелкового крепдешина с длинными лентами воротника.',
            'details': {
                'composition': '100% шелк',
                'fit': 'Прямой свободный крой',
                'season': 'Всесезонный',
                'care': 'Сухая чистка'
            },
            'images': [
                'https://images.unsplash.com/photo-1551803091-e20673f15770?w=800&q=80'
            ],
            'variants': [
                {'size': 'XS', 'color': 'Пудровый', 'color_code': '#e8c5c8', 'stock': 4, 'sku': 'FF-BL-002-PK-XS'},
                {'size': 'S', 'color': 'Пудровый', 'color_code': '#e8c5c8', 'stock': 7, 'sku': 'FF-BL-002-PK-S'},
                {'size': 'M', 'color': 'Пудровый', 'color_code': '#e8c5c8', 'stock': 5, 'sku': 'FF-BL-002-PK-M'},
                {'size': 'S', 'color': 'Молочный', 'color_code': '#fdfbf7', 'stock': 8, 'sku': 'FF-BL-002-ML-S'}
            ]
        },
        {
            'category_slug': 'suits',
            'name': 'Однобортный шерстяной жакет оверсайз',
            'slug': 'oversized-wool-blazer',
            'sku': 'FF-ST-001',
            'price': 18990.0,
            'old_price': 22500.0,
            'is_featured': True,
            'is_new': True,
            'description': 'Флагманский жакет прямого кроя из высококачественной итальянской шерсти.',
            'details': {
                'composition': '100% шерсть Super 120s',
                'fit': 'Masculine oversize fit',
                'season': 'Осень / Весна / Зима',
                'care': 'Химчистка'
            },
            'images': [
                'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=800&q=80'
            ],
            'variants': [
                {'size': 'XS', 'color': 'Серый меланж', 'color_code': '#8a8d8f', 'stock': 6, 'sku': 'FF-ST-001-GR-XS'},
                {'size': 'S', 'color': 'Серый меланж', 'color_code': '#8a8d8f', 'stock': 10, 'sku': 'FF-ST-001-GR-S'},
                {'size': 'M', 'color': 'Серый меланж', 'color_code': '#8a8d8f', 'stock': 8, 'sku': 'FF-ST-001-GR-M'},
                {'size': 'S', 'color': 'Черный', 'color_code': '#000000', 'stock': 9, 'sku': 'FF-ST-001-BK-S'}
            ]
        },
        {
            'category_slug': 'suits',
            'name': 'Твидовый укороченный жакет',
            'slug': 'cropped-tweed-jacket',
            'sku': 'FF-ST-002',
            'price': 15990.0,
            'old_price': None,
            'is_featured': False,
            'is_new': True,
            'description': 'Элегантный жакет из фактурного твида с золотистыми пуговицами.',
            'details': {
                'composition': '50% хлопок, 35% шерсть, 15% люрекс',
                'fit': 'Укороченный силуэт',
                'season': 'Весна / Осень',
                'care': 'Химчистка'
            },
            'images': [
                'https://images.unsplash.com/photo-1548624149-f9b1859aa9d0?w=800&q=80'
            ],
            'variants': [
                {'size': 'XS', 'color': 'Кремовый', 'color_code': '#fdf5e6', 'stock': 5, 'sku': 'FF-ST-002-CR-XS'},
                {'size': 'S', 'color': 'Кремовый', 'color_code': '#fdf5e6', 'stock': 8, 'sku': 'FF-ST-002-CR-S'},
                {'size': 'M', 'color': 'Кремовый', 'color_code': '#fdf5e6', 'stock': 4, 'sku': 'FF-ST-002-CR-M'}
            ]
        },
        {
            'category_slug': 'trousers',
            'name': 'Брюки-палаццо со складками у пояса',
            'slug': 'palazzo-wide-leg-trousers',
            'sku': 'FF-TR-001',
            'price': 9990.0,
            'old_price': 11990.0,
            'is_featured': True,
            'is_new': False,
            'description': 'Широкие струящиеся брюки палаццо с высокой посадкой и глубокими защипами.',
            'details': {
                'composition': '70% вискоза, 25% полиэстер, 5% спандекс',
                'fit': 'Высокая посадка, свободные от бедра',
                'season': 'Всесезонный',
                'care': 'Стирка 30°C'
            },
            'images': [
                'https://images.unsplash.com/photo-1509551388413-e18d0ac5d495?w=800&q=80'
            ],
            'variants': [
                {'size': 'XS', 'color': 'Молочный', 'color_code': '#fcfaf2', 'stock': 6, 'sku': 'FF-TR-001-ML-XS'},
                {'size': 'S', 'color': 'Молочный', 'color_code': '#fcfaf2', 'stock': 11, 'sku': 'FF-TR-001-ML-S'},
                {'size': 'M', 'color': 'Молочный', 'color_code': '#fcfaf2', 'stock': 8, 'sku': 'FF-TR-001-ML-M'},
                {'size': 'S', 'color': 'Темно-синий', 'color_code': '#1a2942', 'stock': 9, 'sku': 'FF-TR-001-NV-S'}
            ]
        },
        {
            'category_slug': 'trousers',
            'name': 'Прямые джинсы с высокой посадкой',
            'slug': 'vintage-straight-high-waist-jeans',
            'sku': 'FF-TR-002',
            'price': 8490.0,
            'old_price': None,
            'is_featured': False,
            'is_new': True,
            'description': 'Классические прямые джинсы из 100% плотного премиального денима.',
            'details': {
                'composition': '100% хлопок',
                'fit': 'High rise, прямые',
                'season': 'Всесезонный',
                'care': 'Стирка 30°C'
            },
            'images': [
                'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=800&q=80'
            ],
            'variants': [
                {'size': 'XS', 'color': 'Индиго', 'color_code': '#2f4f4f', 'stock': 5, 'sku': 'FF-TR-002-IN-XS'},
                {'size': 'S', 'color': 'Индиго', 'color_code': '#2f4f4f', 'stock': 12, 'sku': 'FF-TR-002-IN-S'},
                {'size': 'M', 'color': 'Индиго', 'color_code': '#2f4f4f', 'stock': 9, 'sku': 'FF-TR-002-IN-M'},
                {'size': 'L', 'color': 'Индиго', 'color_code': '#2f4f4f', 'stock': 4, 'sku': 'FF-TR-002-IN-L'}
            ]
        },
        {
            'category_slug': 'outerwear',
            'name': 'Двубортное пальто-халат из шерсти и кашемира',
            'slug': 'wool-cashmere-wrap-coat',
            'sku': 'FF-OW-001',
            'price': 27990.0,
            'old_price': 34990.0,
            'is_featured': True,
            'is_new': True,
            'description': 'Премиальное пальто-халат длины макси с глубоким английским воротником и мягким поясом.',
            'details': {
                'composition': '80% шерсть, 20% кашемир',
                'fit': 'Свободный крой с поясом, длина 125 см',
                'season': 'Холодная осень / Зима',
                'care': 'Химчистка'
            },
            'images': [
                'https://images.unsplash.com/photo-1544923246-77307dd654cb?w=800&q=80'
            ],
            'variants': [
                {'size': 'XS', 'color': 'Camel', 'color_code': '#c19a6b', 'stock': 3, 'sku': 'FF-OW-001-CM-XS'},
                {'size': 'S', 'color': 'Camel', 'color_code': '#c19a6b', 'stock': 7, 'sku': 'FF-OW-001-CM-S'},
                {'size': 'M', 'color': 'Camel', 'color_code': '#c19a6b', 'stock': 5, 'sku': 'FF-OW-001-CM-M'},
                {'size': 'S', 'color': 'Черный', 'color_code': '#1a1a1a', 'stock': 6, 'sku': 'FF-OW-001-BK-S'}
            ]
        },
        {
            'category_slug': 'outerwear',
            'name': 'Классический водостойкий тренч',
            'slug': 'classic-waterproof-cotton-trench',
            'sku': 'FF-OW-002',
            'price': 19990.0,
            'old_price': 23990.0,
            'is_featured': True,
            'is_new': False,
            'description': 'Двубортный тренчкот прямого силуэта со штормовым клапаном и поясом.',
            'details': {
                'composition': '100% хлопок с водоотталкивающей пропиткой',
                'fit': 'Regular oversize fit',
                'season': 'Весна / Осень',
                'care': 'Химчистка'
            },
            'images': [
                'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=800&q=80'
            ],
            'variants': [
                {'size': 'XS', 'color': 'Бежевый', 'color_code': '#f5f0eb', 'stock': 4, 'sku': 'FF-OW-002-BG-XS'},
                {'size': 'S', 'color': 'Бежевый', 'color_code': '#f5f0eb', 'stock': 9, 'sku': 'FF-OW-002-BG-S'},
                {'size': 'M', 'color': 'Бежевый', 'color_code': '#f5f0eb', 'stock': 6, 'sku': 'FF-OW-002-BG-M'}
            ]
        },
        {
            'category_slug': 'skirts',
            'name': 'Шелковая юбка миди по косой',
            'slug': 'bias-cut-silk-midi-skirt',
            'sku': 'FF-SK-001',
            'price': 8990.0,
            'old_price': 10500.0,
            'is_featured': True,
            'is_new': False,
            'description': 'Бестселлер коллекции: струящаяся шелковая юбка с атласным благородным блеском.',
            'details': {
                'composition': '100% шелк',
                'fit': 'A-силуэт по косой, миди',
                'season': 'Всесезонный',
                'care': 'Ручная стирка 30°C'
            },
            'images': [
                'https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=800&q=80'
            ],
            'variants': [
                {'size': 'XS', 'color': 'Хаки', 'color_code': '#556b2f', 'stock': 6, 'sku': 'FF-SK-001-OL-XS'},
                {'size': 'S', 'color': 'Хаки', 'color_code': '#556b2f', 'stock': 10, 'sku': 'FF-SK-001-OL-S'},
                {'size': 'M', 'color': 'Хаки', 'color_code': '#556b2f', 'stock': 7, 'sku': 'FF-SK-001-OL-M'},
                {'size': 'S', 'color': 'Крем', 'color_code': '#f8f4ee', 'stock': 12, 'sku': 'FF-SK-001-CR-S'}
            ]
        },
        {
            'category_slug': 'skirts',
            'name': 'Плиссированная юбка миди из тонкой экокожи',
            'slug': 'pleated-faux-leather-midi-skirt',
            'sku': 'FF-SK-002',
            'price': 7990.0,
            'old_price': None,
            'is_featured': False,
            'is_new': True,
            'description': 'Графичная плиссированная юбка из мягкой экокожи с матовым финишем.',
            'details': {
                'composition': '100% полиуретан',
                'fit': 'A-силуэт с плиссировкой',
                'season': 'Осень / Зима / Весна',
                'care': 'Деликатная чистка'
            },
            'images': [
                'https://images.unsplash.com/photo-1577900232427-18219b9166a0?w=800&q=80'
            ],
            'variants': [
                {'size': 'XS', 'color': 'Шоколадный', 'color_code': '#3b281f', 'stock': 4, 'sku': 'FF-SK-002-CH-XS'},
                {'size': 'S', 'color': 'Шоколадный', 'color_code': '#3b281f', 'stock': 8, 'sku': 'FF-SK-002-CH-S'},
                {'size': 'M', 'color': 'Шоколадный', 'color_code': '#3b281f', 'stock': 5, 'sku': 'FF-SK-002-CH-M'}
            ]
        },
        {
            'category_slug': 'knitwear',
            'name': 'Свитер оверсайз из 100% кашемира',
            'slug': 'oversized-pure-cashmere-sweater',
            'sku': 'FF-KN-001',
            'price': 21990.0,
            'old_price': 25990.0,
            'is_featured': True,
            'is_new': True,
            'description': 'Невероятно мягкий и теплый кашемировый свитер объемной вязки со спущенным плечом.',
            'details': {
                'composition': '100% кашемир',
                'fit': 'Loose oversize',
                'season': 'Зима / Демисезон',
                'care': 'Ручная стирка'
            },
            'images': [
                'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=800&q=80'
            ],
            'variants': [
                {'size': 'XS', 'color': 'Овсяный', 'color_code': '#d8cbb8', 'stock': 6, 'sku': 'FF-KN-001-OT-XS'},
                {'size': 'S', 'color': 'Овсяный', 'color_code': '#d8cbb8', 'stock': 8, 'sku': 'FF-KN-001-OT-S'},
                {'size': 'M', 'color': 'Овсяный', 'color_code': '#d8cbb8', 'stock': 7, 'sku': 'FF-KN-001-OT-M'},
                {'size': 'S', 'color': 'Терракотовый', 'color_code': '#c35b38', 'stock': 5, 'sku': 'FF-KN-001-TR-S'}
            ]
        },
        {
            'category_slug': 'knitwear',
            'name': 'Кардиган тонкой вязки с перламутровыми пуговицами',
            'slug': 'fine-knit-cardigan-pearl-buttons',
            'sku': 'FF-KN-002',
            'price': 8990.0,
            'old_price': 10500.0,
            'is_featured': False,
            'is_new': False,
            'description': 'Нежный базовый кардиган с V-образным вырезом из ультратонкой мериносовой шерсти.',
            'details': {
                'composition': '100% шерсть мериноса',
                'fit': 'Regular fit',
                'season': 'Всесезонный',
                'care': 'Деликатная стирка 30°C'
            },
            'images': [
                'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&q=80'
            ],
            'variants': [
                {'size': 'XS', 'color': 'Голубой', 'color_code': '#a0c4e2', 'stock': 5, 'sku': 'FF-KN-002-BL-XS'},
                {'size': 'S', 'color': 'Голубой', 'color_code': '#a0c4e2', 'stock': 9, 'sku': 'FF-KN-002-BL-S'},
                {'size': 'M', 'color': 'Голубой', 'color_code': '#a0c4e2', 'stock': 6, 'sku': 'FF-KN-002-BL-M'},
                {'size': 'S', 'color': 'Ванильный', 'color_code': '#fdfaf2', 'stock': 8, 'sku': 'FF-KN-002-VN-S'}
            ]
        },
        {
            'category_slug': 'accessories',
            'name': 'Сумка-багет из натуральной гладкой кожи',
            'slug': 'leather-baguette-shoulder-bag',
            'sku': 'FF-AC-001',
            'price': 14990.0,
            'old_price': 17500.0,
            'is_featured': True,
            'is_new': True,
            'description': 'Лаконичная плечевая сумка минималистичной формы из кожи теленка.',
            'details': {
                'composition': '100% натуральная кожа',
                'fit': 'Размеры: 26 × 14 × 6 см',
                'season': 'Всесезонный',
                'care': 'Крем для кожи'
            },
            'images': [
                'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=800&q=80'
            ],
            'variants': [
                {'size': 'One Size', 'color': 'Черный', 'color_code': '#050505', 'stock': 12, 'sku': 'FF-AC-001-BK'},
                {'size': 'One Size', 'color': 'Шоколадный', 'color_code': '#3e2723', 'stock': 8, 'sku': 'FF-AC-001-CH'}
            ]
        },
        {
            'category_slug': 'accessories',
            'name': 'Шелковый платок с арт-принтом',
            'slug': 'printed-silk-square-scarf',
            'sku': 'FF-AC-002',
            'price': 4990.0,
            'old_price': None,
            'is_featured': False,
            'is_new': False,
            'description': 'Квадратный платок 90×90 см из натурального шелка саржевого плетения.',
            'details': {
                'composition': '100% шелк твил',
                'fit': 'Размер 90 × 90 см',
                'season': 'Всесезонный',
                'care': 'Сухая чистка'
            },
            'images': [
                'https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=800&q=80'
            ],
            'variants': [
                {'size': '90x90', 'color': 'Изумруд', 'color_code': '#2e8b57', 'stock': 15, 'sku': 'FF-AC-002-EM'},
                {'size': '90x90', 'color': 'Терракота', 'color_code': '#cc7722', 'stock': 10, 'sku': 'FF-AC-002-TC'}
            ]
        }
    ]

    for pdata in products_seed:
        cat_id = cat_map.get(pdata['category_slug'])
        prod = Product(
            category_id=cat_id,
            name=pdata['name'],
            slug=pdata['slug'],
            sku=pdata['sku'],
            description=pdata['description'],
            details_json=json.dumps(pdata['details'], ensure_ascii=False),
            price=pdata['price'],
            old_price=pdata['old_price'],
            is_active=True,
            is_featured=pdata['is_featured'],
            is_new=pdata['is_new']
        )
        db.add(prod)
        db.flush()

        for idx, img_url in enumerate(pdata['images']):
            img = ProductImage(
                product_id=prod.id,
                image_url=img_url,
                is_primary=(idx == 0),
                sort_order=idx
            )
            db.add(img)

        for v in pdata['variants']:
            variant = ProductVariant(
                product_id=prod.id,
                size=v['size'],
                color=v['color'],
                color_code=v.get('color_code', '#000000'),
                sku=v['sku'],
                stock=v['stock']
            )
            db.add(variant)

    db.commit()

    sample_order = Order(
        order_number='FF-2026-1082',
        user_id=demo_user.id,
        status='Отправлен',
        total_amount=21980.0,
        subtotal_amount=21980.0,
        discount_amount=0.0,
        delivery_fee=0.0,
        first_name='Екатерина',
        last_name='Смирнова',
        phone='+7 (916) 123-45-67',
        email='user@female-fabric.ru',
        city='Москва',
        address='Кутузовский проспект, д. 24, кв. 85',
        delivery_method='Курьер до двери',
        payment_method='Картой онлайн',
        payment_status='Оплачен',
        notes='Пожалуйста, позвоните за 1 час до доставки',
        created_at=datetime.now(timezone.utc) - timedelta(days=2)
    )
    db.add(sample_order)
    db.flush()

    sample_item = OrderItem(
        order_id=sample_order.id,
        product_id=1,
        product_name='Шелковое платье-комбинация в длине миди',
        sku='FF-DR-001-EM-S',
        size='S',
        color='Изумрудный',
        price=12990.0,
        quantity=1,
        image_url='https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&q=80'
    )
    sample_item2 = OrderItem(
        order_id=sample_order.id,
        product_id=7,
        product_name='Шелковая юбка миди по косой',
        sku='FF-SK-001-CR-S',
        size='S',
        color='Крем',
        price=8990.0,
        quantity=1,
        image_url='https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=800&q=80'
    )
    db.add(sample_item)
    db.add(sample_item2)

    db.commit()
    print('Database successfully seeded with categories, products, variants, users, and demo orders!')

if __name__ == '__main__':
    from app.database import engine, Base, SessionLocal
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db)
    db.close()

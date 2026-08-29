import os
import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\Pc\.gemini\antigravity\scratch\female-fabric")
TEMPLATES_DIR = BASE_DIR / "app" / "templates"
PUBLIC_DIR = BASE_DIR / "public"
STATIC_JS_DIR = BASE_DIR / "app" / "static" / "js"

# 1. Comprehensive i18n.js
i18n_content = """// Internationalization Dictionary (Default: Ukrainian, Switchable to Russian)
window.I18N = {
  currentLang: localStorage.getItem('female_fabric_lang') || 'ua',

  translations: {
    ua: {
      // Header & Navigation
      nav_home: "Головна",
      nav_catalog: "Каталог",
      nav_dresses: "Сукні",
      nav_blouses: "Блузи та сорочки",
      nav_suits: "Костюми",
      nav_trousers: "Штани та джинси",
      nav_outerwear: "Верхній одяг",
      nav_knitwear: "Трикотаж",
      nav_sale: "Sale",
      nav_cabinet: "Кабінет",
      nav_admin: "Адмінка",
      nav_cart: "Кошик",
      nav_profile: "Профіль",
      nav_wishlist: "Обране",
      search_placeholder: "Пошук одягу...",
      menu_all_catalog: "Увесь каталог",
      
      // Top Announcement & Delivery
      announcement: "Безкоштовна доставка з приміркою при замовленні від 2 500 ₴ | Знижка 10% на перше замовлення",
      free_ship_text: "Безкоштовна доставка від 2 500 ₴",
      free_ship_included: "✓ Безкоштовна доставка включена!",
      to_free_shipping: "До безкоштовної доставки:",
      
      // Home Page
      hero_subtitle: "НОВА КОЛЕКЦІЯ 2026",
      hero_title: "Елегантність у кожній нитці",
      hero_desc: "Бездоганний крій, преміальні натуральні тканини та витончений стиль для сучасної жінки.",
      hero_btn_catalog: "Дивитися каталог",
      hero_btn_dresses: "Сукні та шовк",
      cat_title: "Категорії одягу",
      cat_subtitle: "КОЛЕКЦІЇ",
      cat_view_all: "Усі категорії →",
      featured_title: "Популярні моделі",
      featured_subtitle: "ВИБІР СТИЛІСТІВ",
      featured_view_all: "Дивитися всі →",
      promo_subtitle: "СПЕЦІАЛЬНА ПРОПОЗИЦІЯ",
      promo_title: "Весняна елегантність зі знижкою до 25%",
      promo_desc: "Поповніть гардероб вишуканими шовковими комбінаціями, шерстяними жакетами та струмуючими штанами.",
      promo_btn: "Перейти до знижок",
      new_title: "Нові надходження",
      new_subtitle: "НОВИНКИ ТИЖНЯ",
      new_view_all: "Усі новинки →",
      
      // Advantages
      adv_1_title: "Примірка перед покупкою",
      adv_1_desc: "Кур'єр зачекає 15 хвилин, поки ви приміряєте обрані моделі.",
      adv_2_title: "Швидка доставка",
      adv_2_desc: "Доставка по всій Україні Новою Поштою або Укрпоштою.",
      adv_3_title: "100% натуральні тканини",
      adv_3_desc: "Шовк Mulberry, кашемір, тонка вовна та органічна бавовна.",
      adv_4_title: "Легке повернення 14 днів",
      adv_4_desc: "Проста процедура повернення без зайвих запитань.",
      
      // Cart & Drawer
      cart_drawer_title: "Кошик покупок",
      cart_empty: "Ваш кошик порожній",
      cart_checkout_btn: "Оформити замовлення",
      cart_view_cart: "Перейти до кошика",
      cart_continue_shopping: "Перейти до покупок",
      cart_continue_browsing: "Продовжити покупки",
      cart_total: "Разом:",
      cart_subtotal: "Сума:",
      cart_delivery: "Доставка:",
      cart_discount: "Знижка:",
      cart_item_qty: "шт.",
      cart_choose_size: "Вибрати розмір",
      cart_add_to_cart: "Додати в кошик",
      cart_added_toast: "додано в кошик",
      cart_remove_item: "Видалити",
      cart_title_page: "Кошик товарів",
      
      // Catalog & Filters
      catalog_title: "Каталог жіночого одягу",
      filter_title: "Фільтри",
      filter_all_categories: "Усі категорії",
      filter_price: "Ціна, ₴",
      filter_size: "Розмір",
      filter_color: "Колір",
      filter_in_stock: "Тільки в наявності",
      filter_on_sale: "Тільки зі знижкою (Sale)",
      filter_reset: "Скинути фільтри",
      filter_apply: "Застосувати",
      sort_label: "Сортування:",
      sort_newest: "Спочатку новинки",
      sort_popular: "За популярністю",
      sort_price_asc: "Від дешевих до дорогих",
      sort_price_desc: "Від дорогих до дешевих",
      catalog_not_found: "За вашим запитом нічого не знайдено",
      catalog_try_reset: "Спробуйте скинути фільтри або змінити пошуковий запит",
      catalog_load_more: "Завантажити ще",
      
      // Product Details
      product_sku: "Артикул:",
      product_select_size: "Оберіть розмір:",
      product_select_color: "Колір:",
      product_size_guide: "Таблиця розмірів",
      product_in_stock: "В наявності",
      product_out_of_stock: "Немає в наявності",
      product_add_cart: "Додати в кошик",
      product_add_fav: "В обране",
      product_in_fav: "В обраному",
      product_desc_tab: "Опис",
      product_details_tab: "Характеристики та догляд",
      product_delivery_tab: "Доставка та повернення",
      product_similar_title: "Вам також може сподобатися",
      
      // Checkout
      checkout_title: "Оформлення замовлення",
      checkout_contact_info: "1. Контактні дані",
      checkout_delivery_info: "2. Доставка по Україні",
      checkout_payment_info: "3. Спосіб оплати",
      checkout_name: "Ім'я",
      checkout_lastname: "Прізвище",
      checkout_phone: "Телефон",
      checkout_email: "Email",
      checkout_city: "Місто",
      checkout_city_placeholder: "Київ, Львів, Одеса...",
      checkout_address: "Адреса або № відділення Нової Пошти",
      checkout_delivery_np: "Нова Пошта (Відділення / Поштомат)",
      checkout_delivery_courier: "Кур'єр Нової Пошти за адресою",
      checkout_delivery_ukrposhta: "Укрпошта Експрес",
      checkout_pay_online: "Карткою онлайн (Visa / Mastercard / Apple Pay)",
      checkout_pay_cod: "Післяплата при отриманні (Нова Пошта)",
      checkout_notes: "Коментар до замовлення (необов'язково)",
      checkout_submit_btn: "Підтвердити замовлення",
      checkout_order_summary: "Ваше замовлення",
      checkout_free: "Безкоштовно",
      checkout_placing: "Оформлення...",
      
      // Order Success
      success_title: "Дякуємо за замовлення!",
      success_subtitle: "Ваше замовлення успішно прийнято в обробку.",
      success_order_num: "Номер замовлення:",
      success_manager_contact: "Наш менеджер зв'яжеться з вами найближчим часом для підтвердження деталей відправки.",
      success_home_btn: "Повернутися на головну",
      success_catalog_btn: "Продовжити покупки",
      
      // Profile
      profile_title: "Особистий кабінет",
      profile_tab_orders: "Мої замовлення",
      profile_tab_info: "Особисті дані",
      profile_tab_fav: "Обрані товари",
      profile_logout: "Вийти з акаунту",
      profile_save_btn: "Зберегти зміни",
      profile_no_orders: "У вас поки що немає оформлених замовлень",
      profile_no_fav: "У вас поки що немає обраних товарів",
      
      // Auth Modal & Login Page
      auth_login_title: "Вхід",
      auth_register_title: "Реєстрація",
      auth_btn_login: "Увійти в акаунт",
      auth_btn_reg: "Зареєструватися",
      auth_email: "Email",
      auth_password: "Пароль",
      auth_name: "Ваше ім'я",
      auth_phone: "Телефон",
      auth_forgot: "Забули пароль?",
      auth_no_account: "Немає акаунту?",
      auth_have_account: "Вже зареєстровані?",
      
      // Footer & Common
      footer_about: "Інтернет-магазин жіночого одягу. Лаконічність, якість та естетика на кожний день.",
      footer_catalog: "Каталог",
      footer_customers: "Покупцям",
      footer_newsletter: "Розсилка",
      footer_newsletter_desc: "Отримуйте першими сповіщення про закриті розпродажі та нові колекції.",
      footer_newsletter_btn: "OK",
      footer_rights: "© 2026 Female-Fabric. Всі права захищені.",
      footer_payment_methods: "Оплата карткою онлайн, Apple Pay, Google Pay",
      footer_phone: "Тел: +38 (097) 123-45-67",
      footer_email: "Email: support@female-fabric.ua",
      currency: "₴"
    },
    ru: {
      // Header & Navigation
      nav_home: "Главная",
      nav_catalog: "Каталог",
      nav_dresses: "Платья",
      nav_blouses: "Блузки и рубашки",
      nav_suits: "Костюмы",
      nav_trousers: "Брюки и джинсы",
      nav_outerwear: "Верхняя одежда",
      nav_knitwear: "Трикотаж",
      nav_sale: "Sale",
      nav_cabinet: "Кабинет",
      nav_admin: "Админка",
      nav_cart: "Корзина",
      nav_profile: "Профиль",
      nav_wishlist: "Избранное",
      search_placeholder: "Поиск одежды...",
      menu_all_catalog: "Весь каталог",
      
      // Top Announcement & Delivery
      announcement: "Бесплатная доставка с примеркой при заказе от 2 500 ₴ | Скидка 10% на первый заказ",
      free_ship_text: "Бесплатная доставка от 2 500 ₴",
      free_ship_included: "✓ Бесплатная доставка включена!",
      to_free_shipping: "До бесплатной доставки:",
      
      // Home Page
      hero_subtitle: "НОВАЯ КОЛЛЕКЦИЯ 2026",
      hero_title: "Элегантность в каждой нити",
      hero_desc: "Безупречный крой, премиальные натуральные ткани и утонченный стиль для современной женщины.",
      hero_btn_catalog: "Смотреть каталог",
      hero_btn_dresses: "Платья и шелк",
      cat_title: "Категории одежды",
      cat_subtitle: "КОЛЛЕКЦИИ",
      cat_view_all: "Все категории →",
      featured_title: "Популярные модели",
      featured_subtitle: "ВЫБОР СТИЛИСТОВ",
      featured_view_all: "Смотреть все →",
      promo_subtitle: "СПЕЦИАЛЬНОЕ ПРЕДЛОЖЕНИЕ",
      promo_title: "Весенняя элегантность со скидкой до 25%",
      promo_desc: "Пополните гардероб изысканными шелковыми комбинациями, шерстяными жакетами и струящимися брюками.",
      promo_btn: "Перейти к скидкам",
      new_title: "Новые поступления",
      new_subtitle: "НОВИНКИ НЕДЕЛИ",
      new_view_all: "Все новинки →",
      
      // Advantages
      adv_1_title: "Примерка перед покупкой",
      adv_1_desc: "Курьер подождет 15 минут, пока вы примерите понравившиеся модели.",
      adv_2_title: "Быстрая доставка",
      adv_2_desc: "Доставка по всей Украине Новой Почтой или Укрпочтой.",
      adv_3_title: "100% натуральные ткани",
      adv_3_desc: "Шелк Mulberry, кашемир, тонкая шерсть и органический хлопок.",
      adv_4_title: "Легкий возврат 14 дней",
      adv_4_desc: "Простая процедура возврата без лишних вопросов.",
      
      // Cart & Drawer
      cart_drawer_title: "Корзина покупок",
      cart_empty: "Ваша корзина пуста",
      cart_checkout_btn: "Оформить заказ",
      cart_view_cart: "Перейти в корзину",
      cart_continue_shopping: "Перейти к покупкам",
      cart_continue_browsing: "Продолжить покупки",
      cart_total: "Итого:",
      cart_subtotal: "Сумма:",
      cart_delivery: "Доставка:",
      cart_discount: "Скидка:",
      cart_item_qty: "шт.",
      cart_choose_size: "Выбрать размер",
      cart_add_to_cart: "Добавить в корзину",
      cart_added_toast: "добавлен в корзину",
      cart_remove_item: "Удалить",
      cart_title_page: "Корзина товаров",
      
      // Catalog & Filters
      catalog_title: "Каталог женской одежды",
      filter_title: "Фильтры",
      filter_all_categories: "Все категории",
      filter_price: "Цена, ₴",
      filter_size: "Размер",
      filter_color: "Цвет",
      filter_in_stock: "Только в наличии",
      filter_on_sale: "Только со скидкой (Sale)",
      filter_reset: "Сбросить фильтры",
      filter_apply: "Применить",
      sort_label: "Сортировка:",
      sort_newest: "Сначала новинки",
      sort_popular: "По популярности",
      sort_price_asc: "От дешевых к дорогим",
      sort_price_desc: "От дорогих к дешевым",
      catalog_not_found: "По вашему запросу ничего не найдено",
      catalog_try_reset: "Попробуйте сбросить фильтры или изменить поисковый запрос",
      catalog_load_more: "Загрузить ещё",
      
      // Product Details
      product_sku: "Артикул:",
      product_select_size: "Выберите размер:",
      product_select_color: "Цвет:",
      product_size_guide: "Таблица размеров",
      product_in_stock: "В наличии",
      product_out_of_stock: "Нет в наличии",
      product_add_cart: "Добавить в корзину",
      product_add_fav: "В избранное",
      product_in_fav: "В избранном",
      product_desc_tab: "Описание",
      product_details_tab: "Характеристики и уход",
      product_delivery_tab: "Доставка и возврат",
      product_similar_title: "Вам также может понравиться",
      
      // Checkout
      checkout_title: "Оформление заказа",
      checkout_contact_info: "1. Контактные данные",
      checkout_delivery_info: "2. Доставка по Украине",
      checkout_payment_info: "3. Способ оплаты",
      checkout_name: "Имя",
      checkout_lastname: "Фамилия",
      checkout_phone: "Телефон",
      checkout_email: "Email",
      checkout_city: "Город",
      checkout_city_placeholder: "Киев, Львов, Одесса...",
      checkout_address: "Адрес или № отделения Новой Почты",
      checkout_delivery_np: "Новая Почта (Отделение / Почтомат)",
      checkout_delivery_courier: "Курьер Новой Почты по адресу",
      checkout_delivery_ukrposhta: "Укрпочта Экспресс",
      checkout_pay_online: "Картой онлайн (Visa / Mastercard / Apple Pay)",
      checkout_pay_cod: "Наложенный платеж (Новая Почта)",
      checkout_notes: "Комментарий к заказу (необязательно)",
      checkout_submit_btn: "Подтвердить заказ",
      checkout_order_summary: "Ваш заказ",
      checkout_free: "Бесплатно",
      checkout_placing: "Оформление...",
      
      // Order Success
      success_title: "Спасибо за заказ!",
      success_subtitle: "Ваш заказ успешно принят в обработку.",
      success_order_num: "Номер заказа:",
      success_manager_contact: "Наш менеджер свяжется с вами в ближайшее время для подтверждения деталей отправки.",
      success_home_btn: "Вернуться на главную",
      success_catalog_btn: "Продолжить покупки",
      
      // Profile
      profile_title: "Личный кабинет",
      profile_tab_orders: "Мои заказы",
      profile_tab_info: "Личные данные",
      profile_tab_fav: "Избранные товары",
      profile_logout: "Выйти из аккаунта",
      profile_save_btn: "Сохранить изменения",
      profile_no_orders: "У вас пока нет оформленных заказов",
      profile_no_fav: "У вас пока нет избранных товаров",
      
      // Auth Modal & Login Page
      auth_login_title: "Вход",
      auth_register_title: "Регистрация",
      auth_btn_login: "Войти в аккаунт",
      auth_btn_reg: "Зарегистрироваться",
      auth_email: "Email",
      auth_password: "Пароль",
      auth_name: "Ваше имя",
      auth_phone: "Телефон",
      auth_forgot: "Забыли пароль?",
      auth_no_account: "Нет аккаунта?",
      auth_have_account: "Уже зарегистрированы?",
      
      // Footer & Common
      footer_about: "Интернет-магазин женской одежды. Лаконичность, качество и эстетика на каждый день.",
      footer_catalog: "Каталог",
      footer_customers: "Покупателям",
      footer_newsletter: "Рассылка",
      footer_newsletter_desc: "Получайте первыми уведомления о закрытых распродажах и новых коллекциях.",
      footer_newsletter_btn: "OK",
      footer_rights: "© 2026 Female-Fabric. Все права защищены.",
      footer_payment_methods: "Оплата картами онлайн, Apple Pay, Google Pay",
      footer_phone: "Тел: +38 (097) 123-45-67",
      footer_email: "Email: support@female-fabric.ua",
      currency: "₴"
    }
  },

  t: function(key) {
    const lang = this.currentLang;
    if (this.translations[lang] && this.translations[lang][key] !== undefined) {
      return this.translations[lang][key];
    }
    if (this.translations['ua'] && this.translations['ua'][key] !== undefined) {
      return this.translations['ua'][key];
    }
    return key;
  },

  setLang: function(lang) {
    this.currentLang = lang;
    localStorage.setItem('female_fabric_lang', lang);
    this.applyToDOM();
    if (window.Store) {
      window.Store.emit('lang:changed', lang);
    }
  },

  applyToDOM: function() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      const translation = this.t(key);
      if (translation !== undefined) {
        if (el.tagName === 'INPUT' && el.getAttribute('placeholder')) {
          el.setAttribute('placeholder', translation);
        } else {
          el.textContent = translation;
        }
      }
    });
  }
};

document.addEventListener('DOMContentLoaded', () => {
  window.I18N.applyToDOM();
});
"""

(STATIC_JS_DIR / "i18n.js").write_text(i18n_content, encoding="utf-8")
print("[OK] i18n.js updated")

# 2. Update store.js formatPrice to ₴
store_file = STATIC_JS_DIR / "store.js"
store_text = store_file.read_text(encoding="utf-8")
store_text = store_text.replace("₽", "₴").replace("ru-RU", "uk-UA")
store_file.write_text(store_text, encoding="utf-8")
print("[OK] store.js updated")

# 3. Update lang-switcher.js
lang_switcher_content = """// Language Switcher Component
document.addEventListener('DOMContentLoaded', () => {
  renderLanguageSwitcher();
});

function renderLanguageSwitcher() {
  const current = window.I18N?.currentLang || 'ua';
  const containerHTML = `
    <div class="lang-switcher flex items-center bg-[#F0EDE8] rounded-full p-0.5 text-[11px] font-semibold tracking-wider text-neutral-600 border border-[#E7E2DA]">
      <button type="button" onclick="switchLanguage('ua')" class="px-2 py-0.5 rounded-full transition ${current === 'ua' ? 'bg-neutral-900 text-white shadow-sm' : 'hover:text-neutral-900'}">
        UA
      </button>
      <button type="button" onclick="switchLanguage('ru')" class="px-2 py-0.5 rounded-full transition ${current === 'ru' ? 'bg-neutral-900 text-white shadow-sm' : 'hover:text-neutral-900'}">
        RU
      </button>
    </div>
  `;

  // Insert into header search / right controls area
  const headerRight = document.querySelector('.site-header .flex.items-center.space-x-4');
  if (headerRight && !document.querySelector('.lang-switcher')) {
    headerRight.insertAdjacentHTML('afterbegin', containerHTML);
  }
}

window.switchLanguage = (lang) => {
  if (window.I18N) {
    window.I18N.setLang(lang);
    document.querySelectorAll('.lang-switcher button').forEach(b => {
      b.className = 'px-2 py-0.5 rounded-full transition hover:text-neutral-900';
    });
    const activeBtn = document.querySelector(`.lang-switcher button[onclick="switchLanguage('${lang}')"]`);
    if (activeBtn) {
      activeBtn.className = 'px-2 py-0.5 rounded-full transition bg-neutral-900 text-white shadow-sm';
    }
  }
};
"""
(STATIC_JS_DIR / "lang-switcher.js").write_text(lang_switcher_content, encoding="utf-8")
print("[OK] lang-switcher.js updated")

print("[DONE] Core localization JS updated successfully!")

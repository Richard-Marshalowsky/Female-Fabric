import os
import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\Pc\.gemini\antigravity\scratch\female-fabric")
JS_DIR = BASE_DIR / "app" / "static" / "js"
PUB_JS_DIR = BASE_DIR / "public" / "static" / "js"

# 1. Update app.js
app_js = JS_DIR / "app.js"
app_text = app_js.read_text(encoding="utf-8")
app_text = app_text.replace("До бесплатной доставки:", "До безкоштовної доставки:")
app_text = app_text.replace("✓ Бесплатная доставка включена!", "✓ Безкоштовна доставка включена!")
app_text = app_text.replace("Удалить", "Видалити")
app_text = app_text.replace("Размер:", "Розмір:")
app_text = app_text.replace("Цвет:", "Колір:")
app_text = app_text.replace("Ошибка обновления корзины", "Помилка оновлення кошика")
app_text = app_text.replace("Товар удален из корзины", "Товар видалено з кошика")
app_text = app_text.replace("Ошибка удаления", "Помилка видалення")
app_text = app_text.replace("Ничего не найдено", "Нічого не знайдено")
app_js.write_text(app_text, encoding="utf-8")
print("[OK] app.js localized")

# 2. Update pages/home.js
home_js = JS_DIR / "pages" / "home.js"
home_text = home_js.read_text(encoding="utf-8")
home_text = home_text.replace("моделей", "моделей")
home_text = home_text.replace("Скоро поступят новые модели", "Скоро з'являться нові моделі")
home_text = home_text.replace("title=\"В избранное\"", "title=\"В обране\"")
home_text = home_text.replace("Выбрать размер", "Вибрати розмір")
home_text = home_text.replace("'Одежда'", "'Одяг'")
home_js.write_text(home_text, encoding="utf-8")
print("[OK] pages/home.js localized")

# 3. Update pages/catalog.js
cat_js = JS_DIR / "pages" / "catalog.js"
cat_text = cat_js.read_text(encoding="utf-8")
cat_text = cat_text.replace("Результаты поиска по запросу", "Результати пошуку за запитом")
cat_text = cat_text.replace("Все категории", "Усі категорії")
cat_text = cat_text.replace("Выбрать размер", "Вибрати розмір")
cat_text = cat_text.replace("title=\"В избранное\"", "title=\"В обране\"")
cat_text = cat_text.replace("'Одежда'", "'Одяг'")
cat_text = cat_text.replace("По вашему запросу ничего не найдено", "За вашим запитом нічого не знайдено")
cat_js.write_text(cat_text, encoding="utf-8")
print("[OK] pages/catalog.js localized")

# 4. Update pages/product.js
prod_js = JS_DIR / "pages" / "product.js"
prod_text = prod_js.read_text(encoding="utf-8")
prod_text = prod_text.replace("Добавить в корзину", "Додати в кошик")
prod_text = prod_text.replace("В корзине", "У кошику")
prod_text = prod_text.replace("Товар добавлен в корзину", "Товар додано в кошик")
prod_text = prod_text.replace("Выберите размер перед добавлением в корзину", "Оберіть розмір перед додаванням у кошик")
prod_text = prod_text.replace("Состав:", "Склад:")
prod_text = prod_text.replace("Посадка:", "Посадка:")
prod_text = prod_text.replace("Сезон:", "Сезон:")
prod_text = prod_text.replace("Уход:", "Догляд:")
prod_text = prod_text.replace("Нет в наличии", "Немає в наявності")
prod_text = prod_text.replace("Выбрать размер", "Вибрати розмір")
prod_js.write_text(prod_text, encoding="utf-8")
print("[OK] pages/product.js localized")

# 5. Update pages/cart.js
cart_js = JS_DIR / "pages" / "cart.js"
cart_text = cart_js.read_text(encoding="utf-8")
cart_text = cart_text.replace("Удалить", "Видалити")
cart_text = cart_text.replace("Размер:", "Розмір:")
cart_text = cart_text.replace("Цвет:", "Колір:")
cart_text = cart_text.replace("Бесплатно", "Безкоштовно")
cart_text = cart_text.replace("За тарифами перевозчика", "За тарифами перевізника")
cart_js.write_text(cart_text, encoding="utf-8")
print("[OK] pages/cart.js localized")

# 6. Update pages/checkout.js
chk_js = JS_DIR / "pages" / "checkout.js"
chk_text = chk_js.read_text(encoding="utf-8")
chk_text = chk_text.replace("Оформление...", "Оформлення...")
chk_text = chk_text.replace("Подтвердить заказ", "Підтвердити замовлення")
chk_text = chk_text.replace("Бесплатно", "Безкоштовно")
chk_text = chk_text.replace("Ваша корзина пуста", "Ваш кошик порожній")
chk_text = chk_text.replace("Заполните обязательные поля", "Заповніть обов'язкові поля")
chk_text = chk_text.replace("Размер:", "Розмір:")
chk_text = chk_text.replace("Цвет:", "Колір:")
chk_text = chk_text.replace("шт.", "шт.")
chk_js.write_text(chk_text, encoding="utf-8")
print("[OK] pages/checkout.js localized")

# 7. Update pages/profile.js
prof_js = JS_DIR / "pages" / "profile.js"
prof_text = prof_js.read_text(encoding="utf-8")
prof_text = prof_text.replace("Заказ", "Замовлення")
prof_text = prof_text.replace("Статус:", "Статус:")
prof_text = prof_text.replace("Сумма:", "Сума:")
prof_text = prof_text.replace("Сохранить", "Зберегти")
prof_text = prof_text.replace("Данные успешно сохранены", "Дані успішно збережено")
prof_text = prof_text.replace("Выбрать размер", "Вибрати розмір")
prof_js.write_text(prof_text, encoding="utf-8")
print("[OK] pages/profile.js localized")

# Sync whole app/static to public/static
shutil.copytree(BASE_DIR / "app" / "static", BASE_DIR / "public" / "static", dirs_exist_ok=True)
print("[OK] Synchronized app/static to public/static")

print("[DONE] All JavaScript assets localized and synced successfully!")

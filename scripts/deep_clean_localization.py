import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\Pc\.gemini\antigravity\scratch\female-fabric")
JS_DIR = BASE_DIR / "app" / "static" / "js"
TPL_DIR = BASE_DIR / "app" / "templates"
PUB_DIR = BASE_DIR / "public"

# 1. Update product.js
prod_path = JS_DIR / "pages" / "product.js"
txt = prod_path.read_text(encoding="utf-8")
txt = txt.replace("label = 'Состав'", "label = 'Склад'")
txt = txt.replace("label = 'Посадка и крой'", "label = 'Посадка та крій'")
txt = txt.replace("label = 'Сезон'", "label = 'Сезон'")
txt = txt.replace("label = 'Уход'", "label = 'Догляд'")
txt = txt.replace("Товар не найден", "Товар не знайдено")
txt = txt.replace("В наличии", "В наявності")
txt = txt.replace("Осталось мало", "Залишилося мало")
txt = txt.replace("всего", "усього")
txt = txt.replace("Пожалуйста, выберите размер", "Будь ласка, оберіть розмір")
txt = txt.replace("Добавление...", "Додавання...")
txt = txt.replace("добавлен в корзину", "додано в кошик")
txt = txt.replace("Не удалось добавить в корзину", "Не вдалося додати в кошик")
txt = txt.replace("Покупатель", "Покупець")
txt = txt.replace("oneclick@female-fabric.ru", "oneclick@female-fabric.ua")
txt = txt.replace("city: 'Москва'", "city: 'Київ'")
txt = txt.replace("Уточнить при звонке менеджера (Быстрый заказ в 1 клик)", "Уточнити при дзвінку менеджера (Швидке замовлення в 1 клік)")
txt = txt.replace("Курьер до двери", "Нова Пошта (Кур'єр)")
txt = txt.replace("При получении", "Післяплата")
txt = txt.replace("Быстрый заказ товара:", "Швидке замовлення товару:")
txt = txt.replace("Ошибка оформления заказа", "Помилка оформлення замовлення")
prod_path.write_text(txt, encoding="utf-8")
print("[OK] product.js deep cleaned")

# 2. Update checkout.js
chk_path = JS_DIR / "pages" / "checkout.js"
txt = chk_path.read_text(encoding="utf-8")
txt = txt.replace("Корзина пуста", "Кошик порожній")
txt = txt.replace("Курьер до двери", "Нова Пошта (Кур'єр)")
txt = txt.replace("Картой онлайн", "Карткою онлайн")
txt = txt.replace("Покупатель", "Покупець")
txt = txt.replace("Заказ", "Замовлення")
chk_path.write_text(txt, encoding="utf-8")
print("[OK] checkout.js deep cleaned")

# 3. Update profile.js
prof_path = JS_DIR / "pages" / "profile.js"
txt = prof_path.read_text(encoding="utf-8")
txt = txt.replace("У вас пока нет заказов", "У вас поки немає замовлень")
txt = txt.replace("Перейти к покупкам", "Перейти до покупок")
txt = txt.replace("'ru-RU'", "'uk-UA'")
txt = txt.replace("от ${dateStr}", "від ${dateStr}")
txt = txt.replace("У вас пока нет сохраненных адресов", "У вас поки немає збережених адрес")
txt = txt.replace("Добавить адрес", "Додати адресу")
txt = txt.replace("У вас пока нет избранных товаров", "У вас поки немає обраних товарів")
txt = txt.replace("Перейти в каталог", "Перейти до каталогу")
txt = txt.replace("Адрес успешно сохранен", "Адресу успішно збережено")
txt = txt.replace("Не удалось сохранить адрес", "Не вдалося зберегти адресу")
txt = txt.replace("Адрес успешно удален", "Адресу успішно видалено")
txt = txt.replace("Не удалось удалить адрес", "Не вдалося видалити адресу")
txt = txt.replace("Удалить адрес?", "Видалити адресу?")
prof_path.write_text(txt, encoding="utf-8")
print("[OK] profile.js deep cleaned")

# 4. Update admin.js
adm_path = JS_DIR / "pages" / "admin.js"
txt = adm_path.read_text(encoding="utf-8")
txt = txt.replace("₽", "₴")
txt = txt.replace("'ru-RU'", "'uk-UA'")
txt = txt.replace("Удалить товар", "Видалити товар")
txt = txt.replace("Товар успешно сохранен", "Товар успішно збережено")
txt = txt.replace("Товар успешно удален", "Товар успішно видалено")
txt = txt.replace("Категория успешно сохранена", "Категорію успішно збережено")
txt = txt.replace("Статус заказа обновлен", "Статус замовлення оновлено")
adm_path.write_text(txt, encoding="utf-8")
print("[OK] admin.js deep cleaned")

# 5. Sync all templates and static to public/
for f in TPL_DIR.glob("*.html"):
    shutil.copyfile(f, PUB_DIR / f.name)
shutil.copytree(BASE_DIR / "app" / "static", PUB_DIR / "static", dirs_exist_ok=True)
print("[OK] Synchronized templates and assets to public/")

print("[DONE] Deep clean localization completed!")

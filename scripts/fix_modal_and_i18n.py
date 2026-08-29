import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\Pc\.gemini\antigravity\scratch\female-fabric")
APP_DIR = BASE_DIR / "app"
PUB_DIR = BASE_DIR / "public"

# 1. Update i18n.js with category translations and event firing
i18n_path = APP_DIR / "static" / "js" / "i18n.js"
i18n_content = i18n_path.read_text(encoding="utf-8")

ua_cat_block = """      // Categories
      cat_all: "Усі категорії",
      cat_dresses: "Сукні та шовк",
      cat_blouses: "Блузи та сорочки",
      cat_suits: "Костюми та жакети",
      cat_trousers: "Штани та джинси",
      cat_outerwear: "Верхній одяг",
      cat_skirts: "Спідниці",
      cat_knitwear: "Трикотаж та светри",
      cat_accessories: "Аксесуари",
"""

ru_cat_block = """      // Categories
      cat_all: "Все категории",
      cat_dresses: "Платья и шелк",
      cat_blouses: "Блузки и рубашки",
      cat_suits: "Костюмы и жакеты",
      cat_trousers: "Брюки и джинсы",
      cat_outerwear: "Верхняя одежда",
      cat_skirts: "Юбки",
      cat_knitwear: "Трикотаж и свитеры",
      cat_accessories: "Аксессуары",
"""

if 'cat_dresses:' not in i18n_content:
    i18n_content = i18n_content.replace('cat_view_all: "Усі категорії →",', 'cat_view_all: "Усі категорії →",\n' + ua_cat_block)
    i18n_content = i18n_content.replace('cat_view_all: "Все категории →",', 'cat_view_all: "Все категории →",\n' + ru_cat_block)
    i18n_path.write_text(i18n_content, encoding="utf-8")
    print("[OK] i18n.js updated with category translations")

# 2. Update main.css to ensure modal-dialog is visible when .active
css_path = APP_DIR / "static" / "css" / "main.css"
css_content = css_path.read_text(encoding="utf-8")
if '.drawer-overlay.active .modal-dialog' not in css_content:
    css_content = css_content.replace(
        '.modal-overlay.active .modal-dialog {',
        '.modal-overlay.active .modal-dialog,\n.drawer-overlay.active .modal-dialog,\n.modal-dialog.active {'
    )
    css_path.write_text(css_content, encoding="utf-8")
    print("[OK] main.css updated for modal dialog visibility")

# 3. Update home.js to translate categories dynamically and listen to lang:changed
home_js_path = APP_DIR / "static" / "js" / "pages" / "home.js"
home_js = home_js_path.read_text(encoding="utf-8")
if 'cat_' not in home_js:
    home_js = home_js.replace(
        '${cat.name}</h3>',
        '${window.I18N ? window.I18N.t("cat_" + cat.slug) || cat.name : cat.name}</h3>'
    )
    if "window.Store.on('lang:changed'" not in home_js:
        home_js += """

// Re-render categories on language switch
if (window.Store) {
  window.Store.on('lang:changed', () => {
    loadHomeCategories();
  });
}
"""
    home_js_path.write_text(home_js, encoding="utf-8")
    print("[OK] home.js updated with dynamic category translations")

# 4. Update catalog.js to translate categories dynamically and listen to lang:changed
catalog_js_path = APP_DIR / "static" / "js" / "pages" / "catalog.js"
cat_js = catalog_js_path.read_text(encoding="utf-8")
cat_js = cat_js.replace('<span>Усі категорії</span>', '<span>${window.I18N ? window.I18N.t("cat_all") : "Усі категорії"}</span>')
cat_js = cat_js.replace('<span>${c.name}</span>', '<span>${window.I18N ? window.I18N.t("cat_" + c.slug) || c.name : c.name}</span>')
if "window.Store.on('lang:changed'" not in cat_js:
    cat_js += """

// Re-render categories and products on language switch
if (window.Store) {
  window.Store.on('lang:changed', () => {
    loadCategoriesFilter();
    loadCatalogProducts();
  });
}
"""
catalog_js_path.write_text(cat_js, encoding="utf-8")
print("[OK] catalog.js updated with dynamic category translations")

# 5. Update product.js breadcrumb translation
prod_js_path = APP_DIR / "static" / "js" / "pages" / "product.js"
prod_js = prod_js_path.read_text(encoding="utf-8")
prod_js = prod_js.replace(
    "breadcrumbCategory.textContent = product.category_name || 'Каталог';",
    "breadcrumbCategory.textContent = (window.I18N ? window.I18N.t('cat_' + product.category_slug) : null) || product.category_name || 'Каталог';"
)
prod_js_path.write_text(prod_js, encoding="utf-8")
print("[OK] product.js updated with dynamic category breadcrumb")

# 6. Update all HTML templates to ensure modal overlay has modal-overlay class
for tpl in (APP_DIR / "templates").glob("*.html"):
    t_text = tpl.read_text(encoding="utf-8")
    # ensure modal-overlay class is on auth-modal and one-click-modal
    t_text = t_text.replace(
        'id="auth-modal" class="drawer-overlay',
        'id="auth-modal" class="modal-overlay drawer-overlay'
    )
    t_text = t_text.replace(
        'id="one-click-modal" class="drawer-overlay',
        'id="one-click-modal" class="modal-overlay drawer-overlay'
    )
    tpl.write_text(t_text, encoding="utf-8")

print("[OK] All HTML templates updated")

# 7. Mirror everything to public/
for f in (APP_DIR / "templates").glob("*.html"):
    shutil.copyfile(f, PUB_DIR / f.name)
shutil.copytree(APP_DIR / "static", PUB_DIR / "static", dirs_exist_ok=True)
print("[OK] Synchronized all templates and assets to public/")

print("[COMPLETE] All fixes applied successfully!")

import os
import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\Pc\.gemini\antigravity\scratch\female-fabric")
TPL_DIR = BASE_DIR / "app" / "templates"
PUB_DIR = BASE_DIR / "public"

# Common Header Snippet in Ukrainian with data-i18n
HEADER_HTML = """  <!-- Top Announcement Bar -->
  <div class="bg-[#121212] text-[#FAF8F5] text-xs py-2 text-center tracking-wider">
    <span data-i18n="announcement">Безкоштовна доставка з приміркою при замовленні від 2 500 ₴ | Знижка 10% на перше замовлення</span>
  </div>

  <!-- Header -->
  <header class="site-header sticky top-0 z-40 bg-[#FAF8F5]/90 backdrop-blur border-b border-[#E7E2DA]">
    <div class="container mx-auto px-4 h-20 flex items-center justify-between gap-4">
      
      <!-- Mobile Menu Button -->
      <button class="md:hidden p-2 text-neutral-800" onclick="window.Modal.open('mobile-menu-drawer')">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>
      </button>

      <!-- Logo -->
      <a href="/" class="flex flex-col items-center">
        <span class="font-serif text-2xl md:text-3xl font-semibold tracking-wider uppercase text-neutral-900">Female-Fabric</span>
        <span class="text-[9px] uppercase tracking-[0.25em] text-neutral-500 -mt-1">Atelier & Boutique</span>
      </a>

      <!-- Desktop Nav -->
      <nav class="hidden md:flex items-center space-x-8 text-sm font-medium">
        <a href="/catalog" class="hover:text-neutral-500 transition" data-i18n="nav_catalog">Каталог</a>
        <a href="/catalog?category=dresses" class="hover:text-neutral-500 transition" data-i18n="nav_dresses">Сукні</a>
        <a href="/catalog?category=suits" class="hover:text-neutral-500 transition" data-i18n="nav_suits">Костюми</a>
        <a href="/catalog?category=outerwear" class="hover:text-neutral-500 transition" data-i18n="nav_outerwear">Верхній одяг</a>
        <a href="/catalog?on_sale=true" class="text-rose-600 hover:text-rose-700 font-semibold transition" data-i18n="nav_sale">Sale</a>
      </nav>

      <!-- Right Action Icons & Search -->
      <div class="flex items-center space-x-4">
        <!-- Live Search Container -->
        <div class="search-container relative hidden sm:block w-48 lg:w-64">
          <input type="text" data-i18n="search_placeholder" placeholder="Пошук одягу..." class="site-search-input w-full pl-9 pr-4 py-2 text-xs bg-white border border-[#E7E2DA] rounded-full focus:outline-none focus:border-neutral-900">
          <svg class="absolute left-3 top-2.5 text-neutral-400" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          <div id="search-autocomplete-dropdown" class="hidden absolute top-full left-0 right-0 mt-2 bg-white rounded-lg shadow-xl border border-[#E7E2DA] overflow-hidden z-50"></div>
        </div>

        <!-- Account -->
        <div class="auth-guest-view">
          <button onclick="window.Modal.open('auth-modal')" class="p-2 text-neutral-800 hover:text-neutral-500 transition" title="Увійти в акаунт">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          </button>
        </div>
        <div class="auth-user-view hidden flex items-center space-x-2">
          <a href="/profile" class="p-2 text-neutral-800 hover:text-neutral-500 flex items-center gap-1 text-xs font-medium" title="Особистий кабінет">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <span class="user-name-slot hidden lg:inline" data-i18n="nav_cabinet">Кабінет</span>
          </a>
          <a href="/admin" class="admin-nav-link hidden text-xs bg-neutral-900 text-white px-2.5 py-1 rounded font-medium hover:bg-neutral-800" data-i18n="nav_admin">Адмінка</a>
        </div>

        <!-- Wishlist -->
        <a href="/profile" class="p-2 text-neutral-800 hover:text-neutral-500 relative" title="Обране">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
        </a>

        <!-- Cart Button (Opens Drawer) -->
        <button onclick="window.Modal.open('cart-drawer')" class="p-2 text-neutral-800 hover:text-neutral-500 relative" title="Кошик">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
          <span class="cart-badge-count absolute -top-1 -right-1 bg-neutral-900 text-white text-[10px] font-bold w-5 h-5 rounded-full items-center justify-center hidden">0</span>
        </button>

      </div>
    </div>
  </header>"""

# Common Footer & Modals in Ukrainian with data-i18n
FOOTER_AND_MODALS_HTML = """  <!-- Footer -->
  <footer class="bg-[#161616] text-[#FAF8F5] pt-16 pb-12 mt-auto">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-10 pb-12 border-b border-neutral-800">
        
        <div>
          <div class="font-serif text-2xl tracking-wider uppercase mb-4">Female-Fabric</div>
          <p class="text-xs text-neutral-400 leading-relaxed mb-6" data-i18n="footer_about">
            Інтернет-магазин жіночого одягу. Лаконічність, якість та естетика на кожний день.
          </p>
          <div class="text-xs text-neutral-400">
            <div data-i18n="footer_phone">Тел: +38 (097) 123-45-67</div>
            <div data-i18n="footer_email">Email: support@female-fabric.ua</div>
          </div>
        </div>

        <div>
          <h4 class="font-medium text-sm text-neutral-200 mb-4 uppercase tracking-wider" data-i18n="footer_catalog">Каталог</h4>
          <ul class="space-y-2 text-xs text-neutral-400">
            <li><a href="/catalog?category=dresses" class="hover:text-white transition" data-i18n="nav_dresses">Сукні</a></li>
            <li><a href="/catalog?category=blouses" class="hover:text-white transition" data-i18n="nav_blouses">Блузи та сорочки</a></li>
            <li><a href="/catalog?category=suits" class="hover:text-white transition" data-i18n="nav_suits">Костюми та жакети</a></li>
            <li><a href="/catalog?category=outerwear" class="hover:text-white transition" data-i18n="nav_outerwear">Верхній одяг</a></li>
            <li><a href="/catalog?category=knitwear" class="hover:text-white transition" data-i18n="nav_knitwear">Трикотаж</a></li>
          </ul>
        </div>

        <div>
          <h4 class="font-medium text-sm text-neutral-200 mb-4 uppercase tracking-wider" data-i18n="footer_customers">Покупцям</h4>
          <ul class="space-y-2 text-xs text-neutral-400">
            <li><a href="/profile" class="hover:text-white transition" data-i18n="profile_title">Особистий кабінет</a></li>
            <li><a href="/cart" class="hover:text-white transition" data-i18n="nav_cart">Кошик</a></li>
            <li><a href="/checkout" class="hover:text-white transition" data-i18n="checkout_title">Оформлення замовлення</a></li>
            <li><a href="/catalog?on_sale=true" class="hover:text-white transition" data-i18n="nav_sale">Розпродаж (Sale)</a></li>
          </ul>
        </div>

        <div>
          <h4 class="font-medium text-sm text-neutral-200 mb-4 uppercase tracking-wider" data-i18n="footer_newsletter">Розсилка</h4>
          <p class="text-xs text-neutral-400 mb-4" data-i18n="footer_newsletter_desc">Отримуйте першими сповіщення про закриті розпродажі та нові колекції.</p>
          <form onsubmit="event.preventDefault(); window.Toast.success('Дякуємо за підписку!');" class="flex gap-2">
            <input type="email" placeholder="Ваш email" required class="bg-neutral-800 text-white text-xs px-3 py-2 rounded focus:outline-none flex-1 border border-neutral-700">
            <button type="submit" class="bg-[#C5A880] text-neutral-900 text-xs px-4 py-2 rounded font-semibold hover:bg-[#B3956D]" data-i18n="footer_newsletter_btn">OK</button>
          </form>
        </div>

      </div>

      <div class="pt-8 flex flex-col sm:flex-row justify-between items-center text-xs text-neutral-500 gap-4">
        <div data-i18n="footer_rights">© 2026 Female-Fabric. Всі права захищені.</div>
        <div class="flex space-x-6">
          <span data-i18n="footer_payment_methods">Оплата карткою онлайн, Apple Pay, Google Pay</span>
        </div>
      </div>
    </div>
  </footer>

  <!-- Mobile Bottom Navigation Bar -->
  <div class="mobile-nav-bar">
    <a href="/" class="flex flex-col items-center text-[10px] text-neutral-900">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>
      <span data-i18n="nav_home">Головна</span>
    </a>
    <a href="/catalog" class="flex flex-col items-center text-[10px] text-neutral-600">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg>
      <span data-i18n="nav_catalog">Каталог</span>
    </a>
    <button onclick="window.Modal.open('cart-drawer')" class="flex flex-col items-center text-[10px] text-neutral-600 relative">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
      <span class="cart-badge-count absolute -top-1 right-2 bg-neutral-900 text-white text-[9px] font-bold w-4 h-4 rounded-full items-center justify-center hidden">0</span>
      <span data-i18n="nav_cart">Кошик</span>
    </button>
    <a href="/profile" class="flex flex-col items-center text-[10px] text-neutral-600">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
      <span data-i18n="nav_profile">Профіль</span>
    </a>
  </div>

  <!-- Cart Side Drawer -->
  <div id="cart-drawer" class="drawer-overlay" onclick="if(event.target === this) window.Modal.close('cart-drawer')">
    <div class="drawer-content">
      <div class="p-4 border-b border-[#E7E2DA] flex justify-between items-center">
        <h3 class="font-serif text-xl font-semibold" data-i18n="cart_drawer_title">Кошик покупок</h3>
        <button onclick="window.Modal.close('cart-drawer')" class="text-neutral-500 hover:text-neutral-900 text-lg">✕</button>
      </div>

      <!-- Free shipping bar -->
      <div id="cart-drawer-freeship" class="p-3 bg-[#FAF8F5] border-b border-[#E7E2DA]"></div>

      <div id="cart-drawer-items" class="flex-1 overflow-y-auto p-4"></div>

      <div id="cart-drawer-empty" class="hidden p-8 text-center my-auto">
        <svg class="mx-auto text-neutral-300 mb-3" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
        <p class="text-sm text-neutral-500 mb-4" data-i18n="cart_empty">Ваш кошик порожній</p>
        <a href="/catalog" onclick="window.Modal.close('cart-drawer')" class="btn btn-primary btn-sm" data-i18n="cart_continue_shopping">Перейти до покупок</a>
      </div>

      <div id="cart-drawer-footer" class="p-4 border-t border-[#E7E2DA] bg-[#FAF8F5]">
        <div class="flex justify-between items-center mb-4 text-base font-semibold">
          <span data-i18n="cart_total">Разом:</span>
          <span id="cart-drawer-subtotal">0 ₴</span>
        </div>
        <div class="flex flex-col gap-2">
          <a href="/checkout" onclick="window.Modal.close('cart-drawer')" class="btn btn-primary w-full py-3" data-i18n="cart_checkout_btn">Оформити замовлення</a>
          <a href="/cart" onclick="window.Modal.close('cart-drawer')" class="btn btn-secondary w-full py-2 text-xs" data-i18n="cart_view_cart">Перейти до кошика</a>
        </div>
      </div>
    </div>
  </div>

  <!-- Auth Modal -->
  <div id="auth-modal" class="drawer-overlay flex items-center justify-center" onclick="if(event.target === this) window.Modal.close('auth-modal')">
    <div class="modal-dialog p-6 md:p-8 bg-white relative max-w-md w-full">
      <button onclick="window.Modal.close('auth-modal')" class="absolute top-4 right-4 text-neutral-400 hover:text-neutral-900 text-lg">✕</button>
      
      <div class="flex border-b border-[#E7E2DA] mb-6">
        <button id="auth-tab-login" class="flex-1 py-3 text-center text-sm font-semibold border-b-2 border-neutral-900 active" data-i18n="auth_login_title">Вхід</button>
        <button id="auth-tab-register" class="flex-1 py-3 text-center text-sm font-semibold text-neutral-400 border-b-2 border-transparent" data-i18n="auth_register_title">Реєстрація</button>
      </div>

      <!-- Login Form -->
      <form id="auth-form-login" class="space-y-4">
        <div>
          <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="auth_email">Email</label>
          <input type="email" id="login-email" required class="form-input text-sm" placeholder="anna@example.com">
        </div>
        <div>
          <div class="flex justify-between items-center mb-1">
            <label class="block text-xs font-medium text-neutral-700" data-i18n="auth_password">Пароль</label>
            <button type="button" onclick="promptForgotPassword()" class="text-xs text-neutral-500 hover:underline" data-i18n="auth_forgot">Забули пароль?</button>
          </div>
          <input type="password" id="login-password" required class="form-input text-sm" placeholder="••••••••">
        </div>
        <button type="submit" class="btn btn-primary w-full py-3 font-medium" data-i18n="auth_btn_login">Увійти в акаунт</button>
        <div class="text-[11px] text-neutral-400 text-center">Демо-доступ адміна: admin@female-fabric.ua / [SECURE_ADMIN_PASSWORD]</div>
      </form>

      <!-- Register Form -->
      <form id="auth-form-register" class="space-y-4 hidden">
        <div>
          <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="auth_name">Ваше ім'я</label>
          <input type="text" id="reg-name" required class="form-input text-sm" placeholder="Анна Коваленко">
        </div>
        <div>
          <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="auth_email">Email</label>
          <input type="email" id="reg-email" required class="form-input text-sm" placeholder="anna@example.com">
        </div>
        <div>
          <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="auth_phone">Телефон</label>
          <input type="tel" id="reg-phone" class="form-input text-sm" placeholder="+38 (097) 000-00-00">
        </div>
        <div>
          <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="auth_password">Пароль (мінімум 6 символів)</label>
          <input type="password" id="reg-password" required minlength="6" class="form-input text-sm" placeholder="••••••••">
        </div>
        <button type="submit" class="btn btn-primary w-full py-3 font-medium" data-i18n="auth_btn_reg">Зареєструватися</button>
      </form>
    </div>
  </div>

  <!-- Mobile Menu Drawer -->
  <div id="mobile-menu-drawer" class="drawer-overlay" onclick="if(event.target === this) window.Modal.close('mobile-menu-drawer')">
    <div class="drawer-content left">
      <div class="p-4 border-b border-[#E7E2DA] flex justify-between items-center">
        <span class="font-serif text-xl font-semibold">Меню</span>
        <button onclick="window.Modal.close('mobile-menu-drawer')" class="text-neutral-500 text-lg">✕</button>
      </div>
      <div class="p-4 space-y-4 text-base font-medium">
        <a href="/catalog" class="block py-2 border-b border-[#F0EDE8]" data-i18n="menu_all_catalog">Увесь каталог</a>
        <a href="/catalog?category=dresses" class="block py-2 border-b border-[#F0EDE8]" data-i18n="nav_dresses">Сукні</a>
        <a href="/catalog?category=blouses" class="block py-2 border-b border-[#F0EDE8]" data-i18n="nav_blouses">Блузи та сорочки</a>
        <a href="/catalog?category=suits" class="block py-2 border-b border-[#F0EDE8]" data-i18n="nav_suits">Костюми та жакети</a>
        <a href="/catalog?category=trousers" class="block py-2 border-b border-[#F0EDE8]" data-i18n="nav_trousers">Штани та джинси</a>
        <a href="/catalog?category=outerwear" class="block py-2 border-b border-[#F0EDE8]" data-i18n="nav_outerwear">Верхній одяг</a>
        <a href="/catalog?category=knitwear" class="block py-2 border-b border-[#F0EDE8]" data-i18n="nav_knitwear">Трикотаж</a>
        <a href="/catalog?on_sale=true" class="block py-2 text-rose-600 font-semibold" data-i18n="nav_sale">Розпродаж (Sale)</a>
      </div>
    </div>
  </div>

  <!-- Toast Container placeholder -->
  <div id="toast-container"></div>"""

COMMON_SCRIPTS = """  <!-- Scripts -->
  <script src="/static/js/components/toast.js"></script>
  <script src="/static/js/components/modal.js"></script>
  <script src="/static/js/api.js"></script>
  <script src="/static/js/store.js"></script>
  <script src="/static/js/app.js"></script>
  <script src="/static/js/i18n.js"></script>
  <script src="/static/js/lang-switcher.js"></script>"""

# 1. CATALOG.HTML
catalog_html = """<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Каталог жіночого одягу — Female-Fabric</title>
  <meta name="description" content="Повний каталог стильного жіночого одягу: сукні, блузи, штани, жакети, верхній одяг, трикотаж. Швидка доставка по Україні, примірка.">
  <link rel="canonical" href="http://localhost:8000/catalog">
  <meta property="og:title" content="Каталог одягу — Female-Fabric">
  <meta property="og:description" content="Обирайте сучасні сукні, костюми та верхній одяг з натуральних тканин.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="http://localhost:8000/catalog">

  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="/static/css/main.css">
</head>
<body class="bg-[#FAF8F5] text-[#1C1917] flex flex-col min-h-screen">

""" + HEADER_HTML + """

  <!-- Main Catalog Content -->
  <main class="flex-1 py-10">
    <div class="container mx-auto px-4">
      
      <!-- Breadcrumbs & Title -->
      <div class="mb-8">
        <div class="text-xs text-neutral-500 mb-2 flex items-center gap-2">
          <a href="/" class="hover:underline" data-i18n="nav_home">Головна</a>
          <span>/</span>
          <span class="text-neutral-900 font-medium" data-i18n="nav_catalog">Каталог</span>
        </div>
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div>
            <h1 id="catalog-main-title" class="font-serif text-3xl md:text-4xl font-normal" data-i18n="catalog_title">Каталог жіночого одягу</h1>
            <p id="catalog-search-title" class="text-xs text-neutral-500 mt-1 hidden"></p>
          </div>
          <div class="flex items-center gap-4">
            <span class="text-xs text-neutral-500 hidden sm:inline" data-i18n="sort_label">Сортування:</span>
            <select id="catalog-sort-select" class="form-input text-xs py-2 px-3 bg-white border border-[#E7E2DA] rounded-md focus:outline-none">
              <option value="newest" data-i18n="sort_newest">Спочатку новинки</option>
              <option value="popular" data-i18n="sort_popular">За популярністю</option>
              <option value="price_asc" data-i18n="sort_price_asc">Від дешевих до дорогих</option>
              <option value="price_desc" data-i18n="sort_price_desc">Від дорогих до дешевих</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Layout: Sidebar Filters + Products Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        
        <!-- Filters Sidebar -->
        <aside class="lg:col-span-1">
          <div class="bg-white p-6 rounded-xl border border-[#E7E2DA] sticky top-28 space-y-6">
            <div class="flex justify-between items-center border-b border-[#F0EDE8] pb-4">
              <h3 class="font-semibold text-base" data-i18n="filter_title">Фільтри</h3>
              <button onclick="resetAllFilters()" class="text-xs text-neutral-500 hover:text-neutral-900 underline" data-i18n="filter_reset">Скинути</button>
            </div>

            <!-- Categories Filter -->
            <div>
              <h4 class="text-xs font-semibold uppercase tracking-wider text-neutral-500 mb-3" data-i18n="cat_title">Категорії</h4>
              <div id="filter-categories-list" class="space-y-2"></div>
            </div>

            <!-- Price Range Filter -->
            <div class="border-t border-[#F0EDE8] pt-4">
              <h4 class="text-xs font-semibold uppercase tracking-wider text-neutral-500 mb-3" data-i18n="filter_price">Ціна, ₴</h4>
              <div class="flex items-center gap-2">
                <input type="number" id="filter-min-price" placeholder="Від" class="w-full text-xs p-2 border border-[#E7E2DA] rounded">
                <span class="text-neutral-400">-</span>
                <input type="number" id="filter-max-price" placeholder="До" class="w-full text-xs p-2 border border-[#E7E2DA] rounded">
              </div>
            </div>

            <!-- Flags (In stock / On sale) -->
            <div class="border-t border-[#F0EDE8] pt-4 space-y-2 text-sm">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" id="filter-in-stock" class="rounded text-neutral-900">
                <span data-i18n="filter_in_stock">Тільки в наявності</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" id="filter-on-sale" class="rounded text-neutral-900">
                <span class="text-rose-600 font-medium" data-i18n="filter_on_sale">Тільки зі знижкою (Sale)</span>
              </label>
            </div>

            <button onclick="applyFilters()" class="btn btn-primary w-full py-2.5 text-xs font-medium" data-i18n="filter_apply">Застосувати</button>
          </div>
        </aside>

        <!-- Products Grid Container -->
        <section class="lg:col-span-3">
          <div id="catalog-products-grid" class="grid grid-cols-2 sm:grid-cols-3 gap-4 md:gap-6">
            <!-- Dynamic Product Cards -->
          </div>

          <!-- Empty State -->
          <div id="catalog-empty-state" class="hidden py-16 text-center bg-white rounded-xl border border-[#E7E2DA]">
            <svg class="mx-auto text-neutral-300 mb-4" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
            <h3 class="text-lg font-medium mb-1" data-i18n="catalog_not_found">За вашим запитом нічого не знайдено</h3>
            <p class="text-xs text-neutral-500 mb-6" data-i18n="catalog_try_reset">Спробуйте скинути фільтри або змінити пошуковий запит</p>
            <button onclick="resetAllFilters()" class="btn btn-secondary text-xs" data-i18n="filter_reset">Скинути всі фільтри</button>
          </div>

          <!-- Pagination / Load More -->
          <div id="catalog-pagination" class="mt-12 text-center hidden">
            <button id="btn-load-more" onclick="loadMoreProducts()" class="btn btn-secondary px-8 py-3 text-xs font-medium" data-i18n="catalog_load_more">Завантажити ще</button>
          </div>
        </section>

      </div>
    </div>
  </main>

""" + FOOTER_AND_MODALS_HTML + """

""" + COMMON_SCRIPTS + """
  <script src="/static/js/pages/catalog.js"></script>
</body>
</html>
"""

# 2. PRODUCT.HTML
product_html = """<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Товар — Female-Fabric</title>
  <meta name="description" content="Купити жіночий одяг преміум якості в інтернет-магазині Female-Fabric з доставкою по Україні.">
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="/static/css/main.css">
</head>
<body class="bg-[#FAF8F5] text-[#1C1917] flex flex-col min-h-screen">

""" + HEADER_HTML + """

  <main class="flex-1 py-10">
    <div class="container mx-auto px-4 max-w-6xl">
      
      <!-- Breadcrumbs -->
      <div class="text-xs text-neutral-500 mb-6 flex items-center gap-2">
        <a href="/" class="hover:underline" data-i18n="nav_home">Головна</a>
        <span>/</span>
        <a href="/catalog" class="hover:underline" data-i18n="nav_catalog">Каталог</a>
        <span>/</span>
        <span id="product-breadcrumb-cat" class="hover:underline cursor-pointer"></span>
        <span>/</span>
        <span id="product-breadcrumb-name" class="text-neutral-900 font-medium"></span>
      </div>

      <!-- Product Details Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-10 lg:gap-14 bg-white p-6 md:p-10 rounded-2xl border border-[#E7E2DA]">
        
        <!-- Gallery -->
        <div class="space-y-4">
          <div class="aspect-[3/4] rounded-xl overflow-hidden bg-[#FAF8F5] border border-[#E7E2DA]">
            <img id="product-main-img" src="" alt="" class="w-full h-full object-cover">
          </div>
          <div id="product-thumbnails" class="flex gap-3 overflow-x-auto pb-2"></div>
        </div>

        <!-- Product Info -->
        <div class="flex flex-col justify-between space-y-6">
          <div>
            <div class="flex items-center justify-between gap-4 mb-2">
              <span id="product-category-badge" class="text-[11px] font-semibold tracking-wider uppercase text-[#C5A880]"></span>
              <span class="text-xs text-neutral-400"><span data-i18n="product_sku">Артикул:</span> <strong id="product-sku"></strong></span>
            </div>
            
            <h1 id="product-title" class="text-2xl md:text-3xl font-serif font-normal mb-4"></h1>

            <!-- Price -->
            <div class="flex items-baseline gap-3 mb-6">
              <span id="product-price" class="text-2xl md:text-3xl font-semibold text-neutral-900"></span>
              <span id="product-old-price" class="text-base text-neutral-400 line-through hidden"></span>
              <span id="product-discount-badge" class="text-xs font-semibold bg-rose-100 text-rose-600 px-2 py-0.5 rounded hidden"></span>
            </div>

            <!-- Color Selector -->
            <div class="mb-6">
              <label class="block text-xs font-semibold uppercase tracking-wider text-neutral-600 mb-2">
                <span data-i18n="product_select_color">Колір:</span> <span id="selected-color-name" class="text-neutral-900 font-normal"></span>
              </label>
              <div id="product-colors-list" class="flex gap-2"></div>
            </div>

            <!-- Size Selector -->
            <div class="mb-8">
              <div class="flex justify-between items-center mb-2">
                <label class="text-xs font-semibold uppercase tracking-wider text-neutral-600" data-i18n="product_select_size">Оберіть розмір:</label>
                <button type="button" onclick="openSizeGuide()" class="text-xs text-neutral-500 hover:underline" data-i18n="product_size_guide">Таблиця розмірів</button>
              </div>
              <div id="product-sizes-list" class="flex flex-wrap gap-2"></div>
            </div>

            <!-- Action Buttons -->
            <div class="flex gap-4 mb-8">
              <button id="btn-add-to-cart" onclick="addProductToCart()" class="btn btn-primary flex-1 py-4 text-sm font-medium" data-i18n="product_add_cart">
                Додати в кошик
              </button>
              <button id="btn-toggle-fav" onclick="toggleProductFav()" class="p-4 border border-[#E7E2DA] rounded-md hover:border-neutral-900 transition flex items-center justify-center">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
              </button>
            </div>
          </div>

          <!-- Description Accordion / Tabs -->
          <div class="border-t border-[#E7E2DA] pt-6 space-y-4 text-xs text-neutral-600 leading-relaxed">
            <div>
              <h4 class="font-semibold text-neutral-900 text-sm mb-2" data-i18n="product_desc_tab">Опис</h4>
              <p id="product-desc"></p>
            </div>
            <div class="border-t border-[#F0EDE8] pt-4">
              <h4 class="font-semibold text-neutral-900 text-sm mb-2" data-i18n="product_details_tab">Характеристики та догляд</h4>
              <ul id="product-details-list" class="space-y-1 list-disc list-inside"></ul>
            </div>
            <div class="border-t border-[#F0EDE8] pt-4">
              <h4 class="font-semibold text-neutral-900 text-sm mb-1" data-i18n="product_delivery_tab">Доставка та повернення</h4>
              <p>Безкоштовна доставка Новою Поштою від 2 500 ₴. Примірка перед покупкою. Легке повернення протягом 14 днів.</p>
            </div>
          </div>

        </div>
      </div>

      <!-- Similar Products -->
      <div class="mt-16">
        <h3 class="font-serif text-2xl mb-8" data-i18n="product_similar_title">Вам також може сподобатися</h3>
        <div id="product-similar-grid" class="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6"></div>
      </div>

    </div>
  </main>

""" + FOOTER_AND_MODALS_HTML + """

""" + COMMON_SCRIPTS + """
  <script src="/static/js/pages/product.js"></script>
</body>
</html>
"""

# 3. CART.HTML
cart_html = """<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Кошик покупок — Female-Fabric</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="/static/css/main.css">
</head>
<body class="bg-[#FAF8F5] text-[#1C1917] flex flex-col min-h-screen">

""" + HEADER_HTML + """

  <main class="flex-1 py-10">
    <div class="container mx-auto px-4 max-w-5xl">
      <h1 class="font-serif text-3xl md:text-4xl mb-8" data-i18n="cart_title_page">Кошик товарів</h1>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <!-- Cart Items List -->
        <div class="lg:col-span-2 space-y-4">
          <div id="cart-page-items" class="bg-white p-6 rounded-2xl border border-[#E7E2DA] divide-y divide-[#F0EDE8]"></div>

          <div id="cart-page-empty" class="hidden bg-white p-12 text-center rounded-2xl border border-[#E7E2DA]">
            <svg class="mx-auto text-neutral-300 mb-4" width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
            <h3 class="text-xl font-medium mb-2" data-i18n="cart_empty">Ваш кошик порожній</h3>
            <p class="text-xs text-neutral-500 mb-6" data-i18n="cart_continue_shopping">Оберіть стильні моделі з нашої нової колекції</p>
            <a href="/catalog" class="btn btn-primary" data-i18n="cart_continue_shopping">Перейти до покупок</a>
          </div>
        </div>

        <!-- Order Summary Card -->
        <div class="lg:col-span-1">
          <div class="bg-white p-6 rounded-2xl border border-[#E7E2DA] sticky top-28 space-y-4">
            <h3 class="font-semibold text-lg pb-2 border-b border-[#F0EDE8]" data-i18n="checkout_order_summary">Ваше замовлення</h3>
            
            <div class="space-y-2 text-sm text-neutral-600">
              <div class="flex justify-between">
                <span data-i18n="cart_subtotal">Сума:</span>
                <strong id="cart-subtotal-val" class="text-neutral-900">0 ₴</strong>
              </div>
              <div class="flex justify-between">
                <span data-i18n="cart_delivery">Доставка:</span>
                <span id="cart-delivery-val" class="text-neutral-900 font-medium">За тарифами перевізника</span>
              </div>
            </div>

            <div class="border-t border-[#F0EDE8] pt-4 flex justify-between items-center text-lg font-semibold">
              <span data-i18n="cart_total">Разом:</span>
              <span id="cart-total-val" class="text-neutral-900">0 ₴</span>
            </div>

            <a href="/checkout" class="btn btn-primary w-full py-3.5 text-center block" data-i18n="cart_checkout_btn">Оформити замовлення</a>
            <a href="/catalog" class="btn btn-secondary w-full py-2.5 text-xs text-center block" data-i18n="cart_continue_browsing">Продовжити покупки</a>
          </div>
        </div>

      </div>
    </div>
  </main>

""" + FOOTER_AND_MODALS_HTML + """

""" + COMMON_SCRIPTS + """
  <script src="/static/js/pages/cart.js"></script>
</body>
</html>
"""

# 4. CHECKOUT.HTML
checkout_html = """<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Оформлення замовлення — Female-Fabric</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="/static/css/main.css">
</head>
<body class="bg-[#FAF8F5] text-[#1C1917] flex flex-col min-h-screen">

""" + HEADER_HTML + """

  <main class="flex-1 py-10">
    <div class="container mx-auto px-4 max-w-5xl">
      <h1 class="font-serif text-3xl md:text-4xl mb-8" data-i18n="checkout_title">Оформлення замовлення</h1>

      <form id="checkout-form" onsubmit="submitOrder(event)" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <!-- Left: Form Fields -->
        <div class="lg:col-span-2 space-y-6">
          
          <!-- 1. Contact info -->
          <div class="bg-white p-6 rounded-2xl border border-[#E7E2DA]">
            <h3 class="font-semibold text-base mb-4" data-i18n="checkout_contact_info">1. Контактні дані</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="checkout_name">Ім'я *</label>
                <input type="text" id="order-first-name" required class="form-input text-sm" placeholder="Марія">
              </div>
              <div>
                <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="checkout_lastname">Прізвище *</label>
                <input type="text" id="order-last-name" required class="form-input text-sm" placeholder="Мельник">
              </div>
              <div>
                <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="checkout_phone">Телефон *</label>
                <input type="tel" id="order-phone" required class="form-input text-sm" placeholder="+38 (097) 123-45-67">
              </div>
              <div>
                <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="checkout_email">Email *</label>
                <input type="email" id="order-email" required class="form-input text-sm" placeholder="maria@example.com">
              </div>
            </div>
          </div>

          <!-- 2. Delivery info -->
          <div class="bg-white p-6 rounded-2xl border border-[#E7E2DA]">
            <h3 class="font-semibold text-base mb-4" data-i18n="checkout_delivery_info">2. Доставка по Україні</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="checkout_city">Місто *</label>
                <input type="text" id="order-city" required class="form-input text-sm" placeholder="Київ, Львів, Одеса..." data-i18n="checkout_city_placeholder">
              </div>

              <div>
                <label class="block text-xs font-medium text-neutral-700 mb-2">Спосіб доставки *</label>
                <div class="space-y-2">
                  <label class="flex items-center gap-3 p-3 border border-[#E7E2DA] rounded-lg cursor-pointer hover:border-neutral-900 transition">
                    <input type="radio" name="delivery_method" value="Нова Пошта (Відділення)" checked class="text-neutral-900">
                    <span class="text-sm font-medium" data-i18n="checkout_delivery_np">Нова Пошта (Відділення / Поштомат)</span>
                  </label>
                  <label class="flex items-center gap-3 p-3 border border-[#E7E2DA] rounded-lg cursor-pointer hover:border-neutral-900 transition">
                    <input type="radio" name="delivery_method" value="Нова Пошта (Кур'єр)" class="text-neutral-900">
                    <span class="text-sm font-medium" data-i18n="checkout_delivery_courier">Кур'єр Нової Пошти за адресою</span>
                  </label>
                  <label class="flex items-center gap-3 p-3 border border-[#E7E2DA] rounded-lg cursor-pointer hover:border-neutral-900 transition">
                    <input type="radio" name="delivery_method" value="Укрпошта" class="text-neutral-900">
                    <span class="text-sm font-medium" data-i18n="checkout_delivery_ukrposhta">Укрпошта Експрес</span>
                  </label>
                </div>
              </div>

              <div>
                <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="checkout_address">Адреса або № відділення *</label>
                <input type="text" id="order-address" required class="form-input text-sm" placeholder="Відділення №12 або вул. Хрещатик, 15">
              </div>
            </div>
          </div>

          <!-- 3. Payment Method -->
          <div class="bg-white p-6 rounded-2xl border border-[#E7E2DA]">
            <h3 class="font-semibold text-base mb-4" data-i18n="checkout_payment_info">3. Спосіб оплати</h3>
            <div class="space-y-2">
              <label class="flex items-center gap-3 p-3 border border-[#E7E2DA] rounded-lg cursor-pointer hover:border-neutral-900 transition">
                <input type="radio" name="payment_method" value="Карткою онлайн" checked class="text-neutral-900">
                <span class="text-sm font-medium" data-i18n="checkout_pay_online">Карткою онлайн (Visa / Mastercard / Apple Pay)</span>
              </label>
              <label class="flex items-center gap-3 p-3 border border-[#E7E2DA] rounded-lg cursor-pointer hover:border-neutral-900 transition">
                <input type="radio" name="payment_method" value="Післяплата" class="text-neutral-900">
                <span class="text-sm font-medium" data-i18n="checkout_pay_cod">Післяплата при отриманні (Нова Пошта)</span>
              </label>
            </div>
          </div>

          <!-- Notes -->
          <div class="bg-white p-6 rounded-2xl border border-[#E7E2DA]">
            <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="checkout_notes">Коментар до замовлення (необов'язково)</label>
            <textarea id="order-notes" rows="2" class="form-input text-sm" placeholder="Побажання щодо доставки, час приїзду кур'єра..."></textarea>
          </div>

        </div>

        <!-- Right: Summary -->
        <div class="lg:col-span-1">
          <div class="bg-white p-6 rounded-2xl border border-[#E7E2DA] sticky top-28 space-y-4">
            <h3 class="font-semibold text-lg pb-2 border-b border-[#F0EDE8]" data-i18n="checkout_order_summary">Ваше замовлення</h3>
            
            <div id="checkout-items-list" class="space-y-3 max-h-60 overflow-y-auto pr-1"></div>

            <div class="border-t border-[#F0EDE8] pt-4 space-y-2 text-sm text-neutral-600">
              <div class="flex justify-between">
                <span data-i18n="cart_subtotal">Сума:</span>
                <strong id="checkout-subtotal" class="text-neutral-900">0 ₴</strong>
              </div>
              <div class="flex justify-between">
                <span data-i18n="cart_delivery">Доставка:</span>
                <span id="checkout-delivery" class="text-neutral-900 font-medium">Безкоштовно</span>
              </div>
            </div>

            <div class="border-t border-[#F0EDE8] pt-4 flex justify-between items-center text-lg font-semibold">
              <span data-i18n="cart_total">Разом:</span>
              <span id="checkout-total" class="text-neutral-900">0 ₴</span>
            </div>

            <button type="submit" id="btn-submit-order" class="btn btn-primary w-full py-4 text-sm font-medium" data-i18n="checkout_submit_btn">
              Підтвердити замовлення
            </button>
          </div>
        </div>

      </form>
    </div>
  </main>

""" + FOOTER_AND_MODALS_HTML + """

""" + COMMON_SCRIPTS + """
  <script src="/static/js/pages/checkout.js"></script>
</body>
</html>
"""

# 5. PROFILE.HTML
profile_html = """<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Особистий кабінет — Female-Fabric</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="/static/css/main.css">
</head>
<body class="bg-[#FAF8F5] text-[#1C1917] flex flex-col min-h-screen">

""" + HEADER_HTML + """

  <main class="flex-1 py-10">
    <div class="container mx-auto px-4 max-w-5xl">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <h1 class="font-serif text-3xl md:text-4xl" data-i18n="profile_title">Особистий кабінет</h1>
        <button onclick="logoutUser()" class="text-xs text-rose-600 hover:underline font-medium self-start sm:self-auto" data-i18n="profile_logout">Вийти з акаунту</button>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Sidebar Navigation -->
        <aside class="lg:col-span-1 space-y-1">
          <button onclick="switchProfileTab('orders')" id="tab-btn-orders" class="w-full text-left px-4 py-3 rounded-lg text-sm font-semibold bg-neutral-900 text-white" data-i18n="profile_tab_orders">Мої замовлення</button>
          <button onclick="switchProfileTab('info')" id="tab-btn-info" class="w-full text-left px-4 py-3 rounded-lg text-sm font-medium text-neutral-600 hover:bg-[#F0EDE8]" data-i18n="profile_tab_info">Особисті дані</button>
          <button onclick="switchProfileTab('favorites')" id="tab-btn-favorites" class="w-full text-left px-4 py-3 rounded-lg text-sm font-medium text-neutral-600 hover:bg-[#F0EDE8]" data-i18n="profile_tab_fav">Обрані товари</button>
        </aside>

        <!-- Main Content Area -->
        <section class="lg:col-span-3">
          
          <!-- Orders Tab -->
          <div id="profile-tab-orders" class="bg-white p-6 md:p-8 rounded-2xl border border-[#E7E2DA] space-y-6">
            <h3 class="font-semibold text-lg border-b border-[#F0EDE8] pb-4" data-i18n="profile_tab_orders">Мої замовлення</h3>
            <div id="profile-orders-list" class="space-y-4"></div>
            <div id="profile-orders-empty" class="hidden text-center py-8 text-neutral-400 text-sm" data-i18n="profile_no_orders">У вас поки що немає оформлених замовлень</div>
          </div>

          <!-- Info Tab -->
          <div id="profile-tab-info" class="hidden bg-white p-6 md:p-8 rounded-2xl border border-[#E7E2DA] space-y-6">
            <h3 class="font-semibold text-lg border-b border-[#F0EDE8] pb-4" data-i18n="profile_tab_info">Особисті дані</h3>
            <form id="profile-info-form" onsubmit="updateProfileInfo(event)" class="space-y-4 max-w-md">
              <div>
                <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="auth_name">Ваше ім'я</label>
                <input type="text" id="prof-name" class="form-input text-sm">
              </div>
              <div>
                <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="auth_email">Email</label>
                <input type="email" id="prof-email" class="form-input text-sm" disabled>
              </div>
              <div>
                <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="auth_phone">Телефон</label>
                <input type="tel" id="prof-phone" class="form-input text-sm">
              </div>
              <button type="submit" class="btn btn-primary py-2.5 px-6 text-xs font-medium" data-i18n="profile_save_btn">Зберегти зміни</button>
            </form>
          </div>

          <!-- Favorites Tab -->
          <div id="profile-tab-favorites" class="hidden bg-white p-6 md:p-8 rounded-2xl border border-[#E7E2DA] space-y-6">
            <h3 class="font-semibold text-lg border-b border-[#F0EDE8] pb-4" data-i18n="profile_tab_fav">Обрані товари</h3>
            <div id="profile-fav-grid" class="grid grid-cols-2 sm:grid-cols-3 gap-4"></div>
            <div id="profile-fav-empty" class="hidden text-center py-8 text-neutral-400 text-sm" data-i18n="profile_no_fav">У вас поки що немає обраних товарів</div>
          </div>

        </section>
      </div>
    </div>
  </main>

""" + FOOTER_AND_MODALS_HTML + """

""" + COMMON_SCRIPTS + """
  <script src="/static/js/pages/profile.js"></script>
</body>
</html>
"""

# 6. LOGIN.HTML
login_html = """<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Вхід в акаунт — Female-Fabric</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="/static/css/main.css">
</head>
<body class="bg-[#FAF8F5] text-[#1C1917] flex flex-col min-h-screen">

""" + HEADER_HTML + """

  <main class="flex-1 py-16 flex items-center justify-center">
    <div class="container mx-auto px-4 max-w-md">
      <div class="bg-white p-8 rounded-2xl border border-[#E7E2DA] shadow-sm">
        <h1 class="font-serif text-2xl text-center mb-6" data-i18n="auth_login_title">Вхід в акаунт</h1>
        
        <form onsubmit="handleLoginPageSubmit(event)" class="space-y-4">
          <div>
            <label class="block text-xs font-medium text-neutral-700 mb-1" data-i18n="auth_email">Email</label>
            <input type="email" id="login-page-email" required class="form-input text-sm" placeholder="anna@example.com">
          </div>
          <div>
            <div class="flex justify-between items-center mb-1">
              <label class="block text-xs font-medium text-neutral-700" data-i18n="auth_password">Пароль</label>
              <button type="button" onclick="window.promptForgotPassword()" class="text-xs text-neutral-500 hover:underline" data-i18n="auth_forgot">Забули пароль?</button>
            </div>
            <input type="password" id="login-page-password" required class="form-input text-sm" placeholder="••••••••">
          </div>
          <button type="submit" class="btn btn-primary w-full py-3 text-sm font-medium" data-i18n="auth_btn_login">Увійти в акаунт</button>
        </form>

        <div class="mt-6 text-center text-xs text-neutral-500">
          <span data-i18n="auth_no_account">Немає акаунту?</span>
          <button onclick="window.Modal.open('auth-modal'); document.getElementById('auth-tab-register').click();" class="text-neutral-900 font-semibold hover:underline ml-1" data-i18n="auth_btn_reg">Зареєструватися</button>
        </div>
      </div>
    </div>
  </main>

""" + FOOTER_AND_MODALS_HTML + """

""" + COMMON_SCRIPTS + """
  <script>
    async function handleLoginPageSubmit(e) {
      e.preventDefault();
      const email = document.getElementById('login-page-email').value;
      const password = document.getElementById('login-page-password').value;
      try {
        const res = await window.API.login(email, password);
        window.Store.setUser(res.user);
        window.Toast.success('Успішний вхід!');
        window.location.href = '/profile';
      } catch (err) {
        window.Toast.error(err.message || 'Помилка входу');
      }
    }
  </script>
</body>
</html>
"""

# 7. ORDER-SUCCESS.HTML
order_success_html = """<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Замовлення оформлено — Female-Fabric</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="/static/css/main.css">
</head>
<body class="bg-[#FAF8F5] text-[#1C1917] flex flex-col min-h-screen">

""" + HEADER_HTML + """

  <main class="flex-1 py-20 flex items-center justify-center">
    <div class="container mx-auto px-4 max-w-lg text-center">
      <div class="bg-white p-8 md:p-12 rounded-3xl border border-[#E7E2DA] shadow-sm">
        
        <div class="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
        </div>

        <h1 class="font-serif text-3xl mb-3" data-i18n="success_title">Дякуємо за замовлення!</h1>
        <p class="text-sm text-neutral-600 mb-6" data-i18n="success_subtitle">Ваше замовлення успішно прийнято в обробку.</p>

        <div class="bg-[#FAF8F5] p-4 rounded-xl border border-[#E7E2DA] mb-6 inline-block">
          <span class="text-xs text-neutral-500" data-i18n="success_order_num">Номер замовлення:</span>
          <div id="success-order-id" class="font-mono text-lg font-bold text-neutral-900 mt-1">FF-2026-0001</div>
        </div>

        <p class="text-xs text-neutral-500 leading-relaxed mb-8 max-w-sm mx-auto" data-i18n="success_manager_contact">
          Наш менеджер зв'яжеться з вами найближчим часом для підтвердження деталей відправки.
        </p>

        <div class="flex flex-col sm:flex-row gap-3 justify-center">
          <a href="/" class="btn btn-primary py-3 px-6 text-xs" data-i18n="success_home_btn">Повернутися на головну</a>
          <a href="/catalog" class="btn btn-secondary py-3 px-6 text-xs" data-i18n="success_catalog_btn">Продовжити покупки</a>
        </div>

      </div>
    </div>
  </main>

""" + FOOTER_AND_MODALS_HTML + """

""" + COMMON_SCRIPTS + """
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const params = new URLSearchParams(window.location.search);
      if (params.has('order_number')) {
        document.getElementById('success-order-id').textContent = params.get('order_number');
      }
    });
  </script>
</body>
</html>
"""

# Write all templates to app/templates and public
tpl_map = {
    "catalog.html": catalog_html,
    "product.html": product_html,
    "cart.html": cart_html,
    "checkout.html": checkout_html,
    "profile.html": profile_html,
    "login.html": login_html,
    "order-success.html": order_success_html,
}

for name, content in tpl_map.items():
    (TPL_DIR / name).write_text(content, encoding="utf-8")
    (PUB_DIR / name).write_text(content, encoding="utf-8")
    print(f"[OK] Wrote template: {name}")

# Also sync index.html to public/index.html
if (TPL_DIR / "index.html").exists():
    shutil.copyfile(TPL_DIR / "index.html", PUB_DIR / "index.html")
    print("[OK] Synced index.html to public")

# Also copy static assets to public/static
if (BASE_DIR / "app" / "static").exists():
    shutil.copytree(BASE_DIR / "app" / "static", PUB_DIR / "static", dirs_exist_ok=True)
    print("[OK] Synced app/static to public/static")

print("[DONE] All templates and assets localized successfully!")

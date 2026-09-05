import json
import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\Pc\.gemini\antigravity\scratch\female-fabric")
APP_DIR = BASE_DIR / "app"
PUB_DIR = BASE_DIR / "public"

# 1. Update i18n.js
i18n_path = APP_DIR / "static" / "js" / "i18n.js"
i18n_txt = i18n_path.read_text(encoding="utf-8")

ua_wishlist = """      // Wishlist
      wishlist_drawer_title: "Список обраного",
      wishlist_empty: "Ваш список обраного порожній",
      wishlist_empty_desc: "Тисніть на сердечко на будь-якій картці товару, щоб зберегти його та повернутися пізніше.",
      wishlist_move_to_cart: "В кошик",
      wishlist_remove: "Видалити",
      cart_choose_size: "Обрати розмір",
"""

ru_wishlist = """      // Wishlist
      wishlist_drawer_title: "Список избранного",
      wishlist_empty: "Ваш список избранного пуст",
      wishlist_empty_desc: "Нажимайте на сердечко на любой карточке товара, чтобы сохранить его и вернуться позже.",
      wishlist_move_to_cart: "В корзину",
      wishlist_remove: "Удалить",
      cart_choose_size: "Выбрать размер",
"""

if "wishlist_drawer_title" not in i18n_txt:
    i18n_txt = i18n_txt.replace('cart_title_page: "Кошик товарів",', 'cart_title_page: "Кошик товарів",\n' + ua_wishlist)
    i18n_txt = i18n_txt.replace('cart_title_page: "Корзина товаров",', 'cart_title_page: "Корзина товаров",\n' + ru_wishlist)
    i18n_path.write_text(i18n_txt, encoding="utf-8")
    print("[OK] i18n.js updated with wishlist translations")

# 2. Update home.js & catalog.js button labels
home_js_path = APP_DIR / "static" / "js" / "pages" / "home.js"
home_js = home_js_path.read_text(encoding="utf-8")
home_js = home_js.replace('Вибрати розмір', "${window.I18N ? window.I18N.t('cart_choose_size') : 'Обрати розмір'}")
home_js_path.write_text(home_js, encoding="utf-8")

catalog_js_path = APP_DIR / "static" / "js" / "pages" / "catalog.js"
cat_js = catalog_js_path.read_text(encoding="utf-8")
cat_js = cat_js.replace('Вибрати розмір', "${window.I18N ? window.I18N.t('cart_choose_size') : 'Обрати розмір'}")
catalog_js_path.write_text(cat_js, encoding="utf-8")
print("[OK] Product card buttons updated with dynamic localization")

# 3. Update app.js
app_js_path = APP_DIR / "static" / "js" / "app.js"
app_js = """// Global App Logic: Header, Search, Cart Drawer, Wishlist Drawer, Navigation
document.addEventListener('DOMContentLoaded', async () => {
  // Initialize Global Store
  await window.Store.init();

  // Sticky Header Scroll Listener
  const header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 20) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  }

  // Update Cart Badges
  window.Store.on('cart:updated', (cart) => {
    const badges = document.querySelectorAll('.cart-badge-count');
    badges.forEach(b => {
      b.textContent = cart.total_quantity;
      b.style.display = cart.total_quantity > 0 ? 'inline-flex' : 'none';
    });
    renderCartDrawer(cart);
  });

  // Update Wishlist Badges
  window.Store.on('fav:updated', (favIds) => {
    const count = favIds.length;
    const badges = document.querySelectorAll('.wishlist-badge-count');
    badges.forEach(b => {
      b.textContent = count;
      b.style.display = count > 0 ? 'inline-flex' : 'none';
    });
    renderWishlistDrawer();
  });

  // Update Auth Header Controls
  window.Store.on('auth:changed', (user) => {
    updateAuthHeaderUI(user);
  });

  // Render initial States
  renderCartDrawer(window.Store.cart);
  updateAuthHeaderUI(window.Store.user);
  
  // Trigger initial badges
  const initFavCount = window.Store.favorites.size;
  document.querySelectorAll('.wishlist-badge-count').forEach(b => {
    b.textContent = initFavCount;
    b.style.display = initFavCount > 0 ? 'inline-flex' : 'none';
  });

  // Setup Global Live Search with Autocomplete
  setupLiveSearch();

  // Setup Auth Modal Tab Switchers
  setupAuthModal();
});

function updateAuthHeaderUI(user) {
  const guestBlocks = document.querySelectorAll('.auth-guest-view');
  const userBlocks = document.querySelectorAll('.auth-user-view');
  const adminLinks = document.querySelectorAll('.admin-nav-link');
  const userNameSlots = document.querySelectorAll('.user-name-slot');

  if (user) {
    guestBlocks.forEach(el => el.classList.add('hidden'));
    userBlocks.forEach(el => el.classList.remove('hidden'));
    userNameSlots.forEach(el => el.textContent = user.full_name.split(' ')[0] || user.full_name);

    if (user.role === 'admin') {
      adminLinks.forEach(el => el.classList.remove('hidden'));
    } else {
      adminLinks.forEach(el => el.classList.add('hidden'));
    }
  } else {
    guestBlocks.forEach(el => el.classList.remove('hidden'));
    userBlocks.forEach(el => el.classList.add('hidden'));
    adminLinks.forEach(el => el.classList.add('hidden'));
  }
}

// Side Cart Drawer Rendering
function renderCartDrawer(cart) {
  const container = document.getElementById('cart-drawer-items');
  const emptyState = document.getElementById('cart-drawer-empty');
  const footer = document.getElementById('cart-drawer-footer');
  const subtotalEl = document.getElementById('cart-drawer-subtotal');
  const freeShipBar = document.getElementById('cart-drawer-freeship');

  if (!container) return;

  if (!cart || !cart.items || cart.items.length === 0) {
    container.innerHTML = '';
    if (emptyState) emptyState.classList.remove('hidden');
    if (footer) footer.classList.add('hidden');
    return;
  }

  if (emptyState) emptyState.classList.add('hidden');
  if (footer) footer.classList.remove('hidden');

  if (subtotalEl) {
    subtotalEl.textContent = window.Store.formatPrice(cart.total);
  }

  if (freeShipBar) {
    const percent = Math.min(100, Math.round((cart.subtotal / cart.free_delivery_threshold) * 100));
    if (cart.amount_left_for_free_delivery > 0) {
      freeShipBar.innerHTML = `
        <div style="font-size:0.813rem; margin-bottom:4px; display:flex; justify-content:space-between;">
          <span>${window.I18N?.currentLang === 'ru' ? 'До бесплатной доставки:' : 'До безкоштовної доставки:'}</span>
          <strong>${window.Store.formatPrice(cart.amount_left_for_free_delivery)}</strong>
        </div>
        <div style="height:4px; background:#E5E0D8; border-radius:2px; overflow:hidden;">
          <div style="height:100%; width:${percent}%; background:#121212; transition:width 0.3s;"></div>
        </div>
      `;
    } else {
      freeShipBar.innerHTML = `
        <div style="font-size:0.813rem; color:#15803D; font-weight:500; display:flex; align-items:center; gap:4px;">
          ${window.I18N?.currentLang === 'ru' ? '✓ Бесплатная доставка включена!' : '✓ Безкоштовна доставка включена!'}
        </div>
      `;
    }
  }

  container.innerHTML = cart.items.map(item => `
    <div class="cart-item-row" style="display:flex; gap:12px; padding:12px 0; border-bottom:1px solid #F0EDE8;">
      <img src="${item.image_url || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=300'}" alt="${item.product_name}" style="width:70px; height:90px; object-fit:cover; border-radius:4px;">
      <div style="flex:1; display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <a href="/product/${item.product_slug}" style="font-weight:500; font-size:0.875rem; line-height:1.3; color:#121212;">${item.product_name}</a>
            <button onclick="window.removeCartItem(${item.id})" style="background:none; border:none; color:#A8A29E; cursor:pointer; padding:2px;" title="Видалити">✕</button>
          </div>
          <div style="font-size:0.75rem; color:#78716C; margin-top:2px;">
            ${item.size ? `Розмір: <strong>${item.size}</strong>` : ''} 
            ${item.color ? ` | Колір: ${item.color}` : ''}
          </div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
          <div style="display:flex; align-items:center; border:1px solid #E5E0D8; border-radius:4px; background:#FFF;">
            <button onclick="window.changeCartQty(${item.id}, ${item.quantity - 1})" style="padding:2px 8px; border:none; background:none; cursor:pointer;">-</button>
            <span style="font-size:0.813rem; padding:0 6px; font-weight:500;">${item.quantity}</span>
            <button onclick="window.changeCartQty(${item.id}, ${item.quantity + 1})" style="padding:2px 8px; border:none; background:none; cursor:pointer;">+</button>
          </div>
          <div style="font-weight:600; font-size:0.938rem;">${window.Store.formatPrice(item.total_price)}</div>
        </div>
      </div>
    </div>
  `).join('');
}

window.changeCartQty = async (itemId, newQty) => {
  try {
    const updated = await window.API.updateCartItem(itemId, newQty);
    window.Store.cart = updated;
    window.Store.emit('cart:updated', updated);
  } catch (err) {
    window.Toast.error(err.message || 'Помилка оновлення кошика');
  }
};

window.removeCartItem = async (itemId) => {
  try {
    const updated = await window.API.removeFromCart(itemId);
    window.Store.cart = updated;
    window.Store.emit('cart:updated', updated);
    window.Toast.info(window.I18N?.currentLang === 'ru' ? 'Товар удален из корзины' : 'Товар видалено з кошика');
  } catch (err) {
    window.Toast.error(err.message || 'Помилка видалення товару');
  }
};

// Wishlist Drawer Rendering & Actions
window.openWishlistDrawer = async () => {
  await renderWishlistDrawer();
  window.Modal?.open('wishlist-drawer');
};

async function renderWishlistDrawer() {
  const container = document.getElementById('wishlist-drawer-items');
  const emptyState = document.getElementById('wishlist-drawer-empty');
  if (!container) return;

  const products = await window.Store.getFavoriteProducts();

  if (!products || products.length === 0) {
    container.innerHTML = '';
    if (emptyState) emptyState.classList.remove('hidden');
    return;
  }

  if (emptyState) emptyState.classList.add('hidden');

  container.innerHTML = products.map(p => `
    <div style="display:flex; gap:12px; padding:12px 0; border-bottom:1px solid #F0EDE8; align-items:center;">
      <a href="/product/${p.slug}">
        <img src="${p.primary_image || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=200'}" alt="${p.name}" style="width:60px; height:75px; object-fit:cover; border-radius:6px;">
      </a>
      <div style="flex:1;">
        <a href="/product/${p.slug}" style="font-weight:500; font-size:0.875rem; color:#121212; display:-webkit-box; -webkit-line-clamp:1; -webkit-box-orient:vertical; overflow:hidden;">${p.name}</a>
        <div style="font-weight:700; font-size:0.875rem; margin:4px 0;">${window.Store.formatPrice(p.price)}</div>
        <div style="display:flex; gap:8px; align-items:center;">
          <a href="/product/${p.slug}" class="btn btn-primary btn-sm" style="font-size:0.75rem; padding:4px 10px;">
            ${window.I18N?.currentLang === 'ru' ? 'В корзину' : 'В кошик'}
          </a>
          <button onclick="window.removeWishlistItem(${p.id})" style="background:none; border:none; color:#DC2626; font-size:0.75rem; cursor:pointer; text-decoration:underline;">
            ${window.I18N?.currentLang === 'ru' ? 'Удалить' : 'Видалити'}
          </button>
        </div>
      </div>
    </div>
  `).join('');
}

window.removeWishlistItem = async (productId) => {
  await window.Store.toggleFavorite(productId);
  await renderWishlistDrawer();
};

// Global Live Search Setup
function setupLiveSearch() {
  const searchInputs = document.querySelectorAll('.site-search-input');
  const dropdown = document.getElementById('search-autocomplete-dropdown');
  let debounceTimeout = null;

  searchInputs.forEach(input => {
    input.addEventListener('input', (e) => {
      clearTimeout(debounceTimeout);
      const query = e.target.value.trim();

      if (!dropdown) return;

      if (query.length < 2) {
        dropdown.classList.add('hidden');
        return;
      }

      debounceTimeout = setTimeout(async () => {
        try {
          const res = await window.API.getProducts({ q: query, limit: 5 });
          dropdown.classList.remove('hidden');

          if (res.items.length === 0) {
            dropdown.innerHTML = '<div style="padding:16px; text-align:center; color:#78716C; font-size:0.875rem;">Нічого не знайдено</div>';
          } else {
            dropdown.innerHTML = `
              <div style="padding:8px 12px; font-size:0.75rem; text-transform:uppercase; color:#A8A29E; font-weight:600;">Знайдено товарів (${res.total})</div>
              ${res.items.map(p => `
                <a href="/product/${p.slug}" style="display:flex; gap:12px; align-items:center; padding:8px 12px; border-bottom:1px solid #F7F5F0; transition:background 0.2s;" onmouseover="this.style.background='#F7F5F0'" onmouseout="this.style.background='transparent'">
                  <img src="${p.primary_image}" alt="${p.name}" style="width:40px; height:50px; object-fit:cover; border-radius:4px;">
                  <div style="flex:1;">
                    <div style="font-size:0.875rem; font-weight:500; color:#121212;">${p.name}</div>
                    <div style="font-size:0.813rem; color:#78716C;">${p.category_name || ''}</div>
                  </div>
                  <div style="font-weight:600; font-size:0.875rem;">${window.Store.formatPrice(p.price)}</div>
                </a>
              `).join('')}
              <a href="/catalog?q=${encodeURIComponent(query)}" style="display:block; text-align:center; padding:10px; font-size:0.813rem; font-weight:600; color:#121212; background:#F0EDE8;">
                Показати всі результати →
              </a>
            `;
          }
        } catch (err) {
          console.error(err);
        }
      }, 300);
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const query = e.target.value.trim();
        if (query) {
          window.location.href = `/catalog?q=${encodeURIComponent(query)}`;
        }
      }
    });
  });

  document.addEventListener('click', (e) => {
    if (dropdown && !e.target.closest('.search-container')) {
      dropdown.classList.add('hidden');
    }
  });
}

// Auth Modal Logic
function setupAuthModal() {
  const loginTabBtn = document.getElementById('auth-tab-login');
  const registerTabBtn = document.getElementById('auth-tab-register');
  const loginForm = document.getElementById('auth-form-login');
  const registerForm = document.getElementById('auth-form-register');

  if (loginTabBtn && registerTabBtn) {
    loginTabBtn.addEventListener('click', () => {
      loginTabBtn.classList.add('border-neutral-900', 'text-neutral-900');
      loginTabBtn.classList.remove('border-transparent', 'text-neutral-400');
      registerTabBtn.classList.remove('border-neutral-900', 'text-neutral-900');
      registerTabBtn.classList.add('border-transparent', 'text-neutral-400');
      if (loginForm) loginForm.classList.remove('hidden');
      if (registerForm) registerForm.classList.add('hidden');
    });

    registerTabBtn.addEventListener('click', () => {
      registerTabBtn.classList.add('border-neutral-900', 'text-neutral-900');
      registerTabBtn.classList.remove('border-transparent', 'text-neutral-400');
      loginTabBtn.classList.remove('border-neutral-900', 'text-neutral-900');
      loginTabBtn.classList.add('border-transparent', 'text-neutral-400');
      if (registerForm) registerForm.classList.remove('hidden');
      if (loginForm) loginForm.classList.add('hidden');
    });
  }

  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email').value;
      const password = document.getElementById('login-password').value;
      const btn = loginForm.querySelector('button[type="submit"]');

      try {
        btn.disabled = true;
        btn.textContent = 'Вхід...';
        const res = await window.API.login({ email, password });
        window.Store.setUser(res.user);
        await window.Store.loadFavorites();
        await window.Store.refreshCart();
        window.Toast.success(`Вітаємо, ${res.user.full_name}!`);
        window.Modal?.close('auth-modal');
        if (window.location.pathname === '/login') {
          window.location.href = res.user.role === 'admin' ? '/admin' : '/profile';
        }
      } catch (err) {
        window.Toast.error(err.message || 'Помилка входу');
      } finally {
        btn.disabled = false;
        btn.textContent = 'Увійти в акаунт';
      }
    });
  }

  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const full_name = document.getElementById('reg-name').value;
      const email = document.getElementById('reg-email').value;
      const phone = document.getElementById('reg-phone')?.value || null;
      const password = document.getElementById('reg-password').value;
      const btn = registerForm.querySelector('button[type="submit"]');

      try {
        btn.disabled = true;
        btn.textContent = 'Реєстрація...';
        const res = await window.API.register({ full_name, email, phone, password });
        window.Store.setUser(res.user);
        window.Toast.success('Реєстрація успішна!');
        window.Modal?.close('auth-modal');
        if (window.location.pathname === '/login') {
          window.location.href = '/profile';
        }
      } catch (err) {
        window.Toast.error(err.message || 'Помилка реєстрації');
      } finally {
        btn.disabled = false;
        btn.textContent = 'Зареєструватися';
      }
    });
  }
}

// Demo Login Helpers
window.fillDemoLogin = (role) => {
  const emailInput = document.getElementById('login-email');
  const passInput = document.getElementById('login-password');
  if (role === 'admin') {
    if (emailInput) emailInput.value = 'admin@female-fabric.ua';
    if (passInput) passInput.value = 'wPSg*3@wQ@k)AcpU)xx4nddK';
  } else {
    if (emailInput) emailInput.value = 'user@female-fabric.ua';
    if (passInput) passInput.value = 'User123!';
  }
};

window.handleGlobalLogout = async () => {
  try {
    await window.API.logout();
    window.Store.setUser(null);
    window.Toast.info('Ви вийшли з акаунту');
    if (window.location.pathname.startsWith('/profile') || window.location.pathname.startsWith('/admin')) {
      window.location.href = '/';
    }
  } catch (e) {
    console.error(e);
  }
};
"""
app_js_path.write_text(app_js, encoding="utf-8")
print("[OK] app.js updated with full Wishlist Drawer and Demo Auth Login")

# 4. Update Header in all Templates (Spacious Auth Modal + Wishlist Drawer + Wishlist Badge)
HEADER_ACTION_OLD_SNIPPET = """        <!-- Account -->
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
        </a>"""

HEADER_ACTION_NEW_SNIPPET = """        <!-- Account (User Profile / Auth Modal) -->
        <div class="auth-guest-view">
          <button onclick="window.Modal.open('auth-modal')" class="p-2 text-neutral-800 hover:text-neutral-500 transition" title="Вхід / Реєстрація">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          </button>
        </div>
        <div class="auth-user-view hidden flex items-center space-x-2">
          <a href="/profile" class="p-2 text-neutral-800 hover:text-neutral-500 flex items-center gap-1.5 text-xs font-semibold" title="Особистий кабінет">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <span class="user-name-slot hidden lg:inline" data-i18n="nav_cabinet">Кабінет</span>
          </a>
          <a href="/admin" class="admin-nav-link hidden text-xs bg-neutral-900 text-white px-2.5 py-1 rounded font-medium hover:bg-neutral-800" data-i18n="nav_admin">Адмінка</a>
        </div>

        <!-- Wishlist (Saved Favorites with Badge) -->
        <button onclick="window.openWishlistDrawer()" class="p-2 text-neutral-800 hover:text-neutral-500 relative transition" title="Список обраного">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
          <span class="wishlist-badge-count absolute -top-1 -right-1 bg-rose-600 text-white text-[10px] font-bold w-5 h-5 rounded-full items-center justify-center hidden">0</span>
        </button>"""

SPACIOUS_AUTH_AND_WISHLIST_MODALS = """
  <!-- Wishlist Drawer -->
  <div id="wishlist-drawer" class="drawer-overlay" onclick="if(event.target === this) window.Modal.close('wishlist-drawer')">
    <div class="drawer-content p-6 flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between pb-4 border-b border-[#E7E2DA]">
          <div class="flex items-center gap-2">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="#E11D48" stroke="#E11D48" stroke-width="2"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
            <h3 class="font-serif text-xl" data-i18n="wishlist_drawer_title">Список обраного</h3>
          </div>
          <button onclick="window.Modal.close('wishlist-drawer')" class="text-neutral-500 hover:text-neutral-900 text-xl font-light">✕</button>
        </div>

        <div id="wishlist-drawer-items" class="overflow-y-auto max-h-[calc(100vh-180px)] py-4 space-y-3"></div>

        <div id="wishlist-drawer-empty" class="flex flex-col items-center justify-center text-center py-16 hidden">
          <div class="w-16 h-16 rounded-full bg-[#FAF8F5] flex items-center justify-center mb-4 text-neutral-400">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
          </div>
          <h4 class="font-serif text-lg mb-2" data-i18n="wishlist_empty">Ваш список обраного порожній</h4>
          <p class="text-xs text-neutral-500 max-w-xs mb-6" data-i18n="wishlist_empty_desc">Тисніть на сердечко на будь-якому товарі, щоб зберегти його та повернутися пізніше.</p>
          <a href="/catalog" onclick="window.Modal.close('wishlist-drawer')" class="btn btn-primary btn-sm" data-i18n="cart_continue_shopping">Перейти до каталогу</a>
        </div>
      </div>

      <div class="pt-4 border-t border-[#E7E2DA]">
        <button onclick="window.Modal.close('wishlist-drawer')" class="btn btn-secondary w-full py-2.5 text-xs font-medium">Продовжити покупки</button>
      </div>
    </div>
  </div>

  <!-- Spacious Modern Auth Modal (Вхід / Реєстрація) -->
  <div id="auth-modal" class="modal-overlay drawer-overlay flex items-center justify-center" onclick="if(event.target === this) window.Modal.close('auth-modal')">
    <div class="modal-dialog p-8 md:p-10 bg-white relative max-w-lg w-full rounded-2xl shadow-2xl border border-[#E7E2DA]">
      <button onclick="window.Modal.close('auth-modal')" class="absolute top-5 right-5 text-neutral-400 hover:text-neutral-900 text-2xl font-light">✕</button>
      
      <div class="text-center mb-6">
        <div class="font-serif text-2xl tracking-wider uppercase mb-1">Female-Fabric</div>
        <p class="text-xs text-neutral-500">Преміальний жіночий одяг та естетика стилю</p>
      </div>

      <div class="flex border-b border-[#E7E2DA] mb-6">
        <button id="auth-tab-login" class="flex-1 py-3 text-center text-sm font-semibold border-b-2 border-neutral-900 text-neutral-900 transition" data-i18n="auth_login_title">Вхід</button>
        <button id="auth-tab-register" class="flex-1 py-3 text-center text-sm font-semibold text-neutral-400 border-b-2 border-transparent hover:text-neutral-900 transition" data-i18n="auth_register_title">Реєстрація</button>
      </div>

      <!-- Quick Demo Login Bar -->
      <div class="bg-[#FAF8F5] p-3 rounded-lg border border-[#E7E2DA] mb-5 flex items-center justify-between text-xs">
        <span class="text-neutral-500 font-medium">Швидкий демо-вхід:</span>
        <div class="flex gap-2">
          <button type="button" onclick="window.fillDemoLogin('customer')" class="px-2.5 py-1 bg-white border border-[#E7E2DA] rounded font-semibold text-neutral-800 hover:bg-neutral-100 shadow-sm transition">Клієнт</button>
          <button type="button" onclick="window.fillDemoLogin('admin')" class="px-2.5 py-1 bg-neutral-900 text-white rounded font-semibold hover:bg-neutral-800 shadow-sm transition">Адмін</button>
        </div>
      </div>

      <!-- Login Form -->
      <form id="auth-form-login" class="space-y-4">
        <div>
          <label class="block text-xs font-semibold uppercase tracking-wider text-neutral-700 mb-1" data-i18n="auth_email">Email</label>
          <input type="email" id="login-email" required class="form-input w-full px-4 py-3 text-sm rounded-lg border border-[#E7E2DA] focus:border-neutral-900 focus:outline-none" placeholder="anna@example.com">
        </div>
        <div>
          <div class="flex justify-between items-center mb-1">
            <label class="block text-xs font-semibold uppercase tracking-wider text-neutral-700" data-i18n="auth_password">Пароль</label>
            <button type="button" onclick="promptForgotPassword()" class="text-xs text-neutral-500 hover:underline" data-i18n="auth_forgot">Забули пароль?</button>
          </div>
          <input type="password" id="login-password" required class="form-input w-full px-4 py-3 text-sm rounded-lg border border-[#E7E2DA] focus:border-neutral-900 focus:outline-none" placeholder="••••••••">
        </div>
        <button type="submit" class="btn btn-primary w-full py-3.5 font-semibold text-sm rounded-lg shadow-sm mt-2" data-i18n="auth_btn_login">Увійти в акаунт</button>
      </form>

      <!-- Register Form -->
      <form id="auth-form-register" class="space-y-4 hidden">
        <div>
          <label class="block text-xs font-semibold uppercase tracking-wider text-neutral-700 mb-1" data-i18n="auth_name">Ваше ім'я</label>
          <input type="text" id="reg-name" required class="form-input w-full px-4 py-3 text-sm rounded-lg border border-[#E7E2DA] focus:border-neutral-900 focus:outline-none" placeholder="Олена Мельник">
        </div>
        <div>
          <label class="block text-xs font-semibold uppercase tracking-wider text-neutral-700 mb-1" data-i18n="auth_email">Email</label>
          <input type="email" id="reg-email" required class="form-input w-full px-4 py-3 text-sm rounded-lg border border-[#E7E2DA] focus:border-neutral-900 focus:outline-none" placeholder="olena@example.com">
        </div>
        <div>
          <label class="block text-xs font-semibold uppercase tracking-wider text-neutral-700 mb-1" data-i18n="auth_phone">Телефон</label>
          <input type="tel" id="reg-phone" class="form-input w-full px-4 py-3 text-sm rounded-lg border border-[#E7E2DA] focus:border-neutral-900 focus:outline-none" placeholder="+38 (097) 123-45-67">
        </div>
        <div>
          <label class="block text-xs font-semibold uppercase tracking-wider text-neutral-700 mb-1" data-i18n="auth_password">Пароль (мінімум 6 символів)</label>
          <input type="password" id="reg-password" required minlength="6" class="form-input w-full px-4 py-3 text-sm rounded-lg border border-[#E7E2DA] focus:border-neutral-900 focus:outline-none" placeholder="••••••••">
        </div>
        <button type="submit" class="btn btn-primary w-full py-3.5 font-semibold text-sm rounded-lg shadow-sm mt-2" data-i18n="auth_btn_reg">Зареєструватися</button>
      </form>
    </div>
  </div>
"""

for tpl_path in (APP_DIR / "templates").glob("*.html"):
    content = tpl_path.read_text(encoding="utf-8")
    
    # Replace header action snippet
    if HEADER_ACTION_OLD_SNIPPET in content:
        content = content.replace(HEADER_ACTION_OLD_SNIPPET, HEADER_ACTION_NEW_SNIPPET)
    elif "<!-- Wishlist -->" in content and "wishlist-badge-count" not in content:
        content = content.replace(
            '<a href="/profile" class="p-2 text-neutral-800 hover:text-neutral-500 relative" title="Обране">\n          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>\n        </a>',
            """<button onclick="window.openWishlistDrawer()" class="p-2 text-neutral-800 hover:text-neutral-500 relative transition" title="Список обраного">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
          <span class="wishlist-badge-count absolute -top-1 -right-1 bg-rose-600 text-white text-[10px] font-bold w-5 h-5 rounded-full items-center justify-center hidden">0</span>
        </button>"""
        )

    # Replace auth modal with spacious auth & wishlist drawers
    if '<div id="auth-modal"' in content:
        # Find auth-modal block and replace
        start_idx = content.find('<!-- Auth Modal -->')
        if start_idx == -1:
            start_idx = content.find('<div id="auth-modal"')
        end_idx = content.find('<!-- Mobile Menu Drawer -->')
        if end_idx == -1:
            end_idx = content.find('<div id="mobile-menu-drawer"')
        
        if start_idx != -1 and end_idx != -1:
            content = content[:start_idx] + SPACIOUS_AUTH_AND_WISHLIST_MODALS + "\n  " + content[end_idx:]
    elif "</body>" in content and "wishlist-drawer" not in content:
        content = content.replace("</body>", SPACIOUS_AUTH_AND_WISHLIST_MODALS + "\n</body>")

    tpl_path.write_text(content, encoding="utf-8")

print("[OK] All templates updated with Spacious Auth Modal, Wishlist Drawer, and Wishlist Badges")

# 5. Mirror to public/
for f in (APP_DIR / "templates").glob("*.html"):
    shutil.copyfile(f, PUB_DIR / f.name)
shutil.copytree(APP_DIR / "static", PUB_DIR / "static", dirs_exist_ok=True)
print("[OK] Synchronized all templates and assets to public/")

print("[SUCCESS] Build full features complete!")

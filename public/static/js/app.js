// Global App Logic: Header, Search, Cart Drawer, Wishlist Drawer, Navigation
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
    try {
      if (cart && cart.items && cart.items.length > 0) {
        localStorage.setItem('ff_cart_backup', JSON.stringify(cart));
      } else {
        localStorage.removeItem('ff_cart_backup');
      }
    } catch (e) {}
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
      <img src="${window.optimizeImg ? window.optimizeImg(item.image_url, 160, 75) : (item.image_url || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=160&auto=format&fit=crop&q=75')}" alt="${item.product_name}" loading="lazy" decoding="async" style="width:70px; height:90px; object-fit:cover; border-radius:4px;">
      <div style="flex:1; display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <a href="/product/${item.product_slug}" style="font-weight:500; font-size:0.875rem; line-height:1.3; color:#121212;">${item.product_name}</a>
            <button onclick="window.removeCartItem(${item.id})" style="background:none; border:none; color:#A8A29E; cursor:pointer; padding:2px;" title="Видалити">✕</button>
          </div>
          <div style="font-size:0.75rem; color:#78716C; margin-top:2px;">
            ${item.sku ? `<span style="color:#A8A29E; font-weight:500;">Арт: ${item.sku}</span> • ` : ''}${item.size ? `Розмір: <strong>${item.size}</strong>` : ''}${item.color ? ` | Колір: ${item.color}` : ''}
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
        <img src="${window.optimizeImg ? window.optimizeImg(p.primary_image, 160, 75) : (p.primary_image || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=160&auto=format&fit=crop&q=75')}" alt="${p.name}" loading="lazy" decoding="async" style="width:60px; height:75px; object-fit:cover; border-radius:6px;">
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
                  <img src="${window.optimizeImg ? window.optimizeImg(p.primary_image, 100, 75) : p.primary_image}" alt="${p.name}" loading="lazy" decoding="async" style="width:40px; height:50px; object-fit:cover; border-radius:4px;">
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
      const email = document.getElementById('login-email').value.trim();
      const password = document.getElementById('login-password').value;
      const btn = loginForm.querySelector('button[type="submit"]');

      try {
        btn.disabled = true;
        btn.textContent = 'Вхід...';

        let userObj = null;
        if (window.SupabaseAuth && window.SupabaseAuth.isConfigured()) {
          const data = await window.SupabaseAuth.signIn(email, password);
          if (data && data.user) {
            userObj = {
              id: data.user.id,
              email: data.user.email,
              full_name: data.user.user_metadata?.full_name || data.user.email.split('@')[0],
              phone: data.user.user_metadata?.phone || '',
              role: 'customer'
            };
            if (data.session) {
              window.API.setToken(data.session.access_token);
            }
          }
        } else {
          const res = await window.API.login({ email, password });
          userObj = res.user;
        }

        if (userObj) {
          window.Store.setUser(userObj);
          await window.Store.loadFavorites();
          await window.Store.refreshCart();
          window.Toast.success(`Вітаємо, ${userObj.full_name}!`);
          window.Modal?.close('auth-modal');
          if (window.location.pathname === '/login') {
            window.location.href = userObj.role === 'admin' ? '/admin' : '/profile';
          }
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
      const full_name = document.getElementById('reg-name').value.trim();
      const email = document.getElementById('reg-email').value.trim();
      const phone = document.getElementById('reg-phone')?.value.trim() || null;
      const password = document.getElementById('reg-password').value;
      const btn = registerForm.querySelector('button[type="submit"]');

      try {
        btn.disabled = true;
        btn.textContent = 'Реєстрація...';

        let userObj = null;
        if (window.SupabaseAuth && window.SupabaseAuth.isConfigured()) {
          const data = await window.SupabaseAuth.signUp(email, password, { full_name, phone });
          if (data && data.user) {
            userObj = {
              id: data.user.id,
              email: data.user.email,
              full_name: full_name || data.user.email.split('@')[0],
              phone: phone || '',
              role: 'customer'
            };
            if (data.session) {
              window.API.setToken(data.session.access_token);
              window.Store.setUser(userObj);
              window.Toast.success('Вітаємо! Реєстрація успішна.');
              window.Modal?.close('auth-modal');
              if (window.location.pathname === '/login') {
                window.location.href = '/profile';
              }
            } else {
              // Confirm email is enabled in Supabase
              window.Toast.info('Акаунт створено! Перевірте пошту та перейдіть за посиланням для активації акаунту перед входом.');
              // Switch modal to login tab
              document.getElementById('auth-tab-login')?.click();
            }
          }
        } else {
          const res = await window.API.register({ full_name, email, phone, password });
          userObj = res.user;
          window.Store.setUser(userObj);
          window.Toast.success('Реєстрація успішна!');
          window.Modal?.close('auth-modal');
          if (window.location.pathname === '/login') {
            window.location.href = '/profile';
          }
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

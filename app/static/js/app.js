// Global App Logic: Header, Search, Cart Drawer, Navigation
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

  // Update Auth Header Controls
  window.Store.on('auth:changed', (user) => {
    updateAuthHeaderUI(user);
  });

  // Render initial Cart Drawer & Auth UI
  renderCartDrawer(window.Store.cart);
  updateAuthHeaderUI(window.Store.user);

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

  // Free shipping progress bar
  if (freeShipBar) {
    const percent = Math.min(100, Math.round((cart.subtotal / cart.free_delivery_threshold) * 100));
    if (cart.amount_left_for_free_delivery > 0) {
      freeShipBar.innerHTML = `
        <div style="font-size:0.813rem; margin-bottom:4px; display:flex; justify-content:space-between;">
          <span>До бесплатной доставки:</span>
          <strong>${window.Store.formatPrice(cart.amount_left_for_free_delivery)}</strong>
        </div>
        <div style="height:4px; background:#E5E0D8; border-radius:2px; overflow:hidden;">
          <div style="height:100%; width:${percent}%; background:#121212; transition:width 0.3s;"></div>
        </div>
      `;
    } else {
      freeShipBar.innerHTML = `
        <div style="font-size:0.813rem; color:#15803D; font-weight:500; display:flex; align-items:center; gap:4px;">
          ✓ Бесплатная доставка включена!
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
            <button onclick="window.removeCartItem(${item.id})" style="background:none; border:none; color:#A8A29E; cursor:pointer; padding:2px;" title="Удалить">✕</button>
          </div>
          <div style="font-size:0.75rem; color:#78716C; margin-top:2px;">
            ${item.size ? `Размер: <strong>${item.size}</strong>` : ''} 
            ${item.color ? ` | Цвет: ${item.color}` : ''}
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
    window.Toast.error(err.message || 'Ошибка обновления корзины');
  }
};

window.removeCartItem = async (itemId) => {
  try {
    const updated = await window.API.removeFromCart(itemId);
    window.Store.cart = updated;
    window.Store.emit('cart:updated', updated);
    window.Toast.info('Товар удален из корзины');
  } catch (err) {
    window.Toast.error(err.message || 'Ошибка удаления');
  }
};

// Live Search with Autocomplete
function setupLiveSearch() {
  const searchInputs = document.querySelectorAll('.site-search-input');
  const dropdown = document.getElementById('search-autocomplete-dropdown');
  let debounceTimeout = null;

  searchInputs.forEach(input => {
    input.addEventListener('input', (e) => {
      clearTimeout(debounceTimeout);
      const query = e.target.value.trim();

      if (query.length < 2) {
        if (dropdown) dropdown.classList.add('hidden');
        return;
      }

      debounceTimeout = setTimeout(async () => {
        try {
          const res = await window.API.getProducts({ q: query, limit: 5 });
          if (!dropdown) return;

          if (res.items.length === 0) {
            dropdown.innerHTML = '<div style="padding:16px; text-align:center; color:#78716C; font-size:0.875rem;">Ничего не найдено</div>';
          } else {
            dropdown.innerHTML = `
              <div style="padding:8px 12px; font-size:0.75rem; text-transform:uppercase; color:#A8A29E; font-weight:600;">Найдено товаров (${res.total})</div>
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
                Показать все результаты (${res.total}) →
              </a>
            `;
          }
          dropdown.classList.remove('hidden');
        } catch (e) {
          console.error(e);
        }
      }, 250);
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

  // Close dropdown on click outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-container') && dropdown) {
      dropdown.classList.add('hidden');
    }
  });
}

// Auth modal tabs & form handlers
function setupAuthModal() {
  const loginTabBtn = document.getElementById('auth-tab-login');
  const registerTabBtn = document.getElementById('auth-tab-register');
  const loginForm = document.getElementById('auth-form-login');
  const registerForm = document.getElementById('auth-form-register');

  if (loginTabBtn && registerTabBtn) {
    loginTabBtn.addEventListener('click', () => {
      loginTabBtn.classList.add('active');
      registerTabBtn.classList.remove('active');
      loginForm.classList.remove('hidden');
      registerForm.classList.add('hidden');
    });

    registerTabBtn.addEventListener('click', () => {
      registerTabBtn.classList.add('active');
      loginTabBtn.classList.remove('active');
      registerForm.classList.remove('hidden');
      loginForm.classList.add('hidden');
    });
  }

  // Handle Login Submit
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email').value;
      const password = document.getElementById('login-password').value;
      const btn = loginForm.querySelector('button[type="submit"]');

      try {
        btn.disabled = true;
        btn.textContent = 'Вход...';
        const res = await window.API.login({ email, password });
        window.Store.setUser(res.user);
        await window.Store.refreshCart();
        await window.Store.loadFavorites();
        window.Toast.success(`Добро пожаловать, ${res.user.full_name}!`);
        window.Modal?.close('auth-modal');
        if (window.location.pathname === '/login') {
          window.location.href = res.user.role === 'admin' ? '/admin' : '/profile';
        }
      } catch (err) {
        window.Toast.error(err.message || 'Ошибка входа');
      } finally {
        btn.disabled = false;
        btn.textContent = 'Войти в аккаунт';
      }
    });
  }

  // Handle Register Submit
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
        btn.textContent = 'Регистрация...';
        const res = await window.API.register({ full_name, email, phone, password });
        window.Store.setUser(res.user);
        await window.Store.refreshCart();
        window.Toast.success('Регистрация прошла успешно!');
        window.Modal?.close('auth-modal');
        if (window.location.pathname === '/login') {
          window.location.href = '/profile';
        }
      } catch (err) {
        window.Toast.error(err.message || 'Ошибка регистрации');
      } finally {
        btn.disabled = false;
        btn.textContent = 'Зарегистрироваться';
      }
    });
  }
}

window.handleGlobalLogout = async () => {
  try {
    await window.API.logout();
    window.Store.setUser(null);
    await window.Store.refreshCart();
    window.Toast.info('Вы вышли из системы');
    if (window.location.pathname.startsWith('/admin') || window.location.pathname.startsWith('/profile')) {
      window.location.href = '/';
    }
  } catch (err) {
    window.Toast.error(err.message || 'Ошибка выхода');
  }
};

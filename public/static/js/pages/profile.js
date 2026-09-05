// User Profile Page JavaScript
document.addEventListener('DOMContentLoaded', async () => {
  // Give Store and Supabase a moment to initialize session
  if (window.Store && !window.Store.user) {
    if (window.SupabaseAuth && window.SupabaseAuth.isConfigured()) {
      try {
        const session = await window.SupabaseAuth.getSession();
        if (session?.user) {
          const u = session.user;
          window.Store.setUser({
            id: u.id,
            email: u.email,
            full_name: u.user_metadata?.full_name || u.email.split('@')[0],
            phone: u.user_metadata?.phone || '',
            role: 'customer'
          });
          window.API.setToken(session.access_token);
        }
      } catch(e) {}
    }
  }

  const token = window.API.getToken();
  const user = window.Store?.user;
  if (!token && !user) {
    window.location.href = '/login';
    return;
  }

  await loadUserProfile();
  await loadUserOrders();
  await loadUserFavorites();
});

// Tab Switcher
window.switchProfileTab = (tabName) => {
  const tabs = ['orders', 'info', 'favorites'];
  tabs.forEach(t => {
    const btn = document.getElementById(`tab-btn-${t}`);
    const pane = document.getElementById(`profile-tab-${t}`);
    if (btn) {
      if (t === tabName) {
        btn.classList.add('bg-neutral-900', 'text-white', 'font-semibold');
        btn.classList.remove('text-neutral-600', 'hover:bg-[#F0EDE8]', 'font-medium');
      } else {
        btn.classList.remove('bg-neutral-900', 'text-white', 'font-semibold');
        btn.classList.add('text-neutral-600', 'hover:bg-[#F0EDE8]', 'font-medium');
      }
    }
    if (pane) {
      if (t === tabName) {
        pane.classList.remove('hidden');
      } else {
        pane.classList.add('hidden');
      }
    }
  });

  if (tabName === 'favorites') {
    loadUserFavorites();
  }
};

// Load and populate user profile
async function loadUserProfile() {
  let currentUser = window.Store?.user;

  // Try fetching fresh profile from API
  try {
    const apiUser = await window.API.getProfile();
    if (apiUser) {
      currentUser = { ...currentUser, ...apiUser };
      window.Store?.setUser(currentUser);
    }
  } catch (e) {
    // If backend 401 or offline, fallback to Supabase user
    if (window.SupabaseAuth && window.SupabaseAuth.isConfigured()) {
      try {
        const sbUser = await window.SupabaseAuth.getUser();
        if (sbUser) {
          currentUser = {
            id: sbUser.id,
            email: sbUser.email,
            full_name: sbUser.user_metadata?.full_name || sbUser.email.split('@')[0],
            phone: sbUser.user_metadata?.phone || '',
            role: 'customer'
          };
          window.Store?.setUser(currentUser);
        }
      } catch (err) {}
    }
  }

  if (!currentUser) return;

  const nameInput = document.getElementById('prof-name');
  const emailInput = document.getElementById('prof-email');
  const phoneInput = document.getElementById('prof-phone');
  const welcomeText = document.getElementById('profile-welcome-text');

  if (nameInput) nameInput.value = currentUser.full_name || '';
  if (emailInput) emailInput.value = currentUser.email || '';
  if (phoneInput) phoneInput.value = currentUser.phone || '';

  if (welcomeText && currentUser.full_name) {
    welcomeText.textContent = `Вітаємо, ${currentUser.full_name}! Раді бачити вас знову.`;
  }
}

// Update profile info (Name, Phone)
window.updateProfileInfo = async (e) => {
  e.preventDefault();
  const form = e.target;
  const btn = form.querySelector('button[type="submit"]');
  const newName = document.getElementById('prof-name')?.value.trim();
  const newPhone = document.getElementById('prof-phone')?.value.trim();

  try {
    if (btn) {
      btn.disabled = true;
      btn.textContent = 'Збереження...';
    }

    // 1. Update in Supabase Auth if configured
    if (window.supabaseClient) {
      const { data, error } = await window.supabaseClient.auth.updateUser({
        data: {
          full_name: newName,
          phone: newPhone
        }
      });
      if (error) throw error;
    }

    // 2. Update via Backend API if available
    try {
      await window.API.updateProfile({ full_name: newName, phone: newPhone });
    } catch (apiErr) {
      console.warn('Backend profile update note:', apiErr.message);
    }

    // 3. Update Store and Local State
    const updatedUser = {
      ...(window.Store?.user || {}),
      full_name: newName,
      phone: newPhone
    };
    window.Store?.setUser(updatedUser);

    const welcomeText = document.getElementById('profile-welcome-text');
    if (welcomeText && newName) {
      welcomeText.textContent = `Вітаємо, ${newName}! Раді бачити вас знову.`;
    }

    window.Toast.success('Дані успішно оновлено!');
  } catch (err) {
    window.Toast.error(err.message || 'Помилка оновлення даних');
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = 'Зберегти зміни';
    }
  }
};

// Load and render user orders with total spent calculation
async function loadUserOrders() {
  const container = document.getElementById('profile-orders-list');
  const emptyEl = document.getElementById('profile-orders-empty');
  const countStatEl = document.getElementById('profile-stat-orders-count');
  const totalStatEl = document.getElementById('profile-stat-total-spent');

  if (!container) return;

  let allOrders = [];
  const currentUser = window.Store?.user;
  const userEmail = (currentUser?.email || '').toLowerCase();

  // 1. Fetch from Backend API
  try {
    const apiOrders = await window.API.getOrders();
    if (Array.isArray(apiOrders)) {
      allOrders = apiOrders;
    }
  } catch (e) {
    console.warn('Backend orders fetch note:', e.message);
  }

  // 2. Merge with LocalStorage order history backup
  if (userEmail) {
    try {
      const localOrders = JSON.parse(localStorage.getItem('ff_orders_' + userEmail) || '[]');
      if (Array.isArray(localOrders) && localOrders.length > 0) {
        const existingNums = new Set(allOrders.map(o => o.order_number));
        localOrders.forEach(lo => {
          if (!existingNums.has(lo.order_number)) {
            allOrders.push(lo);
          }
        });
      }
    } catch(e) {}
  }

  // Calculate statistics (Total Orders & Total Spent)
  const totalOrdersCount = allOrders.length;
  const paidOrders = allOrders.filter(o => o.status !== 'Отменён' && o.status !== 'Скасовано');
  const totalSpent = paidOrders.reduce((sum, o) => sum + (Number(o.total_amount) || 0), 0);

  if (countStatEl) countStatEl.textContent = totalOrdersCount;
  if (totalStatEl) totalStatEl.textContent = window.Store ? window.Store.formatPrice(totalSpent) : `${totalSpent} ₴`;

  if (allOrders.length === 0) {
    container.innerHTML = '';
    if (emptyEl) emptyEl.classList.remove('hidden');
    return;
  }

  if (emptyEl) emptyEl.classList.add('hidden');

  // Format date helper
  const formatDate = (dateStr) => {
    try {
      const d = new Date(dateStr);
      return d.toLocaleDateString('uk-UA', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' });
    } catch(e) {
      return dateStr || '';
    }
  };

  // Status badge colors
  const getStatusBadge = (status) => {
    const s = (status || 'Новий').toLowerCase();
    if (s.includes('доставлен') || s.includes('виконан')) {
      return '<span class="px-2.5 py-1 bg-emerald-50 text-emerald-700 rounded-full text-xs font-semibold border border-emerald-200">Доставлено</span>';
    }
    if (s.includes('відправлен') || s.includes('отправлен')) {
      return '<span class="px-2.5 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-semibold border border-blue-200">Відправлено</span>';
    }
    if (s.includes('підтверд') || s.includes('подтвержд')) {
      return '<span class="px-2.5 py-1 bg-amber-50 text-amber-700 rounded-full text-xs font-semibold border border-amber-200">Підтверджено</span>';
    }
    if (s.includes('скас') || s.includes('отмен')) {
      return '<span class="px-2.5 py-1 bg-rose-50 text-rose-700 rounded-full text-xs font-semibold border border-rose-200">Скасовано</span>';
    }
    return '<span class="px-2.5 py-1 bg-neutral-100 text-neutral-800 rounded-full text-xs font-semibold border border-neutral-200">В обробці</span>';
  };

  container.innerHTML = allOrders.map(order => `
    <div class="bg-white rounded-xl border border-[#E7E2DA] p-5 shadow-sm space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-[#F0EDE8] pb-3">
        <div>
          <span class="font-mono font-semibold text-sm text-neutral-900">Замовлення #${order.order_number}</span>
          <div class="text-xs text-neutral-500 mt-0.5">${formatDate(order.created_at)}</div>
        </div>
        <div class="flex items-center gap-3">
          ${getStatusBadge(order.status)}
          <span class="font-serif font-bold text-lg text-neutral-900">${window.Store ? window.Store.formatPrice(order.total_amount) : `${order.total_amount} ₴`}</span>
        </div>
      </div>

      <!-- Items List -->
      <div class="space-y-3 pt-1">
        ${(order.items || []).map(it => `
          <div class="flex items-center justify-between gap-4 text-xs">
            <div class="flex items-center gap-3">
              <img src="${window.optimizeImg ? window.optimizeImg(it.image_url, 120, 75) : (it.image_url || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=120&auto=format&fit=crop&q=75')}" alt="${it.product_name}" loading="lazy" decoding="async" class="w-12 h-14 object-cover rounded-md border border-[#E7E2DA]">
              <div>
                <div class="font-medium text-neutral-900 text-sm">${it.product_name}</div>
                <div class="text-neutral-500 mt-0.5">
                  ${it.sku ? `<span class="text-neutral-400">Арт: ${it.sku}</span> • ` : ''}
                  ${it.size ? `Розмір: <strong>${it.size}</strong>` : ''}
                  ${it.color ? ` • Колір: ${it.color}` : ''} • ${it.quantity} шт.
                </div>
              </div>
            </div>
            <div class="font-semibold text-neutral-900">${window.Store ? window.Store.formatPrice(it.total_price || (it.price * it.quantity)) : `${it.price} ₴`}</div>
          </div>
        `).join('')}
      </div>

      <!-- Delivery & Payment Info -->
      <div class="pt-3 border-t border-[#F0EDE8] flex flex-wrap justify-between text-xs text-neutral-500 gap-2">
        <div><strong>Доставка:</strong> ${order.delivery_method || 'Нова Пошта'} ${order.city ? `(${order.city}, ${order.address})` : ''}</div>
        <div><strong>Оплата:</strong> ${order.payment_method || 'Карткою онлайн'}</div>
      </div>
    </div>
  `).join('');
}

// Load and render user favorites
async function loadUserFavorites() {
  const container = document.getElementById('profile-fav-grid');
  const emptyEl = document.getElementById('profile-fav-empty');
  if (!container) return;

  try {
    const products = await window.Store?.getFavoriteProducts();
    if (!products || products.length === 0) {
      container.innerHTML = '';
      if (emptyEl) emptyEl.classList.remove('hidden');
      return;
    }

    if (emptyEl) emptyEl.classList.add('hidden');

    container.innerHTML = products.map(p => `
      <div class="product-card bg-white rounded-xl border border-[#E7E2DA] overflow-hidden flex flex-col relative">
        <button onclick="window.Store.toggleFavorite(${p.id}).then(() => loadUserFavorites())" class="absolute top-2 right-2 bg-white/90 rounded-full w-7 h-7 flex items-center justify-center text-xs shadow-sm hover:bg-white z-10" title="Видалити">✕</button>
        <a href="/product/${p.slug}" class="block h-48 overflow-hidden bg-[#FAF8F5]">
          <img src="${window.optimizeImg ? window.optimizeImg(p.primary_image, 400, 75) : p.primary_image}" alt="${p.name}" loading="lazy" decoding="async" class="w-full h-full object-cover">
        </a>
        <div class="p-3 flex-1 flex flex-col justify-between">
          <div>
            <a href="/product/${p.slug}" class="font-medium text-xs text-neutral-900 block mb-1 line-clamp-1 hover:underline">${p.name}</a>
            <div class="font-bold text-sm text-neutral-900 mb-2">${window.Store ? window.Store.formatPrice(p.price) : `${p.price} ₴`}</div>
          </div>
          <a href="/product/${p.slug}" class="btn btn-primary btn-sm w-full py-1.5 text-xs text-center block">Купити</a>
        </div>
      </div>
    `).join('');
  } catch(e) {
    console.error('Favorites load error:', e);
  }
}

// Global logout helper for profile page
window.logoutUser = async () => {
  if (window.SupabaseAuth) {
    await window.SupabaseAuth.signOut();
  }
  window.API.setToken(null);
  window.Store?.setUser(null);
  window.location.href = '/';
};

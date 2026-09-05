// User Profile Page JavaScript
document.addEventListener('DOMContentLoaded', async () => {
  const token = window.API.getToken();
  if (!token) {
    window.location.href = '/login';
    return;
  }

  await loadUserProfile();
  await loadUserOrders();
  await loadUserAddresses();
  await loadUserFavorites();

  setupProfileTabs();
  setupProfileFormHandlers();
});

function setupProfileTabs() {
  const tabs = document.querySelectorAll('.profile-tab-btn');
  const panes = document.querySelectorAll('.profile-tab-pane');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active', 'border-black', 'text-black'));
      panes.forEach(p => p.classList.add('hidden'));

      tab.classList.add('active', 'border-black', 'text-black');
      const targetPane = document.getElementById(tab.dataset.tab);
      if (targetPane) targetPane.classList.remove('hidden');
    });
  });
}

async function loadUserProfile() {
  try {
    const user = await window.API.getProfile();
    document.getElementById('profile-name-header').textContent = user.full_name;
    document.getElementById('profile-email-header').textContent = user.email;

    document.getElementById('edit-full-name').value = user.full_name;
    document.getElementById('edit-email').value = user.email;
    document.getElementById('edit-phone').value = user.phone || '';
  } catch (e) {
    console.error(e);
  }
}

async function loadUserOrders() {
  const container = document.getElementById('profile-orders-list');
  if (!container) return;

  try {
    const orders = await window.API.getOrders();
    if (orders.length === 0) {
      container.innerHTML = `
        <div style="text-align:center; padding:40px; background:#FFF; border-radius:12px; border:1px solid #E5E0D8;">
          <p style="color:#78716C; margin-bottom:16px;">У вас поки немає замовлень</p>
          <a href="/catalog" class="btn btn-primary btn-sm">Перейти до покупок</a>
        </div>
      `;
      return;
    }

    container.innerHTML = orders.map(order => {
      let statusColor = '#2563EB';
      if (order.status === 'Новый') statusColor = '#0284C7';
      else if (order.status === 'Подтверждён') statusColor = '#0D9488';
      else if (order.status === 'Собирается') statusColor = '#D97706';
      else if (order.status === 'Отправлен') statusColor = '#7C3AED';
      else if (order.status === 'Доставлен') statusColor = '#16A34A';
      else if (order.status === 'Отменён') statusColor = '#DC2626';

      const dateStr = new Date(order.created_at).toLocaleDateString('uk-UA', { day: 'numeric', month: 'long', year: 'numeric' });

      return `
        <div style="background:#FFF; border-radius:12px; border:1px solid #E5E0D8; padding:20px; margin-bottom:16px;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px; border-bottom:1px solid #F0EDE8; padding-bottom:12px; flex-wrap:wrap; gap:8px;">
            <div>
              <div style="font-weight:700; font-size:1.125rem;">Замовлення ${order.order_number}</div>
              <div style="font-size:0.813rem; color:#78716C;">від ${dateStr}</div>
            </div>
            <div style="text-align:right;">
              <span style="background:${statusColor}15; color:${statusColor}; font-weight:600; font-size:0.813rem; padding:4px 10px; border-radius:6px; display:inline-block; margin-bottom:4px;">
                ${order.status}
              </span>
              <div style="font-weight:700; font-size:1.063rem;">${window.Store.formatPrice(order.total_amount)}</div>
            </div>
          </div>

          <div style="margin-bottom:16px;">
            ${order.items.map(it => `
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; font-size:0.875rem;">
                <div style="display:flex; gap:10px; align-items:center;">
                  <img src="${window.optimizeImg ? window.optimizeImg(it.image_url, 120, 75) : (it.image_url || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=120&auto=format&fit=crop&q=75')}" alt="${it.product_name}" loading="lazy" decoding="async" style="width:36px; height:46px; object-fit:cover; border-radius:4px;">
                  <div>
                    <div style="font-weight:500;">${it.product_name}</div>
                    <div style="color:#78716C; font-size:0.75rem;">${it.size || ''} | ${it.quantity} шт.</div>
                  </div>
                </div>
                <div>${window.Store.formatPrice(it.total_price)}</div>
              </div>
            `).join('')}
          </div>

          <div style="font-size:0.813rem; color:#78716C; background:#FAF8F5; padding:10px 14px; border-radius:6px;">
            <div><strong>Доставка:</strong> ${order.delivery_method} (${order.city}, ${order.address})</div>
            <div><strong>Оплата:</strong> ${order.payment_method} (${order.payment_status})</div>
          </div>
        </div>
      `;
    }).join('');
  } catch (e) {
    console.error(e);
  }
}

async function loadUserAddresses() {
  const container = document.getElementById('profile-addresses-list');
  if (!container) return;

  try {
    const addresses = await window.API.getAddresses();
    if (addresses.length === 0) {
      container.innerHTML = '<p style="color:#78716C;">У вас поки немає збережених адрес</p>';
      return;
    }

    container.innerHTML = addresses.map(addr => `
      <div style="background:#FFF; border-radius:12px; border:1px solid #E5E0D8; padding:16px; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-weight:600; display:flex; align-items:center; gap:8px;">
            ${addr.title}
            ${addr.is_default ? '<span style="font-size:0.688rem; background:#121212; color:#FFF; padding:2px 6px; border-radius:3px;">Основной</span>' : ''}
          </div>
          <div style="font-size:0.875rem; color:#57534E; margin-top:2px;">${addr.city}, ${addr.address}</div>
        </div>
        <button onclick="deleteAddress(${addr.id})" style="background:none; border:none; color:#DC2626; cursor:pointer; font-size:0.813rem; font-weight:500;">Удалить</button>
      </div>
    `).join('');
  } catch (e) {
    console.error(e);
  }
}

window.deleteAddress = async (id) => {
  if (!confirm('Удалить этот адрес?')) return;
  try {
    await window.API.deleteAddress(id);
    window.Toast.info('Адрес удален');
    await loadUserAddresses();
  } catch (err) {
    window.Toast.error(err.message);
  }
};

async function loadUserFavorites() {
  const container = document.getElementById('profile-favorites-list');
  if (!container) return;

  try {
    const favs = await window.API.getFavorites();
    if (favs.length === 0) {
      container.innerHTML = '<p style="color:#78716C; text-align:center; padding:30px;">В избранном пока нет товаров</p>';
      return;
    }

    container.innerHTML = favs.map(p => `
      <div class="product-card" style="background:#FFF; border-radius:12px; overflow:hidden; border:1px solid #E5E0D8; display:flex; flex-direction:column; position:relative;">
        <button onclick="window.Store.toggleFavorite(${p.id}).then(() => loadUserFavorites())" style="position:absolute; top:10px; right:10px; z-index:10; background:#FFF; border:none; border-radius:50%; width:32px; height:32px; cursor:pointer; box-shadow:0 2px 5px rgba(0,0,0,0.1);">✕</button>
        <a href="/product/${p.slug}" style="display:block; height:240px; overflow:hidden; background:#F3EFEA;">
          <img src="${window.optimizeImg ? window.optimizeImg(p.primary_image, 500, 75) : p.primary_image}" alt="${p.name}" class="img-zoom" loading="lazy" decoding="async" style="width:100%; height:100%; object-fit:cover;">
        </a>
        <div style="padding:14px; flex:1; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <a href="/product/${p.slug}" style="font-size:0.938rem; font-weight:500; color:#121212; display:block; margin-bottom:6px;">${p.name}</a>
            <div style="font-weight:700; font-size:1rem; margin-bottom:10px;">${window.Store.formatPrice(p.price)}</div>
          </div>
          <a href="/product/${p.slug}" class="btn btn-primary btn-sm" style="width:100%;">Купить</a>
        </div>
      </div>
    `).join('');
  } catch (e) {
    console.error(e);
  }
}

function setupProfileFormHandlers() {
  const profileForm = document.getElementById('profile-edit-form');
  if (profileForm) {
    profileForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const full_name = document.getElementById('edit-full-name').value.trim();
      const phone = document.getElementById('edit-phone').value.trim();
      const email = document.getElementById('edit-email').value.trim();

      try {
        const updated = await window.API.updateProfile({ full_name, phone, email });
        window.Store.setUser(updated);
        window.Toast.success('Данные сохранены');
      } catch (err) {
        window.Toast.error(err.message || 'Ошибка обновления данных');
      }
    });
  }

  const passForm = document.getElementById('profile-password-form');
  if (passForm) {
    passForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const old_password = document.getElementById('old-password').value;
      const new_password = document.getElementById('new-password').value;

      try {
        await window.API.changePassword(old_password, new_password);
        window.Toast.success('Пароль успешно изменен');
        passForm.reset();
      } catch (err) {
        window.Toast.error(err.message || 'Ошибка смены пароля');
      }
    });
  }

  const addrForm = document.getElementById('add-address-form');
  if (addrForm) {
    addrForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = document.getElementById('addr-title').value.trim();
      const city = document.getElementById('addr-city').value.trim();
      const address = document.getElementById('addr-street').value.trim();
      const is_default = document.getElementById('addr-default').checked;

      try {
        await window.API.addAddress({ title, city, address, is_default });
        window.Toast.success('Адрес успешно добавлен');
        addrForm.reset();
        window.Modal?.close('add-address-modal');
        await loadUserAddresses();
      } catch (err) {
        window.Toast.error(err.message || 'Ошибка добавления адреса');
      }
    });
  }
}

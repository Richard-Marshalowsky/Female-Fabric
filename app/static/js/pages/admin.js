// Admin Panel JavaScript
document.addEventListener('DOMContentLoaded', async () => {
  const token = window.API.getToken();
  if (!token) {
    window.location.href = '/login';
    return;
  }

  try {
    const user = await window.API.getMe();
    if (user.role !== 'admin') {
      window.Toast.error('Доступ запрещен: требуются права администратора');
      window.location.href = '/';
      return;
    }
    const nameEl = document.getElementById('admin-user-name');
    if (nameEl) nameEl.textContent = user.full_name;
  } catch (e) {
    window.location.href = '/login';
    return;
  }

  setupAdminTabs();
  await loadAdminStats();
  await loadAdminProducts();
  await loadAdminCategories();
  await loadAdminOrders();
  await loadAdminUsers();

  setupProductForm();
  setupCategoryForm();
});

function setupAdminTabs() {
  const tabBtns = document.querySelectorAll('.admin-tab-btn');
  const tabPanes = document.querySelectorAll('.admin-tab-pane');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active', 'bg-neutral-800', 'text-white'));
      tabPanes.forEach(p => p.classList.add('hidden'));

      btn.classList.add('active', 'bg-neutral-800', 'text-white');
      const target = document.getElementById(btn.dataset.tab);
      if (target) target.classList.remove('hidden');
    });
  });
}

// 1. Dashboard Stats
async function loadAdminStats() {
  try {
    const stats = await window.API.getAdminStats();
    document.getElementById('stat-total-revenue').textContent = window.Store.formatPrice(stats.total_revenue);
    document.getElementById('stat-total-orders').textContent = stats.total_orders;
    document.getElementById('stat-new-orders').textContent = stats.new_orders;
    document.getElementById('stat-total-customers').textContent = stats.total_customers;
    document.getElementById('stat-low-stock').textContent = stats.low_stock_products;

    const recentTable = document.getElementById('admin-recent-orders-table');
    if (recentTable) {
      recentTable.innerHTML = stats.recent_orders.map(o => `
        <tr style="border-bottom:1px solid #E5E0D8;">
          <td style="padding:12px; font-weight:600;">${o.order_number}</td>
          <td style="padding:12px;">${o.first_name} ${o.last_name}</td>
          <td style="padding:12px;">${window.Store.formatPrice(o.total_amount)}</td>
          <td style="padding:12px;"><span style="padding:2px 8px; border-radius:4px; font-size:0.75rem; font-weight:600; background:#F0EDE8;">${o.status}</span></td>
          <td style="padding:12px;">
            <button onclick="viewAdminOrder(${o.id})" class="btn btn-secondary btn-sm">Детали</button>
          </td>
        </tr>
      `).join('');
    }
  } catch (e) {
    console.error('Error loading admin stats:', e);
  }
}

// 2. Products Management
let adminProductsList = [];
async function loadAdminProducts() {
  const container = document.getElementById('admin-products-table-body');
  if (!container) return;

  try {
    const products = await window.API.getAdminProducts();
    adminProductsList = products;
    renderAdminProductsTable(products);
  } catch (e) {
    console.error(e);
  }
}

function renderAdminProductsTable(products) {
  const container = document.getElementById('admin-products-table-body');
  if (!container) return;

  container.innerHTML = products.map(p => `
    <tr style="border-bottom:1px solid #E5E0D8;">
      <td style="padding:12px;">
        <img src="${p.primary_image || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=200'}" style="width:48px; height:60px; object-fit:cover; border-radius:4px;">
      </td>
      <td style="padding:12px;">
        <div style="font-weight:600;">${p.name}</div>
        <div style="font-size:0.75rem; color:#78716C;">SKU: ${p.sku} | ${p.category_name}</div>
      </td>
      <td style="padding:12px; font-weight:600;">${window.Store.formatPrice(p.price)}</td>
      <td style="padding:12px;">
        <span style="font-weight:600; color:${p.total_stock < 5 ? '#DC2626' : '#16A34A'}">${p.total_stock} шт.</span>
      </td>
      <td style="padding:12px;">
        <button onclick="toggleProductActive(${p.id})" style="padding:4px 8px; border-radius:4px; font-size:0.75rem; font-weight:600; border:none; cursor:pointer; background:${p.is_active ? '#DCFCE7' : '#FEE2E2'}; color:${p.is_active ? '#15803D' : '#B91C1C'};">
          ${p.is_active ? 'Активен' : 'Скрыт'}
        </button>
      </td>
      <td style="padding:12px;">
        <div style="display:flex; gap:6px;">
          <button onclick="editProductModal(${p.id})" class="btn btn-secondary btn-sm">Редактировать</button>
          <button onclick="deleteProductPrompt(${p.id})" class="btn btn-secondary btn-sm" style="color:#DC2626; border-color:#DC2626;">Удалить</button>
        </div>
      </td>
    </tr>
  `).join('');
}

window.toggleProductActive = async (id) => {
  try {
    const res = await window.API.toggleAdminProductStatus(id);
    window.Toast.success(res.message);
    await loadAdminProducts();
  } catch (e) {
    window.Toast.error(e.message);
  }
};

window.deleteProductPrompt = async (id) => {
  if (!confirm('Вы уверены, что хотите удалить этот товар?')) return;
  try {
    await window.API.deleteAdminProduct(id);
    window.Toast.info('Товар удален');
    await loadAdminProducts();
  } catch (e) {
    window.Toast.error(e.message);
  }
};

function setupProductForm() {
  const form = document.getElementById('admin-product-form');
  const imageInput = document.getElementById('admin-product-image-file');

  if (imageInput) {
    imageInput.addEventListener('change', async (e) => {
      const file = e.target.files[0];
      if (!file) return;
      try {
        window.Toast.info('Загрузка изображения...');
        const res = await window.API.uploadImage(file);
        const imagesInput = document.getElementById('admin-prod-images-urls');
        if (imagesInput) {
          const current = imagesInput.value.trim();
          imagesInput.value = current ? `${current}\n${res.url}` : res.url;
        }
        window.Toast.success('Фото успешно загружено!');
      } catch (err) {
        window.Toast.error(err.message || 'Ошибка загрузки фото');
      }
    });
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const prodId = document.getElementById('admin-prod-id').value;
      const name = document.getElementById('admin-prod-name').value.trim();
      const sku = document.getElementById('admin-prod-sku').value.trim();
      const category_id = parseInt(document.getElementById('admin-prod-category').value);
      const price = parseFloat(document.getElementById('admin-prod-price').value);
      const old_price_raw = document.getElementById('admin-prod-old-price').value;
      const old_price = old_price_raw ? parseFloat(old_price_raw) : null;
      const description = document.getElementById('admin-prod-desc').value.trim();
      const is_active = document.getElementById('admin-prod-active').checked;
      const is_featured = document.getElementById('admin-prod-featured').checked;
      const is_new = document.getElementById('admin-prod-new').checked;

      const imagesText = document.getElementById('admin-prod-images-urls').value.trim();
      const images = imagesText ? imagesText.split('\n').map(u => u.trim()).filter(Boolean) : [];

      const variantsText = document.getElementById('admin-prod-variants-json').value.trim();
      let variants = [];
      if (variantsText) {
        try {
          variants = JSON.parse(variantsText);
        } catch (err) {
          window.Toast.error('Неверный JSON формат вариантов');
          return;
        }
      }

      const payload = {
        name,
        slug: name.toLowerCase().replace(/\s+/g, '-'),
        sku,
        category_id,
        price,
        old_price,
        description,
        is_active,
        is_featured,
        is_new,
        images,
        variants
      };

      try {
        if (prodId) {
          await window.API.updateAdminProduct(parseInt(prodId), payload);
          window.Toast.success('Товар успешно обновлен');
        } else {
          await window.API.createAdminProduct(payload);
          window.Toast.success('Товар успешно создан');
        }
        window.Modal?.close('admin-product-modal');
        form.reset();
        await loadAdminProducts();
      } catch (err) {
        window.Toast.error(err.message || 'Ошибка сохранения товара');
      }
    });
  }
}

window.openAddProductModal = async () => {
  const form = document.getElementById('admin-product-form');
  if (form) form.reset();
  document.getElementById('admin-prod-id').value = '';
  document.getElementById('admin-product-modal-title').textContent = 'Добавить новый товар';
  await populateCategoryDropdown();
  
  document.getElementById('admin-prod-variants-json').value = JSON.stringify([
    {"size": "S", "color": "Черный", "color_code": "#000000", "stock": 10, "sku": "SKU-S"},
    {"size": "M", "color": "Черный", "color_code": "#000000", "stock": 8, "sku": "SKU-M"},
    {"size": "L", "color": "Черный", "color_code": "#000000", "stock": 5, "sku": "SKU-L"}
  ], null, 2);

  window.Modal?.open('admin-product-modal');
};

window.editProductModal = async (id) => {
  const prod = adminProductsList.find(p => p.id === id);
  if (!prod) return;

  await populateCategoryDropdown();
  document.getElementById('admin-prod-id').value = prod.id;
  document.getElementById('admin-product-modal-title').textContent = `Редактировать: ${prod.name}`;
  document.getElementById('admin-prod-name').value = prod.name;
  document.getElementById('admin-prod-sku').value = prod.sku;
  document.getElementById('admin-prod-category').value = prod.category_id;
  document.getElementById('admin-prod-price').value = prod.price;
  document.getElementById('admin-prod-old-price').value = prod.old_price || '';
  document.getElementById('admin-prod-desc').value = prod.description || '';
  document.getElementById('admin-prod-active').checked = prod.is_active;
  document.getElementById('admin-prod-featured').checked = prod.is_featured;
  document.getElementById('admin-prod-new').checked = prod.is_new;
  document.getElementById('admin-prod-images-urls').value = (prod.images || []).join('\n');
  document.getElementById('admin-prod-variants-json').value = JSON.stringify(prod.variants || [], null, 2);

  window.Modal?.open('admin-product-modal');
};

async function populateCategoryDropdown() {
  const select = document.getElementById('admin-prod-category');
  if (!select) return;
  const categories = await window.API.getAdminCategories();
  select.innerHTML = categories.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
}

// 3. Categories Management
let adminCategoriesList = [];
async function loadAdminCategories() {
  const container = document.getElementById('admin-categories-table-body');
  if (!container) return;

  try {
    const categories = await window.API.getAdminCategories();
    adminCategoriesList = categories;
    container.innerHTML = categories.map(c => `
      <tr style="border-bottom:1px solid #E5E0D8;">
        <td style="padding:12px;">
          <img src="${c.image_url || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=200'}" style="width:40px; height:40px; object-fit:cover; border-radius:4px;">
        </td>
        <td style="padding:12px; font-weight:600;">${c.name}</td>
        <td style="padding:12px; color:#78716C;">${c.slug}</td>
        <td style="padding:12px;">${c.products_count}</td>
        <td style="padding:12px;">${c.sort_order}</td>
        <td style="padding:12px;">
          <div style="display:flex; gap:6px;">
            <button onclick="editCategoryModal(${c.id})" class="btn btn-secondary btn-sm">Редактировать</button>
            <button onclick="deleteCategoryPrompt(${c.id})" class="btn btn-secondary btn-sm" style="color:#DC2626; border-color:#DC2626;">Удалить</button>
          </div>
        </td>
      </tr>
    `).join('');
  } catch (e) {
    console.error(e);
  }
}

function setupCategoryForm() {
  const form = document.getElementById('admin-category-form');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const catId = document.getElementById('admin-cat-id').value;
      const name = document.getElementById('admin-cat-name').value.trim();
      const slug = document.getElementById('admin-cat-slug').value.trim() || name.toLowerCase().replace(/\s+/g, '-');
      const image_url = document.getElementById('admin-cat-image').value.trim();
      const sort_order = parseInt(document.getElementById('admin-cat-sort').value) || 0;

      try {
        if (catId) {
          await window.API.updateAdminCategory(parseInt(catId), { name, slug, image_url, sort_order });
          window.Toast.success('Категория обновлена');
        } else {
          await window.API.createAdminCategory({ name, slug, image_url, sort_order });
          window.Toast.success('Категория создана');
        }
        window.Modal?.close('admin-category-modal');
        form.reset();
        await loadAdminCategories();
      } catch (err) {
        window.Toast.error(err.message || 'Ошибка сохранения категории');
      }
    });
  }
}

window.openAddCategoryModal = () => {
  const form = document.getElementById('admin-category-form');
  if (form) form.reset();
  document.getElementById('admin-cat-id').value = '';
  document.getElementById('admin-category-modal-title').textContent = 'Добавить категорию';
  window.Modal?.open('admin-category-modal');
};

window.editCategoryModal = (id) => {
  const cat = adminCategoriesList.find(c => c.id === id);
  if (!cat) return;
  document.getElementById('admin-cat-id').value = cat.id;
  document.getElementById('admin-category-modal-title').textContent = `Редактировать: ${cat.name}`;
  document.getElementById('admin-cat-name').value = cat.name;
  document.getElementById('admin-cat-slug').value = cat.slug;
  document.getElementById('admin-cat-image').value = cat.image_url || '';
  document.getElementById('admin-cat-sort').value = cat.sort_order;
  window.Modal?.open('admin-category-modal');
};

window.deleteCategoryPrompt = async (id) => {
  if (!confirm('Удалить категорию?')) return;
  try {
    await window.API.deleteAdminCategory(id);
    window.Toast.info('Категория удалена');
    await loadAdminCategories();
  } catch (err) {
    window.Toast.error(err.message);
  }
};

// 4. Orders Management
let currentAdminOrders = [];
async function loadAdminOrders(statusFilter = null) {
  const container = document.getElementById('admin-orders-table-body');
  if (!container) return;

  try {
    const orders = await window.API.getAdminOrders(statusFilter ? { status_filter: statusFilter } : {});
    currentAdminOrders = orders;
    container.innerHTML = orders.map(o => `
      <tr style="border-bottom:1px solid #E5E0D8;">
        <td style="padding:12px; font-weight:700;">${o.order_number}</td>
        <td style="padding:12px;">
          <div>${o.first_name} ${o.last_name}</div>
          <div style="font-size:0.75rem; color:#78716C;">${o.phone} | ${o.email}</div>
        </td>
        <td style="padding:12px; font-weight:600;">${window.Store.formatPrice(o.total_amount)}</td>
        <td style="padding:12px;">${o.delivery_method}</td>
        <td style="padding:12px;">
          <select onchange="changeOrderStatus(${o.id}, this.value)" style="padding:4px 8px; border:1px solid #E5E0D8; border-radius:4px; font-size:0.813rem; font-weight:500;">
            <option value="Новый" ${o.status === 'Новый' ? 'selected' : ''}>Новый</option>
            <option value="Подтверждён" ${o.status === 'Подтверждён' ? 'selected' : ''}>Подтверждён</option>
            <option value="Собирается" ${o.status === 'Собирается' ? 'selected' : ''}>Собирается</option>
            <option value="Отправлен" ${o.status === 'Отправлен' ? 'selected' : ''}>Отправлен</option>
            <option value="Доставлен" ${o.status === 'Доставлен' ? 'selected' : ''}>Доставлен</option>
            <option value="Отменён" ${o.status === 'Отменён' ? 'selected' : ''}>Отменён</option>
          </select>
        </td>
        <td style="padding:12px;">
          <button onclick="viewAdminOrder(${o.id})" class="btn btn-secondary btn-sm">Детали</button>
        </td>
      </tr>
    `).join('');
  } catch (e) {
    console.error(e);
  }
}

window.filterAdminOrders = (status) => {
  document.querySelectorAll('.order-filter-tab').forEach(t => t.classList.remove('active', 'bg-neutral-800', 'text-white'));
  if (window.event?.target) {
    window.event.target.classList.add('active', 'bg-neutral-800', 'text-white');
  }
  loadAdminOrders(status || null);
};

window.changeOrderStatus = async (orderId, newStatus) => {
  try {
    const res = await window.API.updateAdminOrderStatus(orderId, newStatus);
    window.Toast.success(res.message);
    await loadAdminStats();
  } catch (err) {
    window.Toast.error(err.message || 'Ошибка обновления статуса');
  }
};

window.viewAdminOrder = (orderId) => {
  const o = currentAdminOrders.find(item => item.id === orderId);
  if (!o) return;

  const modalBody = document.getElementById('admin-order-modal-body');
  if (!modalBody) return;

  modalBody.innerHTML = `
    <div style="display:flex; justify-content:space-between; margin-bottom:16px; border-bottom:1px solid #E5E0D8; padding-bottom:12px;">
      <div>
        <h4 style="font-size:1.125rem; font-weight:700;">Заказ ${o.order_number}</h4>
        <div style="font-size:0.813rem; color:#78716C;">Дата: ${new Date(o.created_at).toLocaleString('ru-RU')}</div>
      </div>
      <div style="text-align:right;">
        <div style="font-weight:700; font-size:1.125rem;">${window.Store.formatPrice(o.total_amount)}</div>
        <div style="font-size:0.813rem; color:#15803D;">Статус: <strong>${o.status}</strong></div>
      </div>
    </div>

    <div style="margin-bottom:16px; background:#FAF8F5; padding:12px; border-radius:8px; font-size:0.875rem;">
      <div><strong>Клиент:</strong> ${o.first_name} ${o.last_name}</div>
      <div><strong>Телефон:</strong> ${o.phone}</div>
      <div><strong>Email:</strong> ${o.email}</div>
      <div><strong>Город и Адрес:</strong> ${o.city}, ${o.address}</div>
      <div><strong>Способ доставки:</strong> ${o.delivery_method} (${o.delivery_fee === 0 ? 'Бесплатно' : window.Store.formatPrice(o.delivery_fee)})</div>
      <div><strong>Оплата:</strong> ${o.payment_method} (${o.payment_status})</div>
      ${o.notes ? `<div><strong>Комментарий:</strong> ${o.notes}</div>` : ''}
    </div>

    <h5 style="font-weight:600; margin-bottom:8px;">Товары в заказе:</h5>
    <div style="max-height:220px; overflow-y:auto;">
      ${o.items.map(it => `
        <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #F0EDE8; font-size:0.875rem;">
          <div style="display:flex; gap:8px; align-items:center;">
            <img src="${it.image_url || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=200'}" style="width:36px; height:46px; object-fit:cover; border-radius:4px;">
            <div>
              <div style="font-weight:500;">${it.product_name}</div>
              <div style="color:#78716C; font-size:0.75rem;">${it.size || ''} | ${it.color || ''} | ${it.quantity} шт.</div>
            </div>
          </div>
          <div style="font-weight:600;">${window.Store.formatPrice(it.total_price)}</div>
        </div>
      `).join('')}
    </div>
  `;

  window.Modal?.open('admin-order-detail-modal');
};

// 5. Users Management
async function loadAdminUsers() {
  const container = document.getElementById('admin-users-table-body');
  if (!container) return;

  try {
    const users = await window.API.getAdminUsers();
    container.innerHTML = users.map(u => `
      <tr style="border-bottom:1px solid #E5E0D8;">
        <td style="padding:12px; font-weight:600;">${u.full_name}</td>
        <td style="padding:12px;">${u.email}</td>
        <td style="padding:12px;">${u.phone || '—'}</td>
        <td style="padding:12px;">
          <span style="padding:2px 8px; border-radius:4px; font-size:0.75rem; font-weight:600; background:${u.role === 'admin' ? '#EDE9FE' : '#F0EDE8'}; color:${u.role === 'admin' ? '#6D28D9' : '#121212'};">
            ${u.role}
          </span>
        </td>
        <td style="padding:12px;">${u.orders_count} заказов</td>
        <td style="padding:12px; font-weight:600;">${window.Store.formatPrice(u.total_spent)}</td>
        <td style="padding:12px;">
          <button onclick="toggleUserActive(${u.id})" style="padding:4px 8px; border-radius:4px; font-size:0.75rem; font-weight:600; border:none; cursor:pointer; background:${u.is_active ? '#DCFCE7' : '#FEE2E2'}; color:${u.is_active ? '#15803D' : '#B91C1C'};">
            ${u.is_active ? 'Активен' : 'Заблокирован'}
          </button>
        </td>
      </tr>
    `).join('');
  } catch (e) {
    console.error(e);
  }
}

window.toggleUserActive = async (userId) => {
  try {
    const res = await window.API.toggleAdminUserStatus(userId);
    window.Toast.success(res.message);
    await loadAdminUsers();
  } catch (err) {
    window.Toast.error(err.message || 'Ошибка изменения статуса');
  }
};

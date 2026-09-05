// Catalog Page JavaScript
let currentFilters = {
  category_slug: null,
  q: null,
  min_price: null,
  max_price: null,
  sizes: [],
  colors: [],
  in_stock: false,
  on_sale: false,
  sort_by: 'newest',
  page: 1,
  limit: 12
};

document.addEventListener('DOMContentLoaded', async () => {
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has('category')) currentFilters.category_slug = urlParams.get('category');
  if (urlParams.has('q')) {
    currentFilters.q = urlParams.get('q');
    const searchHeader = document.getElementById('catalog-search-title');
    if (searchHeader) searchHeader.textContent = `Результати пошуку за запитом «${currentFilters.q}»`;
  }
  if (urlParams.has('sort')) currentFilters.sort_by = urlParams.get('sort');
  if (urlParams.has('on_sale')) currentFilters.on_sale = true;

  await Promise.all([
    loadCategoriesFilter(),
    loadCatalogProducts()
  ]);
  setupFilterEventListeners();
});

async function loadCategoriesFilter() {
  const container = document.getElementById('filter-categories-list');
  if (!container) return;

  try {
    const categories = await window.API.getCategories();
    container.innerHTML = `
      <label class="filter-radio-item" style="display:flex; align-items:center; gap:8px; cursor:pointer; font-size:0.875rem; padding:4px 0;">
        <input type="radio" name="cat-filter" value="" ${!currentFilters.category_slug ? 'checked' : ''} onchange="selectCategory(null)">
        <span>${window.I18N ? window.I18N.t("cat_all") : "Усі категорії"}</span>
      </label>
      ${categories.map(c => `
        <label class="filter-radio-item" style="display:flex; align-items:center; justify-content:space-between; cursor:pointer; font-size:0.875rem; padding:4px 0;">
          <div style="display:flex; align-items:center; gap:8px;">
            <input type="radio" name="cat-filter" value="${c.slug}" ${currentFilters.category_slug === c.slug ? 'checked' : ''} onchange="selectCategory('${c.slug}')">
            <span>${window.I18N ? window.I18N.t("cat_" + c.slug) || c.name : c.name}</span>
          </div>
          <span style="color:#A8A29E; font-size:0.75rem;">${c.products_count || 0}</span>
        </label>
      `).join('')}
    `;
  } catch (e) {
    console.error(e);
  }
}

window.selectCategory = (slug) => {
  currentFilters.category_slug = slug;
  currentFilters.page = 1;
  loadCatalogProducts();
};

async function loadCatalogProducts() {
  const grid = document.getElementById('catalog-products-grid');
  const countEl = document.getElementById('catalog-total-count');
  const paginationEl = document.getElementById('catalog-pagination');

  if (!grid) return;

  grid.innerHTML = Array(6).fill(0).map(() => `
    <div style="border-radius:12px; overflow:hidden; border:1px solid #E5E0D8; height:450px; display:flex; flex-direction:column; background:#FFF;">
      <div class="skeleton" style="height:300px; width:100%;"></div>
      <div style="padding:16px; flex:1; display:flex; flex-direction:column; gap:8px;">
        <div class="skeleton" style="height:14px; width:40%;"></div>
        <div class="skeleton" style="height:18px; width:90%;"></div>
        <div class="skeleton" style="height:22px; width:50%; margin-top:auto;"></div>
      </div>
    </div>
  `).join('');

  try {
    const params = {
      category_slug: currentFilters.category_slug,
      q: currentFilters.q,
      min_price: currentFilters.min_price,
      max_price: currentFilters.max_price,
      sizes: currentFilters.sizes.join(','),
      colors: currentFilters.colors.join(','),
      in_stock: currentFilters.in_stock || undefined,
      on_sale: currentFilters.on_sale || undefined,
      sort_by: currentFilters.sort_by,
      page: currentFilters.page,
      limit: currentFilters.limit
    };

    const res = await window.API.getProducts(params);
    if (countEl) countEl.textContent = `${res.total} товаров`;

    renderDynamicFilterOptions(res.available_sizes, res.available_colors);

    if (res.items.length === 0) {
      grid.innerHTML = `
        <div style="grid-column:1/-1; text-align:center; padding:60px 20px; background:#FFF; border-radius:12px; border:1px solid #E5E0D8;">
          <h3 style="font-size:1.25rem; font-weight:600; margin-bottom:8px;">Ничего не найдено</h3>
          <p style="color:#78716C; font-size:0.875rem; margin-bottom:20px;">Попробуйте изменить параметры фильтра или сбросить их</p>
          <button onclick="resetFilters()" class="btn btn-primary btn-sm">Сбросить все фильтры</button>
        </div>
      `;
      if (paginationEl) paginationEl.innerHTML = '';
      return;
    }

    grid.innerHTML = res.items.map(p => `
      <div class="product-card" style="background:var(--color-surface); border-radius:12px; overflow:hidden; border:1px solid var(--color-border); display:flex; flex-direction:column; position:relative;">
        <button onclick="window.Store.toggleFavorite(${p.id}).then(() => this.classList.toggle('active', window.Store.isFavorite(${p.id})))" 
          class="fav-btn ${p.is_favorite ? 'active' : ''}" 
          style="position:absolute; top:12px; right:12px; z-index:10; background:rgba(255,255,255,0.85); backdrop-filter:blur(4px); border:none; border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center; cursor:pointer; box-shadow:0 2px 6px rgba(0,0,0,0.08);"
          title="В обране">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="${p.is_favorite ? '#E11D48' : 'none'}" stroke="${p.is_favorite ? '#E11D48' : '#121212'}" stroke-width="2"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
        </button>

        <div style="position:absolute; top:12px; left:12px; z-index:10; display:flex; flex-direction:column; gap:4px;">
          ${p.discount_percent ? `<span style="background:var(--color-sale); color:#FFF; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:4px;">-${p.discount_percent}%</span>` : ''}
          ${p.is_new ? `<span style="background:var(--color-new); color:#FFF; font-size:0.75rem; font-weight:600; padding:2px 8px; border-radius:4px;">NEW</span>` : ''}
        </div>

        <a href="/product/${p.slug}" style="display:block; height:330px; position:relative; overflow:hidden; background:#F3EFEA;">
          <img src="${window.optimizeImg ? window.optimizeImg(p.primary_image, 500, 75) : p.primary_image}" alt="${p.name}" class="img-zoom" loading="lazy" decoding="async" style="width:100%; height:100%; object-fit:cover;">
        </a>

        <div style="padding:16px; display:flex; flex-direction:column; flex:1; justify-content:space-between;">
          <div>
            <div style="font-size:0.75rem; text-transform:uppercase; color:#78716C; letter-spacing:0.05em; margin-bottom:4px;">${p.category_name || 'Одяг'}</div>
            <a href="/product/${p.slug}" style="font-size:0.938rem; font-weight:500; color:#121212; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; line-height:1.35; height:38px; margin-bottom:8px;">${p.name}</a>
            
            ${p.sizes && p.sizes.length > 0 ? `
              <div style="display:flex; flex-wrap:wrap; gap:4px; margin-bottom:10px;">
                ${p.sizes.map(s => `<span style="font-size:0.688rem; border:1px solid #E5E0D8; padding:2px 6px; border-radius:3px; color:#57534E;">${s}</span>`).join('')}
              </div>
            ` : ''}
          </div>

          <div>
            <div style="display:flex; align-items:baseline; gap:8px; margin-bottom:12px;">
              <span style="font-size:1.125rem; font-weight:700; color:#121212;">${window.Store.formatPrice(p.price)}</span>
              ${p.old_price ? `<span style="font-size:0.875rem; text-decoration:line-through; color:#A8A29E;">${window.Store.formatPrice(p.old_price)}</span>` : ''}
            </div>

            <a href="/product/${p.slug}" class="btn btn-secondary btn-sm" style="width:100%;">
              ${window.I18N ? window.I18N.t('cart_choose_size') : 'Обрати розмір'}
            </a>
          </div>
        </div>
      </div>
    `).join('');

    renderPagination(paginationEl, res.page, res.pages);
  } catch (err) {
    grid.innerHTML = '<div style="grid-column:1/-1; text-align:center; padding:40px; color:#B91C1C;">Ошибка при загрузке каталога</div>';
    console.error(err);
  }
}

function renderDynamicFilterOptions(sizes, colors) {
  const sizesContainer = document.getElementById('filter-sizes-list');
  const colorsContainer = document.getElementById('filter-colors-list');

  if (sizesContainer && sizes && sizes.length > 0 && sizesContainer.children.length === 0) {
    sizesContainer.innerHTML = sizes.map(s => `
      <button type="button" class="size-badge ${currentFilters.sizes.includes(s) ? 'active' : ''}" onclick="toggleSizeFilter('${s}', this)">
        ${s}
      </button>
    `).join('');
  }

  if (colorsContainer && colors && colors.length > 0 && colorsContainer.children.length === 0) {
    colorsContainer.innerHTML = colors.map(c => `
      <div style="display:flex; align-items:center; gap:8px; cursor:pointer; font-size:0.813rem; padding:3px 0;" onclick="toggleColorFilter('${c.name}', this)">
        <span class="color-dot ${currentFilters.colors.includes(c.name) ? 'active' : ''}" style="background:${c.code}; width:18px; height:18px;"></span>
        <span>${window.I18N ? window.I18N.t("cat_" + c.slug) || c.name : c.name}</span>
      </div>
    `).join('');
  }
}

window.toggleSizeFilter = (size, btn) => {
  if (currentFilters.sizes.includes(size)) {
    currentFilters.sizes = currentFilters.sizes.filter(s => s !== size);
    btn.classList.remove('active');
  } else {
    currentFilters.sizes.push(size);
    btn.classList.add('active');
  }
  currentFilters.page = 1;
  loadCatalogProducts();
};

window.toggleColorFilter = (colorName, el) => {
  const dot = el.querySelector('.color-dot');
  if (currentFilters.colors.includes(colorName)) {
    currentFilters.colors = currentFilters.colors.filter(c => c !== colorName);
    dot.classList.remove('active');
  } else {
    currentFilters.colors.push(colorName);
    dot.classList.add('active');
  }
  currentFilters.page = 1;
  loadCatalogProducts();
};

function setupFilterEventListeners() {
  const sortSelect = document.getElementById('catalog-sort-select');
  if (sortSelect) {
    sortSelect.value = currentFilters.sort_by;
    sortSelect.addEventListener('change', (e) => {
      currentFilters.sort_by = e.target.value;
      currentFilters.page = 1;
      loadCatalogProducts();
    });
  }

  const inStockCheck = document.getElementById('filter-in-stock');
  if (inStockCheck) {
    inStockCheck.addEventListener('change', (e) => {
      currentFilters.in_stock = e.target.checked;
      currentFilters.page = 1;
      loadCatalogProducts();
    });
  }

  const onSaleCheck = document.getElementById('filter-on-sale');
  if (onSaleCheck) {
    onSaleCheck.addEventListener('change', (e) => {
      currentFilters.on_sale = e.target.checked;
      currentFilters.page = 1;
      loadCatalogProducts();
    });
  }

  const priceMin = document.getElementById('filter-price-min');
  const priceMax = document.getElementById('filter-price-max');
  let priceDebounce = null;

  const handlePriceChange = () => {
    clearTimeout(priceDebounce);
    priceDebounce = setTimeout(() => {
      currentFilters.min_price = priceMin?.value ? parseFloat(priceMin.value) : null;
      currentFilters.max_price = priceMax?.value ? parseFloat(priceMax.value) : null;
      currentFilters.page = 1;
      loadCatalogProducts();
    }, 400);
  };

  if (priceMin) priceMin.addEventListener('input', handlePriceChange);
  if (priceMax) priceMax.addEventListener('input', handlePriceChange);
}

window.resetFilters = () => {
  currentFilters = {
    category_slug: null,
    q: null,
    min_price: null,
    max_price: null,
    sizes: [],
    colors: [],
    in_stock: false,
    on_sale: false,
    sort_by: 'newest',
    page: 1,
    limit: 12
  };
  window.history.pushState({}, '', '/catalog');
  document.querySelectorAll('.filter-radio-item input').forEach(i => i.checked = (i.value === ''));
  document.querySelectorAll('.size-badge').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.color-dot').forEach(d => d.classList.remove('active'));
  const pMin = document.getElementById('filter-price-min');
  const pMax = document.getElementById('filter-price-max');
  const inStock = document.getElementById('filter-in-stock');
  const onSale = document.getElementById('filter-on-sale');
  if (pMin) pMin.value = '';
  if (pMax) pMax.value = '';
  if (inStock) inStock.checked = false;
  if (onSale) onSale.checked = false;

  loadCatalogProducts();
};

function renderPagination(container, currentPage, totalPages) {
  if (!container || totalPages <= 1) {
    if (container) container.innerHTML = '';
    return;
  }

  let html = '<div style="display:flex; justify-content:center; gap:6px; margin-top:40px;">';
  if (currentPage > 1) {
    html += `<button onclick="goToPage(${currentPage - 1})" class="btn btn-secondary btn-sm">← Назад</button>`;
  }
  for (let i = 1; i <= totalPages; i++) {
    if (i === currentPage) {
      html += `<button class="btn btn-primary btn-sm" style="min-width:38px;">${i}</button>`;
    } else if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
      html += `<button onclick="goToPage(${i})" class="btn btn-secondary btn-sm" style="min-width:38px;">${i}</button>`;
    } else if (i === currentPage - 3 || i === currentPage + 3) {
      html += `<span style="padding:4px 8px; color:#A8A29E;">...</span>`;
    }
  }
  if (currentPage < totalPages) {
    html += `<button onclick="goToPage(${currentPage + 1})" class="btn btn-secondary btn-sm">Вперед →</button>`;
  }
  html += '</div>';
  container.innerHTML = html;
}

window.goToPage = (page) => {
  currentFilters.page = page;
  loadCatalogProducts();
  window.scrollTo({ top: 0, behavior: 'smooth' });
};


// Re-render categories and products on language switch
if (window.Store) {
  window.Store.on('lang:changed', () => {
    loadCategoriesFilter();
    loadCatalogProducts();
  });
}

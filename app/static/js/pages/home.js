// Home Page JavaScript
document.addEventListener('DOMContentLoaded', async () => {
  await loadHomeCategories();
  await loadFeaturedProducts();
  await loadNewArrivals();
});

async function loadHomeCategories() {
  const container = document.getElementById('home-categories-grid');
  if (!container) return;

  try {
    const categories = await window.API.getCategories();
    if (!categories || categories.length === 0) {
      container.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:30px;color:#78716C;">Категорії завантажуються...</div>';
      return;
    }
    container.innerHTML = categories.map(cat => `
      <a href="/catalog?category=${cat.slug}" class="category-card" style="position:relative; overflow:hidden; border-radius:12px; height:260px; display:block; box-shadow:0 1px 3px rgba(0,0,0,0.1);">
        <img src="${window.optimizeImg ? window.optimizeImg(cat.image_url, 600, 75) : (cat.image_url || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=600&auto=format&fit=crop&q=75')}" alt="${cat.name}" loading="lazy" decoding="async" style="width:100%; height:100%; object-fit:cover; transition:transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);" class="category-img">
        <div style="position:absolute; inset:0; background:linear-gradient(to top, rgba(0,0,0,0.65) 0%, rgba(0,0,0,0.1) 60%, transparent 100%);"></div>
        <div style="position:absolute; bottom:0; left:0; right:0; padding:20px; color:#FFF;">
          <h3 style="font-size:1.375rem; font-weight:500; font-family:Georgia,serif; margin-bottom:4px;">${window.I18N ? window.I18N.t('cat_' + cat.slug) || cat.name : cat.name}</h3>
          <span style="font-size:0.813rem; opacity:0.85;">${cat.products_count || 0} ${window.I18N && window.I18N.currentLang === 'ru' ? 'моделей' : 'моделей'}</span>
        </div>
      </a>
    `).join('');

    document.querySelectorAll('.category-card').forEach(card => {
      card.addEventListener('mouseenter', () => {
        const img = card.querySelector('.category-img');
        if (img) img.style.transform = 'scale(1.08)';
      });
      card.addEventListener('mouseleave', () => {
        const img = card.querySelector('.category-img');
        if (img) img.style.transform = 'scale(1)';
      });
    });
  } catch (err) {
    console.error('Error loading home categories:', err);
    container.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:30px;color:#78716C;">Помилка завантаження</div>';
  }
}

async function loadFeaturedProducts() {
  const container = document.getElementById('home-featured-grid');
  if (!container) return;

  try {
    const products = await window.API.getFeaturedProducts(8);
    renderProductGrid(container, products);
  } catch (err) {
    console.error('Error loading featured products:', err);
    container.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:30px;color:#78716C;">Помилка завантаження</div>';
  }
}

async function loadNewArrivals() {
  const container = document.getElementById('home-new-grid');
  if (!container) return;

  try {
    const products = await window.API.getNewProducts(8);
    renderProductGrid(container, products);
  } catch (err) {
    console.error('Error loading new arrivals:', err);
    container.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:30px;color:#78716C;">Помилка завантаження</div>';
  }
}

function renderProductGrid(container, products) {
  if (!products || products.length === 0) {
    container.innerHTML = '<div style="grid-column:1/-1; text-align:center; padding:30px; color:#78716C;">Скоро з\'являться нові моделі</div>';
    return;
  }

  const lang = window.I18N ? window.I18N.currentLang : 'ua';
  const chooseSizeLabel = lang === 'ru' ? 'Выбрать размер' : 'Обрати розмір';

  container.innerHTML = products.map(p => `
    <div class="product-card" style="background:#FFF; border-radius:12px; overflow:hidden; border:1px solid #E7E2DA; display:flex; flex-direction:column; position:relative;">
      <button onclick="window.Store.toggleFavorite(${p.id})"
        class="fav-btn ${p.is_favorite ? 'active' : ''}"
        style="position:absolute; top:12px; right:12px; z-index:10; background:rgba(255,255,255,0.85); backdrop-filter:blur(4px); border:none; border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center; cursor:pointer; box-shadow:0 2px 6px rgba(0,0,0,0.08);"
        title="${lang === 'ru' ? 'В избранное' : 'В обране'}">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="${p.is_favorite ? '#E11D48' : 'none'}" stroke="${p.is_favorite ? '#E11D48' : '#121212'}" stroke-width="2"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
      </button>

      <div style="position:absolute; top:12px; left:12px; z-index:10; display:flex; flex-direction:column; gap:4px;">
        ${p.discount_percent ? `<span style="background:#E11D48; color:#FFF; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:4px;">-${p.discount_percent}%</span>` : ''}
        ${p.is_new ? `<span style="background:#16A34A; color:#FFF; font-size:0.75rem; font-weight:600; padding:2px 8px; border-radius:4px;">NEW</span>` : ''}
      </div>

      <a href="/product/${p.slug}" style="display:block; height:320px; position:relative; overflow:hidden; background:#F3EFEA;">
        <img src="${window.optimizeImg ? window.optimizeImg(p.primary_image, 500, 75) : (p.primary_image || 'https://images.unsplash.com/photo-1544923246-77307dd654cb?w=500&auto=format&fit=crop&q=75')}" alt="${p.name}" class="img-zoom" loading="lazy" decoding="async" style="width:100%; height:100%; object-fit:cover; transition:transform 0.6s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
      </a>

      <div style="padding:16px; display:flex; flex-direction:column; flex:1; justify-content:space-between;">
        <div>
          <div style="font-size:0.75rem; text-transform:uppercase; color:#78716C; letter-spacing:0.05em; margin-bottom:4px;">${p.category_name || 'Одяг'}</div>
          <a href="/product/${p.slug}" style="font-size:0.938rem; font-weight:500; color:#121212; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; line-height:1.35; height:38px; margin-bottom:8px;">${p.name}</a>

          ${p.colors && p.colors.length > 0 ? `
            <div style="display:flex; gap:6px; margin-bottom:8px;">
              ${p.colors.slice(0, 5).map(c => `
                <span style="width:14px; height:14px; border-radius:50%; background:${c.code}; display:inline-block; border:1px solid rgba(0,0,0,0.1);" title="${c.name}"></span>
              `).join('')}
            </div>
          ` : ''}
        </div>

        <div>
          <div style="display:flex; align-items:baseline; gap:8px; margin-bottom:12px;">
            <span style="font-size:1.125rem; font-weight:700; color:#121212;">${window.Store.formatPrice(p.price)}</span>
            ${p.old_price ? `<span style="font-size:0.875rem; text-decoration:line-through; color:#A8A29E;">${window.Store.formatPrice(p.old_price)}</span>` : ''}
          </div>

          <a href="/product/${p.slug}" style="display:block; width:100%; padding:10px; text-align:center; border:1.5px solid #121212; border-radius:6px; font-size:0.813rem; font-weight:500; color:#121212; text-decoration:none; transition:all 0.2s;" onmouseover="this.style.background='#121212';this.style.color='#FFF'" onmouseout="this.style.background='transparent';this.style.color='#121212'">
            ${chooseSizeLabel}
          </a>
        </div>
      </div>
    </div>
  `).join('');
}

// Re-render categories on language switch
window.addEventListener('lang:changed', () => {
  loadHomeCategories();
  loadFeaturedProducts();
  loadNewArrivals();
});

if (window.Store) {
  window.Store.on('lang:changed', () => {
    loadHomeCategories();
  });
}

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
    container.innerHTML = categories.map(cat => `
      <a href="/catalog?category=${cat.slug}" class="category-card" style="position:relative; overflow:hidden; border-radius:12px; height:260px; display:block; box-shadow:var(--shadow-sm);">
        <img src="${cat.image_url || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800'}" alt="${cat.name}" style="width:100%; height:100%; object-fit:cover; transition:transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);" class="category-img">
        <div style="position:absolute; inset:0; background:linear-gradient(to top, rgba(0,0,0,0.65) 0%, rgba(0,0,0,0.1) 60%, transparent 100%);"></div>
        <div style="position:absolute; bottom:0; left:0; right:0; padding:20px; color:#FFF;">
          <h3 style="font-size:1.375rem; font-weight:500; font-family:var(--font-serif); margin-bottom:4px;">${cat.name}</h3>
          <span style="font-size:0.813rem; opacity:0.85;">${cat.products_count || 0} моделей</span>
        </div>
      </a>
    `).join('');

    document.querySelectorAll('.category-card').forEach(card => {
      card.addEventListener('mouseenter', () => {
        card.querySelector('.category-img').style.transform = 'scale(1.08)';
      });
      card.addEventListener('mouseleave', () => {
        card.querySelector('.category-img').style.transform = 'scale(1)';
      });
    });
  } catch (err) {
    console.error('Error loading home categories:', err);
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
  }
}

function renderProductGrid(container, products) {
  if (!products || products.length === 0) {
    container.innerHTML = '<div style="grid-column:1/-1; text-align:center; padding:30px; color:#78716C;">Скоро поступят новые модели</div>';
    return;
  }

  container.innerHTML = products.map(p => `
    <div class="product-card" style="background:var(--color-surface); border-radius:12px; overflow:hidden; border:1px solid var(--color-border); display:flex; flex-direction:column; position:relative;">
      <button onclick="window.Store.toggleFavorite(${p.id}).then(() => this.classList.toggle('active', window.Store.isFavorite(${p.id})))" 
        class="fav-btn ${p.is_favorite ? 'active' : ''}" 
        style="position:absolute; top:12px; right:12px; z-index:10; background:rgba(255,255,255,0.85); backdrop-filter:blur(4px); border:none; border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center; cursor:pointer; box-shadow:0 2px 6px rgba(0,0,0,0.08);"
        title="В избранное">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="${p.is_favorite ? '#E11D48' : 'none'}" stroke="${p.is_favorite ? '#E11D48' : '#121212'}" stroke-width="2"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
      </button>

      <div style="position:absolute; top:12px; left:12px; z-index:10; display:flex; flex-direction:column; gap:4px;">
        ${p.discount_percent ? `<span style="background:var(--color-sale); color:#FFF; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:4px;">-${p.discount_percent}%</span>` : ''}
        ${p.is_new ? `<span style="background:var(--color-new); color:#FFF; font-size:0.75rem; font-weight:600; padding:2px 8px; border-radius:4px;">NEW</span>` : ''}
      </div>

      <a href="/product/${p.slug}" style="display:block; height:320px; position:relative; overflow:hidden; background:#F3EFEA;">
        <img src="${p.primary_image}" alt="${p.name}" class="img-zoom" style="width:100%; height:100%; object-fit:cover;">
      </a>

      <div style="padding:16px; display:flex; flex-direction:column; flex:1; justify-content:space-between;">
        <div>
          <div style="font-size:0.75rem; text-transform:uppercase; color:#78716C; letter-spacing:0.05em; margin-bottom:4px;">${p.category_name || 'Одежда'}</div>
          <a href="/product/${p.slug}" style="font-size:0.938rem; font-weight:500; color:#121212; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; line-height:1.35; height:38px; margin-bottom:8px;">${p.name}</a>
          
          ${p.colors && p.colors.length > 0 ? `
            <div style="display:flex; gap:6px; margin-bottom:8px;">
              ${p.colors.slice(0, 5).map(c => `
                <span class="color-dot" style="background:${c.code};" title="${c.name}"></span>
              `).join('')}
            </div>
          ` : ''}
        </div>

        <div>
          <div style="display:flex; align-items:baseline; gap:8px; margin-bottom:12px;">
            <span style="font-size:1.125rem; font-weight:700; color:#121212;">${window.Store.formatPrice(p.price)}</span>
            ${p.old_price ? `<span style="font-size:0.875rem; text-decoration:line-through; color:#A8A29E;">${window.Store.formatPrice(p.old_price)}</span>` : ''}
          </div>

          <a href="/product/${p.slug}" class="btn btn-secondary btn-sm" style="width:100%;">
            Выбрать размер
          </a>
        </div>
      </div>
    </div>
  `).join('');
}

// Product Detail Page JavaScript
let currentProduct = null;
let selectedSize = null;
let selectedColor = null;
let selectedQuantity = 1;

document.addEventListener('DOMContentLoaded', async () => {
  const pathParts = window.location.pathname.split('/');
  const slug = pathParts[pathParts.length - 1];

  if (!slug) return;
  await loadProductDetail(slug);

  if (window.Store) {
    window.Store.on('lang:changed', () => {
      if (currentProduct) {
        updateProductLocalizedContent(currentProduct);
      }
    });
  }
});

async function loadProductDetail(slug) {
  try {
    const product = await window.API.getProductDetail(slug);
    currentProduct = product;

    document.title = `${product.name} — Female-Fabric`;

    // Breadcrumbs
    const bcCat = document.getElementById('product-breadcrumb-cat') || document.getElementById('product-bc-category');
    const bcName = document.getElementById('product-breadcrumb-name') || document.getElementById('product-bc-name');
    if (bcCat) {
      const catTranslated = window.I18N ? window.I18N.t('cat_' + product.category_slug) : null;
      bcCat.textContent = catTranslated || product.category_name || 'Каталог';
      bcCat.onclick = () => window.location.href = `/catalog?category=${product.category_slug}`;
    }
    if (bcName) bcName.textContent = product.name;

    // Category Badge
    const catBadge = document.getElementById('product-category-badge');
    if (catBadge) {
      const catTranslated = window.I18N ? window.I18N.t('cat_' + product.category_slug) : null;
      catBadge.textContent = catTranslated || product.category_name || 'Одяг';
    }

    // SKU
    const skuEl = document.getElementById('product-sku');
    if (skuEl) skuEl.textContent = product.sku;

    // Title
    const titleEl = document.getElementById('product-title');
    if (titleEl) titleEl.textContent = product.name;

    // Price & Discount
    const priceEl = document.getElementById('product-price');
    const oldPriceEl = document.getElementById('product-old-price');
    const discountEl = document.getElementById('product-discount-badge');

    if (priceEl) priceEl.textContent = window.Store.formatPrice(product.price);
    if (oldPriceEl) {
      if (product.old_price && product.old_price > product.price) {
        oldPriceEl.textContent = window.Store.formatPrice(product.old_price);
        oldPriceEl.classList.remove('hidden');
      } else {
        oldPriceEl.classList.add('hidden');
      }
    }
    if (discountEl) {
      if (product.discount_percent && product.discount_percent > 0) {
        discountEl.textContent = `-${product.discount_percent}%`;
        discountEl.classList.remove('hidden');
      } else {
        discountEl.classList.add('hidden');
      }
    }

    // Gallery
    renderProductGallery(product);

    // Default Size & Color
    if (product.sizes && product.sizes.length > 0) selectedSize = product.sizes[0];
    if (product.colors && product.colors.length > 0) selectedColor = product.colors[0].name;

    renderSizeSelector(product);
    renderColorSelector(product);

    // Description & Specs
    const descEl = document.getElementById('product-desc') || document.getElementById('product-description');
    if (descEl) descEl.textContent = product.description || '';

    renderProductSpecs(product);

    // Favorite Button
    updateFavoriteButtonState(product.id);

    // Similar Products
    loadSimilarProducts(product);

  } catch (err) {
    console.error('Error loading product details:', err);
    window.Toast?.error('Не вдалося завантажити інформацію про товар');
  }
}

function updateProductLocalizedContent(product) {
  const bcCat = document.getElementById('product-breadcrumb-cat') || document.getElementById('product-bc-category');
  if (bcCat) {
    const catTranslated = window.I18N.t('cat_' + product.category_slug);
    bcCat.textContent = catTranslated || product.category_name || 'Каталог';
  }
  const catBadge = document.getElementById('product-category-badge');
  if (catBadge) {
    const catTranslated = window.I18N.t('cat_' + product.category_slug);
    catBadge.textContent = catTranslated || product.category_name || 'Одяг';
  }
  renderProductSpecs(product);
}

function renderProductGallery(product) {
  const mainImg = document.getElementById('product-main-img') || document.getElementById('product-main-image');
  const thumbsContainer = document.getElementById('product-thumbnails') || document.getElementById('product-thumbnails-container');

  const images = (product.images && product.images.length > 0) ? product.images : [product.primary_image || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800'];

  if (mainImg) {
    mainImg.src = window.optimizeImg ? window.optimizeImg(images[0], 900, 80) : images[0];
    mainImg.decoding = 'async';
    mainImg.alt = product.name;
  }

  if (thumbsContainer) {
    if (images.length > 1) {
      thumbsContainer.innerHTML = images.map((imgUrl, idx) => `
        <button type="button" onclick="window.switchMainProductImage('${imgUrl}', this)" class="product-thumb-btn ${idx === 0 ? 'border-neutral-900' : 'border-transparent'}" style="width:64px; height:80px; border-radius:6px; overflow:hidden; border-width:2px; flex-shrink:0; cursor:pointer; background:#FAF8F5; padding:0;">
          <img src="${window.optimizeImg ? window.optimizeImg(imgUrl, 160, 75) : imgUrl}" alt="Thumbnail ${idx}" loading="lazy" decoding="async" style="width:100%; height:100%; object-fit:cover;">
        </button>
      `).join('');
    } else {
      thumbsContainer.innerHTML = '';
    }
  }
}

window.switchMainProductImage = (url, btn) => {
  const mainImg = document.getElementById('product-main-img') || document.getElementById('product-main-image');
  if (mainImg) mainImg.src = window.optimizeImg ? window.optimizeImg(url, 900, 80) : url;
  document.querySelectorAll('.product-thumb-btn').forEach(b => {
    b.classList.remove('border-neutral-900');
    b.classList.add('border-transparent');
  });
  if (btn) {
    btn.classList.remove('border-transparent');
    btn.classList.add('border-neutral-900');
  }
};

function renderSizeSelector(product) {
  const container = document.getElementById('product-sizes-list') || document.getElementById('product-sizes-selector');
  if (!container) return;

  const sizes = product.sizes && product.sizes.length > 0 ? product.sizes : ['XS', 'S', 'M', 'L'];
  container.innerHTML = sizes.map(s => `
    <button type="button" onclick="window.selectProductSize('${s}', this)" 
      class="size-choice-btn px-4 py-2 text-xs font-semibold rounded-md border transition ${selectedSize === s ? 'bg-neutral-900 text-white border-neutral-900' : 'bg-white text-neutral-800 border-[#E7E2DA] hover:border-neutral-900'}">
      ${s}
    </button>
  `).join('');
}

window.selectProductSize = (size, btn) => {
  selectedSize = size;
  document.querySelectorAll('.size-choice-btn').forEach(b => {
    b.className = 'size-choice-btn px-4 py-2 text-xs font-semibold rounded-md border transition bg-white text-neutral-800 border-[#E7E2DA] hover:border-neutral-900';
  });
  if (btn) {
    btn.className = 'size-choice-btn px-4 py-2 text-xs font-semibold rounded-md border transition bg-neutral-900 text-white border-neutral-900';
  }
};

function renderColorSelector(product) {
  const container = document.getElementById('product-colors-list') || document.getElementById('product-colors-selector');
  const labelEl = document.getElementById('selected-color-name') || document.getElementById('product-selected-color-name');

  if (!container) return;
  const colors = product.colors && product.colors.length > 0 ? product.colors : [{ name: 'Базовий', code: '#121212' }];

  if (labelEl && selectedColor) labelEl.textContent = selectedColor;

  container.innerHTML = colors.map(c => `
    <button type="button" onclick="window.selectProductColor('${c.name}', this)" 
      class="color-choice-btn w-7 h-7 rounded-full border-2 transition ${selectedColor === c.name ? 'border-neutral-900 scale-110' : 'border-transparent hover:scale-105'}" 
      style="background:${c.code}; padding:0;" title="${c.name}">
    </button>
  `).join('');
}

window.selectProductColor = (colorName, btn) => {
  selectedColor = colorName;
  document.querySelectorAll('.color-choice-btn').forEach(b => {
    b.classList.remove('border-neutral-900', 'scale-110');
    b.classList.add('border-transparent');
  });
  if (btn) {
    btn.classList.remove('border-transparent');
    btn.classList.add('border-neutral-900', 'scale-110');
  }
  const labelEl = document.getElementById('selected-color-name') || document.getElementById('product-selected-color-name');
  if (labelEl) labelEl.textContent = colorName;
};

function renderProductSpecs(product) {
  const specsList = document.getElementById('product-details-list') || document.getElementById('product-specs-list');
  if (!specsList) return;

  if (product.details) {
    const isRu = window.I18N?.currentLang === 'ru';
    specsList.innerHTML = Object.entries(product.details).map(([k, v]) => {
      let label = k;
      if (k === 'composition') label = isRu ? 'Состав' : 'Склад';
      else if (k === 'fit') label = isRu ? 'Посадка и крой' : 'Посадка та крій';
      else if (k === 'season') label = isRu ? 'Сезон' : 'Сезон';
      else if (k === 'care') label = isRu ? 'Уход' : 'Догляд';
      return `<li><strong>${label}:</strong> ${v}</li>`;
    }).join('');
  } else {
    specsList.innerHTML = '<li>100% преміальна натуральна тканина</li><li>Вироблено в Україні</li>';
  }
}

window.addProductToCart = async () => {
  if (!currentProduct) return;
  if (!selectedSize && currentProduct.sizes && currentProduct.sizes.length > 0) {
    window.Toast?.warning(window.I18N?.currentLang === 'ru' ? 'Пожалуйста, выберите размер' : 'Будь ласка, оберіть розмір');
    return;
  }

  const btn = document.getElementById('btn-add-to-cart') || document.getElementById('add-to-cart-btn');
  try {
    if (btn) {
      btn.disabled = true;
      btn.textContent = window.I18N?.currentLang === 'ru' ? 'Добавление...' : 'Додавання...';
    }

    const updatedCart = await window.API.addToCart(
      currentProduct.id,
      selectedSize,
      selectedColor,
      selectedQuantity
    );

    window.Store.cart = updatedCart;
    window.Store.emit('cart:updated', updatedCart);
    window.Toast?.success(window.I18N?.currentLang === 'ru' ? `«${currentProduct.name}» добавлен в корзину` : `«${currentProduct.name}» додано в кошик`);
    window.Modal?.open('cart-drawer');
  } catch (err) {
    window.Toast?.error(err.message || 'Не вдалося додати в кошик');
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = window.I18N ? window.I18N.t('product_add_cart') : 'Додати в кошик';
    }
  }
};

window.toggleProductFav = async () => {
  if (!currentProduct) return;
  const isFav = await window.Store.toggleFavorite(currentProduct.id);
  updateFavoriteButtonState(currentProduct.id);
  window.Toast?.success(isFav ? 
    (window.I18N?.currentLang === 'ru' ? 'Товар добавлен в избранное' : 'Товар додано до обраного') : 
    (window.I18N?.currentLang === 'ru' ? 'Товар удален из избранного' : 'Товар видалено з обраного')
  );
};

function updateFavoriteButtonState(productId) {
  const btn = document.getElementById('btn-toggle-fav') || document.getElementById('product-fav-btn');
  if (!btn) return;
  const isFav = window.Store.isFavorite(productId);
  const svg = btn.querySelector('svg');
  if (svg) {
    svg.setAttribute('fill', isFav ? '#E11D48' : 'none');
    svg.setAttribute('stroke', isFav ? '#E11D48' : '#121212');
  }
}

async function loadSimilarProducts(product) {
  const container = document.getElementById('product-similar-grid') || document.getElementById('product-related-grid');
  if (!container) return;

  try {
    const res = await window.API.getProducts({ category_slug: product.category_slug, limit: 4 });
    const items = res.items.filter(p => p.id !== product.id).slice(0, 4);

    if (items.length === 0) {
      container.parentElement?.classList.add('hidden');
      return;
    }

    container.innerHTML = items.map(p => `
      <div class="product-card" style="background:#FFF; border-radius:12px; overflow:hidden; border:1px solid #E7E2DA; display:flex; flex-direction:column;">
        <a href="/product/${p.slug}" style="display:block; height:240px; position:relative; overflow:hidden; background:#FAF8F5;">
          <img src="${window.optimizeImg ? window.optimizeImg(p.primary_image, 500, 75) : (p.primary_image || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500&auto=format&fit=crop&q=75')}" alt="${p.name}" class="img-zoom" loading="lazy" decoding="async" style="width:100%; height:100%; object-fit:cover;">
        </a>
        <div style="padding:14px; display:flex; flex-direction:column; flex:1; justify-content:space-between;">
          <a href="/product/${p.slug}" style="font-size:0.875rem; font-weight:500; color:#121212; margin-bottom:6px; display:-webkit-box; -webkit-line-clamp:1; -webkit-box-orient:vertical; overflow:hidden;">${p.name}</a>
          <div style="font-weight:700; font-size:0.938rem;">${window.Store.formatPrice(p.price)}</div>
        </div>
      </div>
    `).join('');
  } catch (e) {
    console.warn('Error loading similar products:', e);
  }
}

window.openSizeGuide = () => {
  const isRu = window.I18N?.currentLang === 'ru';
  alert(isRu ? 
    "Таблица размеров:\nXS: ОГ 82-86, ОТ 62-66, ОБ 88-92\nS: ОГ 86-90, ОТ 66-70, ОБ 92-96\nM: ОГ 90-94, ОТ 70-74, ОБ 96-100\nL: ОГ 94-98, ОТ 74-78, ОБ 100-104" : 
    "Таблиця розмірів:\nXS: ОГ 82-86, ОТ 62-66, ОБ 88-92\nS: ОГ 86-90, ОТ 66-70, ОБ 92-96\nM: ОГ 90-94, ОТ 70-74, ОБ 96-100\nL: ОГ 94-98, ОТ 74-78, ОБ 100-104"
  );
};

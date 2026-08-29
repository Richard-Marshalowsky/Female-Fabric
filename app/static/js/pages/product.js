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
});

async function loadProductDetail(slug) {
  const loader = document.getElementById('product-loader');
  const content = document.getElementById('product-content');

  try {
    const product = await window.API.getProductDetail(slug);
    currentProduct = product;

    if (loader) loader.classList.add('hidden');
    if (content) content.classList.remove('hidden');

    document.title = `${product.name} — Female-Fabric`;

    const breadcrumbCategory = document.getElementById('product-bc-category');
    const breadcrumbName = document.getElementById('product-bc-name');
    if (breadcrumbCategory) {
      breadcrumbCategory.textContent = (window.I18N ? window.I18N.t('cat_' + product.category_slug) : null) || product.category_name || 'Каталог';
      breadcrumbCategory.href = `/catalog?category=${product.category_slug}`;
    }
    if (breadcrumbName) breadcrumbName.textContent = product.name;

    renderProductGallery(product);

    document.getElementById('product-title').textContent = product.name;
    document.getElementById('product-sku').textContent = `Артикул: ${product.sku}`;
    document.getElementById('product-price').textContent = window.Store.formatPrice(product.price);
    
    const oldPriceEl = document.getElementById('product-old-price');
    const discountEl = document.getElementById('product-discount-badge');
    if (product.old_price && product.old_price > product.price) {
      oldPriceEl.textContent = window.Store.formatPrice(product.old_price);
      oldPriceEl.classList.remove('hidden');
      if (discountEl && product.discount_percent) {
        discountEl.textContent = `-${product.discount_percent}%`;
        discountEl.classList.remove('hidden');
      }
    } else {
      if (oldPriceEl) oldPriceEl.classList.add('hidden');
      if (discountEl) discountEl.classList.add('hidden');
    }

    if (product.sizes && product.sizes.length > 0) selectedSize = product.sizes[0];
    if (product.colors && product.colors.length > 0) selectedColor = product.colors[0].name;

    renderSizeSelector(product);
    renderColorSelector(product);
    updateStockDisplay(product);

    document.getElementById('product-description').textContent = product.description || '';
    
    if (product.details) {
      const specsList = document.getElementById('product-specs-list');
      if (specsList) {
        specsList.innerHTML = Object.entries(product.details).map(([k, v]) => {
          let label = k;
          if (k === 'composition') label = 'Склад';
          else if (k === 'fit') label = 'Посадка та крій';
          else if (k === 'season') label = 'Сезон';
          else if (k === 'care') label = 'Догляд';
          return `
            <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #F0EDE8; font-size:0.875rem;">
              <span style="color:#78716C;">${label}:</span>
              <strong style="text-align:right; max-width:60%; font-weight:500;">${v}</strong>
            </div>
          `;
        }).join('');
      }
    }

    const favBtn = document.getElementById('product-fav-btn');
    if (favBtn) {
      favBtn.classList.toggle('active', product.is_favorite);
      favBtn.onclick = async () => {
        const res = await window.Store.toggleFavorite(product.id);
        favBtn.classList.toggle('active', res);
      };
    }

    if (product.related_products && product.related_products.length > 0) {
      const relatedContainer = document.getElementById('product-related-grid');
      if (relatedContainer) {
        relatedContainer.innerHTML = product.related_products.map(p => `
          <div class="product-card" style="background:var(--color-surface); border-radius:12px; overflow:hidden; border:1px solid var(--color-border); display:flex; flex-direction:column;">
            <a href="/product/${p.slug}" style="display:block; height:240px; position:relative; overflow:hidden; background:#F3EFEA;">
              <img src="${p.primary_image}" alt="${p.name}" class="img-zoom" style="width:100%; height:100%; object-fit:cover;">
            </a>
            <div style="padding:12px;">
              <a href="/product/${p.slug}" style="font-size:0.875rem; font-weight:500; display:block; margin-bottom:6px; color:#121212; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${p.name}</a>
              <div style="font-weight:700; font-size:0.938rem;">${window.Store.formatPrice(p.price)}</div>
            </div>
          </div>
        `).join('');
      }
    }

  } catch (err) {
    if (loader) loader.innerHTML = '<div style="color:#B91C1C; text-align:center; padding:40px;">Товар не знайдено</div>';
    console.error(err);
  }
}

function renderProductGallery(product) {
  const mainImg = document.getElementById('product-main-image');
  const thumbsContainer = document.getElementById('product-thumbnails-container');
  const images = product.images && product.images.length > 0 ? product.images : [product.primary_image];

  if (mainImg) mainImg.src = images[0];

  if (thumbsContainer) {
    thumbsContainer.innerHTML = images.map((imgUrl, idx) => `
      <button type="button" onclick="switchMainImage('${imgUrl}', this)" class="product-thumb-btn ${idx === 0 ? 'active' : ''}" style="width:70px; height:90px; border-radius:6px; overflow:hidden; border:2px solid ${idx === 0 ? '#121212' : 'transparent'}; cursor:pointer; background:#F3EFEA; padding:0;">
        <img src="${imgUrl}" alt="Thumbnail ${idx}" style="width:100%; height:100%; object-fit:cover;">
      </button>
    `).join('');
  }
}

window.switchMainImage = (url, btn) => {
  const mainImg = document.getElementById('product-main-image');
  if (mainImg) mainImg.src = url;
  document.querySelectorAll('.product-thumb-btn').forEach(b => b.style.borderColor = 'transparent');
  if (btn) btn.style.borderColor = '#121212';
};

function renderSizeSelector(product) {
  const container = document.getElementById('product-sizes-selector');
  if (!container || !product.sizes) return;

  container.innerHTML = product.sizes.map(s => `
    <button type="button" class="size-badge ${selectedSize === s ? 'active' : ''}" onclick="selectProductSize('${s}', this)">
      ${s}
    </button>
  `).join('');
}

window.selectProductSize = (size, btn) => {
  selectedSize = size;
  document.querySelectorAll('#product-sizes-selector .size-badge').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  updateStockDisplay(currentProduct);
};

function renderColorSelector(product) {
  const container = document.getElementById('product-colors-selector');
  const colorNameLabel = document.getElementById('product-selected-color-name');

  if (!container || !product.colors) return;
  if (colorNameLabel && selectedColor) colorNameLabel.textContent = selectedColor;

  container.innerHTML = product.colors.map(c => `
    <button type="button" class="color-dot ${selectedColor === c.name ? 'active' : ''}" style="background:${c.code}; width:24px; height:24px;" title="${c.name}" onclick="selectProductColor('${c.name}', this)">
    </button>
  `).join('');
}

window.selectProductColor = (colorName, btn) => {
  selectedColor = colorName;
  document.querySelectorAll('#product-colors-selector .color-dot').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const colorNameLabel = document.getElementById('product-selected-color-name');
  if (colorNameLabel) colorNameLabel.textContent = colorName;
  updateStockDisplay(currentProduct);
};

function updateStockDisplay(product) {
  const stockEl = document.getElementById('product-stock-status');
  if (!stockEl || !product) return;

  let stock = 10;
  if (product.variants) {
    const v = product.variants.find(item => 
      (!selectedSize || item.size === selectedSize) && 
      (!selectedColor || item.color === selectedColor)
    );
    if (v) stock = v.stock;
  }

  if (stock > 5) {
    stockEl.innerHTML = `<span style="color:#15803D; display:flex; align-items:center; gap:6px; font-size:0.875rem;"><span style="width:8px; height:8px; background:#15803D; border-radius:50%;"></span> В наявності (${stock} шт.)</span>`;
  } else if (stock > 0) {
    stockEl.innerHTML = `<span style="color:#D97706; display:flex; align-items:center; gap:6px; font-size:0.875rem;"><span style="width:8px; height:8px; background:#D97706; border-radius:50%;"></span> Залишилося мало (усього ${stock} шт.)</span>`;
  } else {
    stockEl.innerHTML = `<span style="color:#B91C1C; display:flex; align-items:center; gap:6px; font-size:0.875rem;"><span style="width:8px; height:8px; background:#B91C1C; border-radius:50%;"></span> Немає в наявності</span>`;
  }
}

window.changeProductQty = (delta) => {
  selectedQuantity = Math.max(1, selectedQuantity + delta);
  const qtyEl = document.getElementById('product-qty-input');
  if (qtyEl) qtyEl.textContent = selectedQuantity;
};

window.handleAddToCart = async () => {
  if (!currentProduct) return;
  if (!selectedSize && currentProduct.sizes && currentProduct.sizes.length > 0) {
    window.Toast.warning('Будь ласка, оберіть розмір');
    return;
  }

  const btn = document.getElementById('add-to-cart-btn');
  try {
    if (btn) {
      btn.disabled = true;
      btn.textContent = 'Додавання...';
    }

    const updatedCart = await window.API.addToCart(
      currentProduct.id,
      selectedSize,
      selectedColor,
      selectedQuantity
    );

    window.Store.cart = updatedCart;
    window.Store.emit('cart:updated', updatedCart);
    window.Toast.success(`«${currentProduct.name}» додано в кошик`);
    window.Modal?.open('cart-drawer');
  } catch (err) {
    window.Toast.error(err.message || 'Не вдалося додати в кошик');
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = 'Додати в кошик';
    }
  }
};

window.openOneClickModal = () => {
  if (!selectedSize && currentProduct?.sizes?.length > 0) {
    window.Toast.warning('Будь ласка, оберіть розмір');
    return;
  }
  const modalProdName = document.getElementById('one-click-prod-name');
  const modalProdSize = document.getElementById('one-click-prod-size');
  const modalProdPrice = document.getElementById('one-click-prod-price');

  if (modalProdName) modalProdName.textContent = currentProduct.name;
  if (modalProdSize) modalProdSize.textContent = `Размер: ${selectedSize || 'Standard'}${selectedColor ? ` | Цвет: ${selectedColor}` : ''}`;
  if (modalProdPrice) modalProdPrice.textContent = window.Store.formatPrice(currentProduct.price);

  window.Modal?.open('one-click-modal');
};

window.submitOneClickOrder = async (e) => {
  e.preventDefault();
  const phone = document.getElementById('one-click-phone').value;
  const name = document.getElementById('one-click-name').value;

  try {
    const orderData = {
      first_name: name,
      last_name: 'Покупець',
      phone: phone,
      email: 'oneclick@female-fabric.ua',
      city: 'Київ',
      address: 'Уточнити при дзвінку менеджера (Швидке замовлення в 1 клік)',
      delivery_method: 'Нова Пошта (Кур'єр)',
      payment_method: 'Післяплата',
      notes: `Швидке замовлення товару: ${currentProduct.name} (${selectedSize}, ${selectedColor})`,
      items: [{
        product_id: currentProduct.id,
        size: selectedSize,
        color: selectedColor,
        quantity: selectedQuantity,
        price: currentProduct.price
      }]
    };

    const res = await window.API.createOrder(orderData);
    window.Modal?.close('one-click-modal');
    window.location.href = `/order-success?order_number=${res.order_number}`;
  } catch (err) {
    window.Toast.error(err.message || 'Помилка оформлення замовлення');
  }
};

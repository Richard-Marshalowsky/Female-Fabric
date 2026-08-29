// Cart Page JavaScript
document.addEventListener('DOMContentLoaded', () => {
  renderCartPage(window.Store.cart);
  window.Store.on('cart:updated', (cart) => {
    renderCartPage(cart);
  });
});

function renderCartPage(cart) {
  const itemsContainer = document.getElementById('cart-page-items');
  const emptyState = document.getElementById('cart-page-empty');
  const contentBlock = document.getElementById('cart-page-content');
  const subtotalEl = document.getElementById('cart-page-subtotal');
  const discountEl = document.getElementById('cart-page-discount');
  const discountRow = document.getElementById('cart-page-discount-row');
  const deliveryEl = document.getElementById('cart-page-delivery');
  const totalEl = document.getElementById('cart-page-total');
  const freeShipBadge = document.getElementById('cart-page-freeship-badge');

  if (!cart || !cart.items || cart.items.length === 0) {
    if (emptyState) emptyState.classList.remove('hidden');
    if (contentBlock) contentBlock.classList.add('hidden');
    return;
  }

  if (emptyState) emptyState.classList.add('hidden');
  if (contentBlock) contentBlock.classList.remove('hidden');

  if (subtotalEl) subtotalEl.textContent = window.Store.formatPrice(cart.subtotal);
  if (totalEl) totalEl.textContent = window.Store.formatPrice(cart.total);

  if (discountRow) {
    if (cart.discount > 0) {
      discountRow.classList.remove('hidden');
      if (discountEl) discountEl.textContent = `-${window.Store.formatPrice(cart.discount)}`;
    } else {
      discountRow.classList.add('hidden');
    }
  }

  if (deliveryEl) {
    deliveryEl.textContent = cart.delivery_fee === 0 ? 'Безкоштовно' : window.Store.formatPrice(cart.delivery_fee);
  }

  if (freeShipBadge) {
    if (cart.amount_left_for_free_delivery > 0) {
      freeShipBadge.innerHTML = `Добавьте товаров на <strong>${window.Store.formatPrice(cart.amount_left_for_free_delivery)}</strong> для бесплатной доставки`;
    } else {
      freeShipBadge.innerHTML = `<span style="color:#15803D; font-weight:600;">✓ Вы получили бесплатную доставку!</span>`;
    }
  }

  if (itemsContainer) {
    itemsContainer.innerHTML = cart.items.map(item => `
      <div style="display:flex; gap:16px; padding:20px; border-bottom:1px solid #E5E0D8; background:#FFF; border-radius:8px; margin-bottom:12px;">
        <img src="${item.image_url || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=300'}" alt="${item.product_name}" style="width:90px; height:120px; object-fit:cover; border-radius:6px;">
        <div style="flex:1; display:flex; flex-direction:column; justify-content:space-between;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
              <a href="/product/${item.product_slug}" style="font-size:1.063rem; font-weight:600; color:#121212;">${item.product_name}</a>
              <div style="font-size:0.875rem; color:#78716C; margin-top:4px;">
                ${item.size ? `Розмір: <strong>${item.size}</strong>` : ''}
                ${item.color ? ` | Колір: <strong>${item.color}</strong>` : ''}
              </div>
            </div>
            <button onclick="window.removeCartItem(${item.id})" style="background:none; border:none; color:#A8A29E; cursor:pointer; font-size:1.25rem;" title="Видалити">✕</button>
          </div>

          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px;">
            <div style="display:flex; align-items:center; border:1px solid #E5E0D8; border-radius:6px; background:#FAF8F5;">
              <button onclick="window.changeCartQty(${item.id}, ${item.quantity - 1})" style="padding:4px 12px; border:none; background:none; cursor:pointer; font-weight:bold;">-</button>
              <span style="padding:0 10px; font-weight:600; font-size:0.938rem;">${item.quantity}</span>
              <button onclick="window.changeCartQty(${item.id}, ${item.quantity + 1})" style="padding:4px 12px; border:none; background:none; cursor:pointer; font-weight:bold;">+</button>
            </div>

            <div style="text-align:right;">
              <div style="font-size:1.125rem; font-weight:700; color:#121212;">${window.Store.formatPrice(item.total_price)}</div>
              ${item.old_price ? `<div style="font-size:0.813rem; text-decoration:line-through; color:#A8A29E;">${window.Store.formatPrice(item.old_price * item.quantity)}</div>` : ''}
            </div>
          </div>
        </div>
      </div>
    `).join('');
  }
}

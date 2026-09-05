// Checkout Page JavaScript
document.addEventListener('DOMContentLoaded', async () => {
  // 1. If store already has cart or local backup exists, render immediately
  if (window.Store && window.Store.cart && window.Store.cart.items && window.Store.cart.items.length > 0) {
    renderCheckoutSummary(window.Store.cart);
  } else {
    try {
      const backup = JSON.parse(localStorage.getItem('ff_cart_backup') || '{}');
      if (backup && backup.items && backup.items.length > 0) {
        renderCheckoutSummary(backup);
      }
    } catch(e) {}
  }

  // 2. Listen for cart updates
  window.Store.on('cart:updated', (cart) => {
    renderCheckoutSummary(cart);
  });

  // 3. Ensure store is initialized and cart is verified with backend
  if (window.Store) {
    await window.Store.refreshCart();
    renderCheckoutSummary(window.Store.cart);
  }

  if (window.Store.user) {
    prefillUserData(window.Store.user);
  } else {
    window.Store.on('auth:changed', (user) => {
      if (user) prefillUserData(user);
    });
  }

  const checkoutForm = document.getElementById('checkout-form');
  if (checkoutForm) {
    checkoutForm.addEventListener('submit', handleCheckoutSubmit);
  }
});

async function prefillUserData(user) {
  const nameParts = (user.full_name || '').split(' ');
  const firstNameInput = document.getElementById('checkout-first-name');
  const lastNameInput = document.getElementById('checkout-last-name');
  const emailInput = document.getElementById('checkout-email');
  const phoneInput = document.getElementById('checkout-phone');

  if (firstNameInput && !firstNameInput.value) firstNameInput.value = nameParts[0] || '';
  if (lastNameInput && !lastNameInput.value) lastNameInput.value = nameParts.slice(1).join(' ') || '';
  if (emailInput && !emailInput.value) emailInput.value = user.email || '';
  if (phoneInput && !phoneInput.value) phoneInput.value = user.phone || '';

  try {
    const addresses = await window.API.getAddresses();
    const defaultAddr = addresses.find(a => a.is_default) || addresses[0];
    if (defaultAddr) {
      const cityInput = document.getElementById('checkout-city');
      const addressInput = document.getElementById('checkout-address');
      if (cityInput && !cityInput.value) cityInput.value = defaultAddr.city;
      if (addressInput && !addressInput.value) addressInput.value = defaultAddr.address;
    }
  } catch (e) {
    console.warn(e);
  }
}

function renderCheckoutSummary(cart) {
  const itemsContainer = document.getElementById('checkout-items-list') || document.getElementById('checkout-items-summary');
  const subtotalEl = document.getElementById('checkout-subtotal');
  const discountEl = document.getElementById('checkout-discount');
  const discountRow = document.getElementById('checkout-discount-row');
  const deliveryEl = document.getElementById('checkout-delivery');
  const totalEl = document.getElementById('checkout-total');

  if (!cart || !cart.items || cart.items.length === 0) {
    if (itemsContainer) itemsContainer.innerHTML = '<div style="color:#78716C; padding:12px 0;">Кошик порожній</div>';
    if (subtotalEl) subtotalEl.textContent = '0 ₴';
    if (totalEl) totalEl.textContent = '0 ₴';
    return;
  }

  if (itemsContainer) {
    itemsContainer.innerHTML = cart.items.map(item => `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; font-size:0.875rem;">
        <div style="display:flex; gap:10px; align-items:center; max-width:70%;">
          <img src="${window.optimizeImg ? window.optimizeImg(item.image_url, 120, 75) : (item.image_url || 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=120&auto=format&fit=crop&q=75')}" alt="${item.product_name}" loading="lazy" decoding="async" style="width:40px; height:50px; object-fit:cover; border-radius:4px;">
          <div>
            <div style="font-weight:500; line-height:1.2;">${item.product_name}</div>
            <div style="color:#78716C; font-size:0.75rem;">${item.sku ? `<span style="color:#78716C; font-weight:500;">Арт: ${item.sku}</span> • ` : ''}${item.size ? `Розмір: ${item.size}` : ''}${item.color ? ` • ${item.color}` : ''} • ${item.quantity} шт.</div>
          </div>
        </div>
        <div style="font-weight:600;">${window.Store.formatPrice(item.total_price)}</div>
      </div>
    `).join('');
  }

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
}

async function handleCheckoutSubmit(e) {
  e.preventDefault();
  const form = e.target;
  const submitBtn = form.querySelector('button[type="submit"]');

  const deliveryMethod = form.querySelector('input[name="delivery_method"]:checked')?.value || "Нова Пошта (Кур'єр)";
  const paymentMethod = form.querySelector('input[name="payment_method"]:checked')?.value || 'Карткою онлайн';

  const orderData = {
    first_name: document.getElementById('checkout-first-name').value.trim(),
    last_name: document.getElementById('checkout-last-name').value.trim(),
    phone: document.getElementById('checkout-phone').value.trim(),
    email: document.getElementById('checkout-email').value.trim(),
    city: document.getElementById('checkout-city').value.trim(),
    address: document.getElementById('checkout-address').value.trim(),
    delivery_method: deliveryMethod,
    payment_method: paymentMethod,
    notes: document.getElementById('checkout-notes')?.value.trim() || null,
    items: (window.Store.cart?.items || []).map(it => ({
      product_id: it.product_id,
      variant_id: it.variant_id || null,
      size: it.size || null,
      color: it.color || null,
      quantity: it.quantity,
      price: it.price
    }))
  };

  try {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Оформление заказа...';

    const res = await window.API.createOrder(orderData);
    try {
      const userEmail = orderData.email.toLowerCase();
      const existing = JSON.parse(localStorage.getItem('ff_orders_' + userEmail) || '[]');
      const orderRecord = {
        order_number: res.order_number,
        created_at: new Date().toISOString(),
        status: 'Новий',
        total_amount: res.total_amount,
        subtotal_amount: res.subtotal_amount,
        delivery_fee: res.delivery_fee,
        discount_amount: res.discount_amount || 0,
        delivery_method: orderData.delivery_method,
        payment_method: orderData.payment_method,
        city: orderData.city,
        address: orderData.address,
        items: (window.Store.cart?.items || []).map(it => ({
          product_name: it.product_name,
          sku: it.sku || '',
          size: it.size,
          color: it.color,
          quantity: it.quantity,
          price: it.price,
          total_price: it.total_price || (it.price * it.quantity),
          image_url: it.image_url
        }))
      };
      existing.unshift(orderRecord);
      localStorage.setItem('ff_orders_' + userEmail, JSON.stringify(existing));
      localStorage.removeItem('ff_cart_backup');
    } catch(e){}
    await window.Store.refreshCart();
    window.location.href = `/order-success?order_number=${res.order_number}`;
  } catch (err) {
    window.Toast.error(err.message || 'Ошибка оформления заказа');
    submitBtn.disabled = false;
    submitBtn.textContent = 'Підтвердити замовлення';
  }
}

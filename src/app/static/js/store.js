// Global Reactive State Store for Female-Fabric
class Store {
  constructor() {
    this.user = null;
    this.cart = {
      items: [],
      total_quantity: 0,
      subtotal: 0,
      discount: 0,
      delivery_fee: 0,
      total: 0
    };
    this.favorites = new Set();
    this.listeners = {};
  }

  on(event, callback) {
    if (!this.listeners[event]) this.listeners[event] = [];
    this.listeners[event].push(callback);
  }

  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(cb => cb(data));
    }
  }

  async init() {
    // 1. Check user token & profile
    const token = window.API.getToken();
    if (token) {
      try {
        const userData = await window.API.getMe();
        this.setUser(userData);
        await this.loadFavorites();
      } catch (e) {
        console.warn('Could not restore user session:', e);
        this.setUser(null);
      }
    } else {
      this.setUser(null);
    }

    // 2. Fetch initial cart
    await this.refreshCart();
  }

  setUser(user) {
    this.user = user;
    this.emit('auth:changed', this.user);
  }

  async refreshCart() {
    try {
      const cartData = await window.API.getCart();
      this.cart = cartData;
      this.emit('cart:updated', this.cart);
    } catch (e) {
      console.error('Failed to load cart:', e);
    }
  }

  async loadFavorites() {
    if (!this.user) {
      this.favorites.clear();
      this.emit('fav:updated', this.favorites);
      return;
    }
    try {
      const favList = await window.API.getFavorites();
      this.favorites = new Set(favList.map(p => p.id));
      this.emit('fav:updated', this.favorites);
    } catch (e) {
      console.warn('Failed to load favorites:', e);
    }
  }

  isFavorite(productId) {
    return this.favorites.has(productId);
  }

  async toggleFavorite(productId) {
    if (!this.user) {
      window.Toast.info('Войдите или зарегистрируйтесь, чтобы сохранять товары в избранное');
      window.Modal?.open('auth-modal');
      return false;
    }
    try {
      const res = await window.API.toggleFavorite(productId);
      if (res.is_favorite) {
        this.favorites.add(productId);
        window.Toast.success('Добавлено в избранное');
      } else {
        this.favorites.delete(productId);
        window.Toast.info('Удалено из избранного');
      }
      this.emit('fav:updated', this.favorites);
      return res.is_favorite;
    } catch (err) {
      window.Toast.error(err.message || 'Не удалось обновить избранное');
      return false;
    }
  }

  formatPrice(price) {
    if (price === undefined || price === null) return '0 ₽';
    return Number(price).toLocaleString('ru-RU') + ' ₽';
  }
}

window.Store = new Store();

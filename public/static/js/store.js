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
    this.favoriteProductsCache = [];
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
      } catch (e) {
        console.warn('Could not restore user session:', e);
        this.setUser(null);
      }
    } else {
      this.setUser(null);
    }

    // 2. Load favorites (guest or user)
    await this.loadFavorites();

    // 3. Fetch initial cart
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
    if (this.user) {
      try {
        const favList = await window.API.getFavorites();
        this.favoriteProductsCache = favList;
        this.favorites = new Set(favList.map(p => p.id));
      } catch (e) {
        console.warn('Failed to load user favorites:', e);
      }
    } else {
      try {
        const saved = localStorage.getItem('female_fabric_fav_ids');
        const ids = saved ? JSON.parse(saved) : [];
        this.favorites = new Set(ids);
      } catch (e) {
        this.favorites = new Set();
      }
    }
    this.emit('fav:updated', Array.from(this.favorites));
  }

  isFavorite(productId) {
    return this.favorites.has(Number(productId));
  }

  async toggleFavorite(productId, productObj = null) {
    const id = Number(productId);
    let isNowFav = false;

    if (this.user) {
      try {
        const res = await window.API.toggleFavorite(id);
        isNowFav = res.is_favorite;
        if (isNowFav) {
          this.favorites.add(id);
          if (productObj) this.favoriteProductsCache.push(productObj);
        } else {
          this.favorites.delete(id);
          this.favoriteProductsCache = this.favoriteProductsCache.filter(p => p.id !== id);
        }
      } catch (err) {
        console.error('Toggle favorite API error:', err);
      }
    } else {
      // Guest localStorage support
      if (this.favorites.has(id)) {
        this.favorites.delete(id);
        isNowFav = false;
        this.favoriteProductsCache = this.favoriteProductsCache.filter(p => p.id !== id);
      } else {
        this.favorites.add(id);
        isNowFav = true;
        if (productObj) this.favoriteProductsCache.push(productObj);
      }
      localStorage.setItem('female_fabric_fav_ids', JSON.stringify(Array.from(this.favorites)));
    }

    this.emit('fav:updated', Array.from(this.favorites));
    return isNowFav;
  }

  async getFavoriteProducts() {
    if (this.user) {
      try {
        const favList = await window.API.getFavorites();
        this.favoriteProductsCache = favList;
        return favList;
      } catch (e) {
        return this.favoriteProductsCache;
      }
    } else {
      const ids = Array.from(this.favorites);
      if (ids.length === 0) return [];
      try {
        // Fetch products list and filter
        const res = await window.API.getProducts({ limit: 50 });
        return res.items.filter(p => this.favorites.has(p.id));
      } catch (e) {
        return this.favoriteProductsCache;
      }
    }
  }

  formatPrice(price) {
    if (price === undefined || price === null) return '0 ₴';
    return Number(price).toLocaleString('uk-UA') + ' ₴';
  }
}

window.Store = new Store();

// Centralized API Client for Female-Fabric
class ApiClient {
  constructor() {
    this.baseUrl = '';
    this.sessionKey = 'ff_session_id';
    this.tokenKey = 'ff_access_token';
    this.cache = new Map();
    this.cacheTTL = 120000; // 2 minutes RAM cache for instant UI response
  }

  getSessionId() {
    let sid = localStorage.getItem(this.sessionKey);
    if (!sid) {
      sid = 'sess_' + Math.random().toString(36).substring(2) + Date.now().toString(36);
      localStorage.setItem(this.sessionKey, sid);
    }
    return sid;
  }

  getToken() {
    return localStorage.getItem(this.tokenKey);
  }

  setToken(token) {
    if (token) {
      localStorage.setItem(this.tokenKey, token);
    } else {
      localStorage.removeItem(this.tokenKey);
    }
    this.cache.clear();
  }

  async request(endpoint, options = {}) {
    const method = (options.method || 'GET').toUpperCase();
    const isGet = method === 'GET';
    const useCache = isGet && options.useCache !== false;

    // Check RAM cache for GET requests
    if (useCache && this.cache.has(endpoint)) {
      const cached = this.cache.get(endpoint);
      if (Date.now() - cached.timestamp < this.cacheTTL) {
        return cached.data;
      }
    }

    const headers = options.headers || {};
    
    // Add Authorization Header if available
    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    // Add Session ID Header for guest cart
    headers['X-Session-ID'] = this.getSessionId();

    if (!(options.body instanceof FormData) && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json';
    }

    const config = {
      ...options,
      headers
    };

    try {
      const res = await fetch(endpoint, config);
      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        let errorMsg = data.detail || 'Произошла ошибка при обработке запроса';
        if (Array.isArray(data.detail)) {
          errorMsg = data.detail.map(d => `${d.loc ? d.loc.join('.') + ': ' : ''}${d.msg}`).join(', ');
        }
        
        // Handle 401 Unauthorized
        if (res.status === 401) {
          if (this.getToken()) {
            this.setToken(null);
            window.Store?.setUser(null);
          }
        }

        const error = new Error(errorMsg);
        error.status = res.status;
        error.data = data;
        throw error;
      }

      // Store in RAM cache if GET, or clear cache if mutating
      if (useCache) {
        this.cache.set(endpoint, { timestamp: Date.now(), data });
      } else if (!isGet) {
        this.cache.clear();
      }

      return data;
    } catch (err) {
      console.error(`API Error [${endpoint}]:`, err);
      throw err;
    }
  }

  // Auth
  async register(userData) {
    const data = await this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
    this.setToken(data.access_token);
    return data;
  }

  async login(credentials) {
    const data = await this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    });
    this.setToken(data.access_token);
    return data;
  }

  async logout() {
    try {
      await this.request('/api/auth/logout', { method: 'POST' });
    } finally {
      this.setToken(null);
    }
  }

  async getMe() {
    return this.request('/api/auth/me');
  }

  async forgotPassword(email) {
    return this.request('/api/auth/forgot-password', {
      method: 'POST',
      body: JSON.stringify({ email })
    });
  }

  async resetPassword(token, newPassword) {
    return this.request('/api/auth/reset-password', {
      method: 'POST',
      body: JSON.stringify({ token, new_password: newPassword })
    });
  }

  // Categories & Products
  async getCategories() {
    return this.request('/api/categories');
  }

  async getProducts(params = {}) {
    const query = new URLSearchParams();
    for (const [k, v] of Object.entries(params)) {
      if (v !== undefined && v !== null && v !== '') {
        query.append(k, v);
      }
    }
    const qs = query.toString();
    return this.request(`/api/products${qs ? '?' + qs : ''}`);
  }

  async getFeaturedProducts(limit = 8) {
    const data = await this.request(`/api/products?is_featured=true&limit=${limit}`);
    return data.items || data;
  }

  async getNewProducts(limit = 8) {
    const data = await this.request(`/api/products?is_new=true&limit=${limit}`);
    return data.items || data;
  }

  async getProductDetail(slugOrId) {
    return this.request(`/api/products/${slugOrId}`);
  }

  // Cart
  async getCart() {
    return this.request('/api/cart');
  }

  async addToCart(productId, size, color, quantity = 1, variantId = null) {
    return this.request('/api/cart/items', {
      method: 'POST',
      body: JSON.stringify({
        product_id: productId,
        size,
        color,
        quantity,
        variant_id: variantId
      })
    });
  }

  async updateCartItem(itemId, quantity, size = null, color = null) {
    return this.request(`/api/cart/items/${itemId}`, {
      method: 'PATCH',
      body: JSON.stringify({ quantity, size, color })
    });
  }

  async removeFromCart(itemId) {
    return this.request(`/api/cart/items/${itemId}`, { method: 'DELETE' });
  }

  async clearCart() {
    return this.request('/api/cart', { method: 'DELETE' });
  }

  async syncCart(items) {
    return this.request('/api/cart/sync', {
      method: 'POST',
      body: JSON.stringify({ items })
    });
  }

  // Checkout
  async createOrder(orderData) {
    return this.request('/api/checkout', {
      method: 'POST',
      body: JSON.stringify(orderData)
    });
  }

  async getOrderByNumber(orderNumber) {
    return this.request(`/api/checkout/orders/${orderNumber}`);
  }

  // Profile & Addresses
  async getProfile() {
    return this.request('/api/profile');
  }

  async updateProfile(profileData) {
    return this.request('/api/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData)
    });
  }

  async changePassword(oldPassword, newPassword) {
    return this.request('/api/profile/password', {
      method: 'POST',
      body: JSON.stringify({ old_password: oldPassword, new_password: newPassword })
    });
  }

  async getAddresses() {
    return this.request('/api/profile/addresses');
  }

  async addAddress(addressData) {
    return this.request('/api/profile/addresses', {
      method: 'POST',
      body: JSON.stringify(addressData)
    });
  }

  async deleteAddress(addressId) {
    return this.request(`/api/profile/addresses/${addressId}`, { method: 'DELETE' });
  }

  async getOrders() {
    return this.request('/api/profile/orders');
  }

  // Favorites
  async getFavorites() {
    return this.request('/api/favorites');
  }

  async toggleFavorite(productId) {
    return this.request(`/api/favorites/${productId}`, { method: 'POST' });
  }

  // Admin APIs
  async getAdminStats() {
    return this.request('/api/admin/stats');
  }

  async getAdminProducts(params = {}) {
    const query = new URLSearchParams(params);
    const qs = query.toString();
    return this.request(`/api/admin/products${qs ? '?' + qs : ''}`);
  }

  async createAdminProduct(productData) {
    return this.request('/api/admin/products', {
      method: 'POST',
      body: JSON.stringify(productData)
    });
  }

  async updateAdminProduct(productId, productData) {
    return this.request(`/api/admin/products/${productId}`, {
      method: 'PUT',
      body: JSON.stringify(productData)
    });
  }

  async toggleAdminProductStatus(productId) {
    return this.request(`/api/admin/products/${productId}/status`, { method: 'PATCH' });
  }

  async deleteAdminProduct(productId) {
    return this.request(`/api/admin/products/${productId}`, { method: 'DELETE' });
  }

  async getAdminCategories() {
    return this.request('/api/admin/categories');
  }

  async createAdminCategory(categoryData) {
    return this.request('/api/admin/categories', {
      method: 'POST',
      body: JSON.stringify(categoryData)
    });
  }

  async updateAdminCategory(categoryId, categoryData) {
    return this.request(`/api/admin/categories/${categoryId}`, {
      method: 'PUT',
      body: JSON.stringify(categoryData)
    });
  }

  async deleteAdminCategory(categoryId) {
    return this.request(`/api/admin/categories/${categoryId}`, { method: 'DELETE' });
  }

  async getAdminOrders(params = {}) {
    const query = new URLSearchParams(params);
    const qs = query.toString();
    return this.request(`/api/admin/orders${qs ? '?' + qs : ''}`);
  }

  async getAdminOrderDetail(orderId) {
    return this.request(`/api/admin/orders/${orderId}`);
  }

  async updateAdminOrderStatus(orderId, status) {
    return this.request(`/api/admin/orders/${orderId}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status })
    });
  }

  async getAdminUsers() {
    return this.request('/api/admin/users');
  }

  async toggleAdminUserStatus(userId) {
    return this.request(`/api/admin/users/${userId}/status`, { method: 'PATCH' });
  }

  async uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);
    return this.request('/api/admin/upload', {
      method: 'POST',
      body: formData
    });
  }
}

window.API = new ApiClient();

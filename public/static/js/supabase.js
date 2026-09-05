// Supabase Client and Authentication Service for Female-Fabric
(function() {
  const supabaseUrl = window.__SUPABASE_URL__|| 
                      document.querySelector('meta[name="supabase-url"]')?.content || 
                      localStorage.getItem('ff_supabase_url') || 
                      '';

  const supabaseAnonKey = window.__SUPABASE_ANON_KEY__ || 
                          document.querySelector('meta[name="supabase-anon-key"]')?.content || 
                          localStorage.getItem('ff_supabase_anon_key') || 
                          '';

  let client = null;

  function initClient(url, key) {
    const finalUrl = url || supabaseUrl;
    const finalKey = key || supabaseAnonKey;

    if (finalUrl && finalKey && window.supabase && window.supabase.createClient) {
      try {
        client = window.supabase.createClient(finalUrl, finalKey, {
          auth: {
            persistSession: true,
            autoRefreshToken: true,
            detectSessionInUrl: true
          }
        });
        window.supabaseClient = client;
        console.log('[Supabase] Client initialized');
      } catch (e) {
        console.error('[Supabase] Initialization error:', e);
      }
    }
    return client;
  }


  if (window.supabase) {
    initClient();
  } else {
    window.addEventListener('load', () => {
      if (window.supabase && !client) {
        initClient();
      }
    });
  }

  window.SupabaseAuth = {
    isConfigured: () => Boolean(client),

    getClient: () => client || initClient(),

    setCredentials: (url, anonKey) => {
      localStorage.setItem('ff_supabase_url', url);
      localStorage.setItem('ff_supabase_anon_key', anonKey);
      return initClient(url, anonKey);
    },

    async signUp(email, password, metadata = {}) {
      const sb = this.getClient();
      if (!sb) {
        throw new Error('Supabase не налаштовано. Будь ласка, вкажіть Project URL та anon key.');
      }

      const { data, error } = await sb.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: metadata.full_name || '',
            phone: metadata.phone || ''
          }
        }
      });

      if (error) throw error;
      return data;
    },

    async signIn(email, password) {
      const sb = this.getClient();
      if (!sb) {
        throw new Error('Supabase не налаштовано. Будь ласка, вкажіть Project URL та anon key.');
      }

      const { data, error } = await sb.auth.signInWithPassword({
        email,
        password
      });

      if (error) throw error;
      return data;
    },

    async signOut() {
      const sb = this.getClient();
      if (sb) {
        await sb.auth.signOut().catch(() => {});
      }
      window.API.setToken(null);
      window.Store.setUser(null);
    },

    async getSession() {
      const sb = this.getClient();
      if (!sb) return null;
      const { data } = await sb.auth.getSession();
      return data?.session || null;
    },

    async getUser() {
      const sb = this.getClient();
      if (!sb) return null;
      const { data } = await sb.auth.getUser();
      return data?.user || null;
    },

    onAuthStateChange(callback) {
      const sb = this.getClient();
      if (!sb) return null;
      return sb.auth.onAuthStateChange((event, session) => {
        callback(event, session);
      });
    }
  };
})();

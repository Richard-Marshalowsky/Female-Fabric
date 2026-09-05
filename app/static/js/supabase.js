// Supabase Client and Authentication Service for Female-Fabric
(function() {
  const DEFAULT_SUPABASE_URL = 'https://ihoxwxdzrltvxamyhwsa.supabase.co';
  const DEFAULT_SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlob3h3eGR6cmx0dnhhbXlod3NhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc5MDEyODcsImV4cCI6MjEwMzQ3NzI4N30.g6Ff_TT_UKbSDyG-b4IDVjXId3-5Nc-0vxpDsb7Vt-s';

  const supabaseUrl = window.__SUPABASE_URL__ || 
                      document.querySelector('meta[name="supabase-url"]')?.content || 
                      localStorage.getItem('ff_supabase_url') || 
                      DEFAULT_SUPABASE_URL;

  const supabaseAnonKey = window.__SUPABASE_ANON_KEY__ || 
                          document.querySelector('meta[name="supabase-anon-key"]')?.content || 
                          localStorage.getItem('ff_supabase_anon_key') || 
                          DEFAULT_SUPABASE_ANON_KEY;

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
        console.log('[Supabase] Client initialized with project', finalUrl);
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
    isConfigured: () => Boolean(client || (supabaseUrl && supabaseAnonKey)),

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

// Language Switcher Component
document.addEventListener('DOMContentLoaded', () => {
  if (window.i18n) {
    window.i18n.updateDOM();
  }
  addLanguageSwitcher();
});

function addLanguageSwitcher() {
  const headerActions = document.querySelector('.site-header-actions') || 
                        document.querySelector('.site-header .flex.items-center.space-x-4') ||
                        document.querySelector('header .flex.items-center.space-x-4');
                        
  if (!headerActions) return;
  if (document.querySelector('.language-switcher')) return;

  const currentLang = window.i18n ? window.i18n.getLanguage() : 'uk';

  const switcher = document.createElement('div');
  switcher.className = 'language-switcher relative inline-block';
  switcher.innerHTML = `
    <button class="lang-toggle flex items-center space-x-1 px-2.5 py-1 text-xs font-medium border border-[#E7E2DA] rounded-full hover:border-neutral-900 transition bg-white text-neutral-800">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/>
        <line x1="2" y1="12" x2="22" y2="12"/>
        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
      </svg>
      <span class="current-lang uppercase">${currentLang}</span>
    </button>
    <div class="lang-dropdown hidden absolute right-0 mt-2 bg-white rounded-lg shadow-xl border border-[#E7E2DA] overflow-hidden z-50 min-w-[120px]">
      <button class="lang-option w-full px-3 py-2 text-left text-xs hover:bg-neutral-50 transition flex items-center justify-between" data-lang="uk">
        <span>🇺🇦 UA</span>
        <svg class="lang-check ${currentLang === 'uk' ? '' : 'hidden'} w-3.5 h-3.5 text-green-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
      </button>
      <button class="lang-option w-full px-3 py-2 text-left text-xs hover:bg-neutral-50 transition flex items-center justify-between" data-lang="ru">
        <span>🇷🇺 RU</span>
        <svg class="lang-check ${currentLang === 'ru' ? '' : 'hidden'} w-3.5 h-3.5 text-green-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
      </button>
    </div>
  `;

  headerActions.insertBefore(switcher, headerActions.firstChild);

  const toggle = switcher.querySelector('.lang-toggle');
  const dropdown = switcher.querySelector('.lang-dropdown');
  const options = switcher.querySelectorAll('.lang-option');
  const currentLangSpan = switcher.querySelector('.current-lang');

  toggle.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdown.classList.toggle('hidden');
  });

  document.addEventListener('click', () => {
    dropdown.classList.add('hidden');
  });

  options.forEach(option => {
    option.addEventListener('click', (e) => {
      e.stopPropagation();
      const lang = option.getAttribute('data-lang');
      if (window.i18n) {
        window.i18n.setLanguage(lang);
      }
      currentLangSpan.textContent = lang.toUpperCase();
      dropdown.classList.add('hidden');
      options.forEach(opt => {
        const check = opt.querySelector('.lang-check');
        if (opt.getAttribute('data-lang') === lang) {
          check.classList.remove('hidden');
        } else {
          check.classList.add('hidden');
        }
      });
      setTimeout(() => window.location.reload(), 200);
    });
  });
}

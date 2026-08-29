// Language Switcher Component - автоматически добавляется на все страницы

document.addEventListener('DOMContentLoaded', () => {
  // Инициализируем i18n
  if (window.i18n) {
    window.i18n.updateDOM();
  }

  // Добавляем переключатель языка в хедер
  addLanguageSwitcher();
  
  // Обновляем валюту на украинскую гривну
  updateCurrency();
});

function addLanguageSwitcher() {
  // Находим место для вставки (перед иконками в хедере)
  const headerActions = document.querySelector('.site-header .flex.items-center.space-x-4');
  if (!headerActions) return;

  // Создаём кнопку переключателя
  const switcher = document.createElement('div');
  switcher.className = 'language-switcher relative';
  switcher.innerHTML = `
    <button class="lang-toggle flex items-center space-x-1 px-3 py-1.5 text-xs font-medium border border-[#E7E2DA] rounded-full hover:border-neutral-900 transition">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/>
        <line x1="2" y1="12" x2="22" y2="12"/>
        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
      </svg>
      <span class="current-lang uppercase">${window.i18n.getLanguage()}</span>
    </button>
    <div class="lang-dropdown hidden absolute right-0 mt-2 bg-white rounded-lg shadow-xl border border-[#E7E2DA] overflow-hidden z-50 min-w-[120px]">
      <button class="lang-option w-full px-4 py-2 text-left text-sm hover:bg-neutral-50 transition flex items-center justify-between" data-lang="uk">
        <span>🇺🇦 Українська</span>
        <svg class="lang-check hidden w-4 h-4 text-green-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
      </button>
      <button class="lang-option w-full px-4 py-2 text-left text-sm hover:bg-neutral-50 transition flex items-center justify-between" data-lang="ru">
        <span>🇷🇺 Русский</span>
        <svg class="lang-check hidden w-4 h-4 text-green-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
      </button>
    </div>
  `;

  // Вставляем переключатель первым элементом
  headerActions.insertBefore(switcher, headerActions.firstChild);

  // Логика переключения
  const toggle = switcher.querySelector('.lang-toggle');
  const dropdown = switcher.querySelector('.lang-dropdown');
  const options = switcher.querySelectorAll('.lang-option');
  const currentLangSpan = switcher.querySelector('.current-lang');

  // Показать текущий язык
  updateSelectedLang();

  // Открыть/закрыть dropdown
  toggle.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdown.classList.toggle('hidden');
  });

  // Закрыть при клике вне
  document.addEventListener('click', () => {
    dropdown.classList.add('hidden');
  });

  // Выбор языка
  options.forEach(option => {
    option.addEventListener('click', (e) => {
      e.stopPropagation();
      const lang = option.getAttribute('data-lang');
      window.i18n.setLanguage(lang);
      currentLangSpan.textContent = lang.toUpperCase();
      dropdown.classList.add('hidden');
      updateSelectedLang();
      
      // Перезагрузка страницы для обновления контента с сервера
      setTimeout(() => window.location.reload(), 300);
    });
  });

  function updateSelectedLang() {
    const currentLang = window.i18n.getLanguage();
    options.forEach(opt => {
      const check = opt.querySelector('.lang-check');
      if (opt.getAttribute('data-lang') === currentLang) {
        check.classList.remove('hidden');
      } else {
        check.classList.add('hidden');
      }
    });
  }
}

function updateCurrency() {
  // Заменяем рубли на гривны
  document.body.innerHTML = document.body.innerHTML
    .replace(/₽/g, '₴')
    .replace(/руб\./g, '₴')
    .replace(/5\s*000/g, '5 000')
    .replace(/Россия/gi, 'Україна')
    .replace(/России/gi, 'України')
    .replace(/Москв/gi, 'Київ');
}

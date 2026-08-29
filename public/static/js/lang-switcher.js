// Language Switcher Component
document.addEventListener('DOMContentLoaded', () => {
  renderLanguageSwitcher();
});

function renderLanguageSwitcher() {
  const current = window.I18N?.currentLang || 'ua';
  const containerHTML = `
    <div class="lang-switcher flex items-center bg-[#F0EDE8] rounded-full p-0.5 text-[11px] font-semibold tracking-wider text-neutral-600 border border-[#E7E2DA]">
      <button type="button" onclick="switchLanguage('ua')" class="px-2 py-0.5 rounded-full transition ${current === 'ua' ? 'bg-neutral-900 text-white shadow-sm' : 'hover:text-neutral-900'}">
        UA
      </button>
      <button type="button" onclick="switchLanguage('ru')" class="px-2 py-0.5 rounded-full transition ${current === 'ru' ? 'bg-neutral-900 text-white shadow-sm' : 'hover:text-neutral-900'}">
        RU
      </button>
    </div>
  `;

  // Insert into header search / right controls area
  const headerRight = document.querySelector('.site-header .flex.items-center.space-x-4');
  if (headerRight && !document.querySelector('.lang-switcher')) {
    headerRight.insertAdjacentHTML('afterbegin', containerHTML);
  }
}

window.switchLanguage = (lang) => {
  if (window.I18N) {
    window.I18N.setLang(lang);
    document.querySelectorAll('.lang-switcher button').forEach(b => {
      b.className = 'px-2 py-0.5 rounded-full transition hover:text-neutral-900';
    });
    const activeBtn = document.querySelector(`.lang-switcher button[onclick="switchLanguage('${lang}')"]`);
    if (activeBtn) {
      activeBtn.className = 'px-2 py-0.5 rounded-full transition bg-neutral-900 text-white shadow-sm';
    }
  }
};

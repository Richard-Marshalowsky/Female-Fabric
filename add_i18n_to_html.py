#!/usr/bin/env python3
"""
Скрипт автоматически добавляет i18n скрипты во все HTML файлы
"""
import os
from pathlib import Path

# Пути к HTML файлам
TEMPLATES_DIR = Path(__file__).parent / 'app' / 'templates'

# Скрипты которые нужно добавить
I18N_SCRIPTS = '''
  <!-- i18n System -->
  <script src="/static/js/i18n.js"></script>
  <script src="/static/js/lang-switcher.js"></script>
'''

def add_i18n_to_html(filepath):
    """Добавляет i18n скрипты перед </body> если их ещё нет"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем не добавлены ли уже
    if 'i18n.js' in content:
        print(f"  ✓ {filepath.name} - уже обновлён")
        return False
    
    # Добавляем перед </body>
    if '</body>' in content:
        content = content.replace('</body>', f'{I18N_SCRIPTS}</body>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ {filepath.name} - обновлён!")
        return True
    else:
        print(f"  ⚠️ {filepath.name} - не найден тег </body>")
        return False

def main():
    print("=" * 60)
    print("Добавление i18n системы во все HTML файлы")
    print("=" * 60)
    print()
    
    html_files = list(TEMPLATES_DIR.glob('*.html'))
    
    if not html_files:
        print("❌ HTML файлы не найдены в", TEMPLATES_DIR)
        return
    
    print(f"Найдено {len(html_files)} HTML файлов:")
    print()
    
    updated = 0
    for html_file in html_files:
        if add_i18n_to_html(html_file):
            updated += 1
    
    print()
    print("=" * 60)
    print(f"✅ Готово! Обновлено {updated} из {len(html_files)} файлов")
    print("=" * 60)

if __name__ == '__main__':
    main()

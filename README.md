# Flet-multilingual-support
An application demonstrating advanced localization for the Flet framework with dynamic language switching and automatic updating of UI components.

## Main features ✨

- **Multi-language support**: EN, SK, CZ (easy extension with other languages)
- **Complex UI components**: Localized buttons, text fields, navigation, dropdowns
- **Dynamic language switching**: Instant UI update without page reload
- **Fallback system**: Automatic return to the base language in case of missing translations
- **Modular design**: Easy addition of new localized components
- **RTL support**: Ready for languages ​​with right-hand writing (e.g. Arabic)

## Installation ⚙️

1. **Requirements**:
- Python 3.7+
- Flet framework

2. **Install packages**:
```bash
pip install flet
```
## Štruktúra projektu 📂

├── main.py                # Hlavný vstupný bod aplikácie
├── locales/               # Modul pre lokalizáciu
│   ├── localization.py    # Implementácia lokalizačného servisu
│   └── ...                # Ďalšie lokalizačné súbory
├── translations/          # Prekladové súbory
│   ├── en.json            # Anglické preklady
│   ├── sk.json            # Slovenské preklady
│   └── cs.json            # České preklady
├── views/                 # UI views
│   └── login_page.py      # Príklad login obrazovky
└── assets/                # Statické assets

## Konfigurácia prekladov 🈯

Vytvorenie prekladových súborov:
Každý jazyk má vlastný JSON súbor v priečinku translations:

// sk.json
```bash
{
  "app_title": "Flet Lokalizácia",
  "welcome_message": "Vitajte v aplikácií!",
  "email": "Email",
  "password": "Heslo",
  "login": "Prihlásiť"
}
```

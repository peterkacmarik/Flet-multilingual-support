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
## Project structure 📂
```bash
├── main.py              # Main application entry point
├── locales/             # Localization module
│ ├── localization.py    # Localization service implementation
│ └── ...                # Additional localization files
├── translations/        # Translation files
│ ├── en.json            # English translations
│ ├── sk.json            # Slovak translations
│ └── cs.json            # Czech translations
├── views/               # UI views
│ └── login_page.py      # Example login screen
└── assets/              # Static assets
```
## Configuring translations 🈯

1. Creating translation files:
Each language has its own JSON file in the translations folder:

```bash
// sk.json
{
  "app_title": "Flet Lokalizácia",
  "welcome_message": "Vitajte v aplikácií!",
  "email": "Email",
  "password": "Heslo",
  "login": "Prihlásiť"
}
```
2. Adding a new language:
```bash
# V LocalizationService.__init__
self.supported_locales = {
    ...
    "de": LocaleInfo("de", "Deutsch", TextDirection.LTR, "🇩🇪")
}
```
## Using components �

### Basic text
```bash
LocalizedText(
    localization_service,
    text_key="welcome_message",
    default="Welcome!",
    size=24,
    weight=ft.FontWeight.BOLD
)
```

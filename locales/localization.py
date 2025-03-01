import flet as ft
from typing import Dict, Optional, List, Callable, Any
import json
import os
import logging
from dataclasses import dataclass
from enum import Enum

# Nastavenie loggera
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextDirection(Enum):
    LTR = "ltr"
    RTL = "rtl"

@dataclass
class LocaleInfo:
    code: str
    name: str
    direction: TextDirection
    flag_emoji: str
    
class LocalizationService:
    def __init__(
        self, 
        translations_dir: str = "translations",
        fallback_locale: str = "en",
        default_locale: str = "en"
    ):
        self.translations_dir = translations_dir
        self.current_locale = default_locale
        self.fallback_locale = fallback_locale
        self.translations: Dict[str, Dict[str, str]] = {}
        self.listeners: List[Callable[[], None]] = []
        
        self.supported_locales = {
            "en": LocaleInfo("en", "English", TextDirection.LTR, "🇬🇧"),
            "sk": LocaleInfo("sk", "Slovenčina", TextDirection.LTR, "🇸🇰"),
            "cs": LocaleInfo("cs", "Čeština", TextDirection.LTR, "🇨🇿"),
            # "de": LocaleInfo("de", "Deutsch", TextDirection.LTR, "🇩🇪"),
            # "fr": LocaleInfo("fr", "Français", TextDirection.LTR, "🇫🇷"),
            # "es": LocaleInfo("es", "Español", TextDirection.LTR, "🇪🇸"),
            # "it": LocaleInfo("it", "Italiano", TextDirection.LTR, "🇮🇹"),
            # "pt": LocaleInfo("pt", "Português", TextDirection.LTR, "🇵🇹")
        }

        # Validácia jazykov
        self._validate_locales()
        self._load_translations()

    def _validate_locales(self):
        """Kontrola existencie fallback a default jazyka"""
        if self.fallback_locale not in self.supported_locales:
            raise ValueError(f"Neplatný fallback locale: {self.fallback_locale}")
        if self.current_locale not in self.supported_locales:
            raise ValueError(f"Neplatný default locale: {self.current_locale}")
        if "en" not in self.supported_locales:
            raise ValueError("Základný jazyk 'en' musí byť vždy prítomný")

    def _load_translations(self) -> None:
        try:
            os.makedirs(self.translations_dir, exist_ok=True)
            for locale in self.supported_locales:
                file_path = os.path.join(self.translations_dir, f"{locale}.json")
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.translations[locale] = json.load(f)
                else:
                    logger.warning(f"Chýbajúci prekladový súbor pre jazyk: {locale}")
                    self.translations[locale] = {}
        except Exception as e:
            logger.error(f"Chyba pri načítaní prekladov: {str(e)}")
            raise

    def get(self, key: str, default: Optional[str] = None) -> str:
        locales_to_try = list(
            dict.fromkeys([  # Odstráni duplicity zachovaním poradia
                self.current_locale,
                self.fallback_locale,
                "en"
            ])
        )
        
        for locale in locales_to_try:
            if locale in self.translations:
                if translation := self.translations[locale].get(key):
                    return translation
        return default or f"[{key}]"

    def switch_locale(self, locale: str) -> None:
        if locale not in self.supported_locales:
            logger.error(f"Pokus o prepnutie na nepodporovaný jazyk: {locale}")
            return
            
        self.current_locale = locale
        self.notify_listeners()
        
    def add_listener(self, listener: Callable[[], None]) -> None:
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_listener(self, listener: Callable[[], None]) -> None:
        if listener in self.listeners:
            self.listeners.remove(listener)

    def notify_listeners(self) -> None:
        for listener in self.listeners:
            listener()

class LocalizedMixin:
    def __init__(self, localization: LocalizationService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.localization = localization
        self.localization.add_listener(self.update_localization)
        
    def update_localization(self) -> None:
        # Aktualizácia textu bez volania update()
        self._update_text()
        
        # Ak je komponent na stránke, vykonáme update
        if hasattr(self, 'page') and self.page is not None:
            self.update()

    def _update_text(self) -> None:
        try:
            # Použitie novej get() metódy s fallback
            self._apply_localized_text()
        except Exception as e:
            logger.error(f"Chyba pri aktualizácii textu: {str(e)}")
            self.value = "L10N_ERROR"

    def _apply_localized_text(self):
        """Abstraktná metóda pre aplikáciu lokalizovaného textu"""
        raise NotImplementedError

    def did_mount(self):
        """Volá sa po pridaní komponentu na stránku"""
        self._update_text()
        super().did_mount()

    def dispose(self):
        self.localization.remove_listener(self.update_localization)
        super().dispose()

class LanguageSelector(ft.PopupMenuButton):
    def __init__(self, localization: LocalizationService):
        super().__init__()
        self.localization = localization
        self.localization.add_listener(self._update_items) 
        self.icon = ft.Icons.LANGUAGE
        self._update_items()

    def _update_items(self) -> None:
        self.items = [
            ft.PopupMenuItem(
                text=f"{info.flag_emoji} {info.name}",
                data=locale,
                on_click=lambda e: self.localization.switch_locale(e.control.data)
            ) for locale, info in self.localization.supported_locales.items()
        ]

class LocalizedText(LocalizedMixin, ft.Text):
    def __init__(
        self, 
        localization: LocalizationService, 
        text_key: str, 
        default: Optional[str] = None, **kwargs
    ):
        self.text_key = text_key
        self.default = default
        super().__init__(localization=localization, **kwargs)
        self._apply_localized_text()  # Pridané pre okamžitú inicializáciu

    def _apply_localized_text(self):
        self.value = self.localization.get(self.text_key, self.default)

class LocalizedTextField(LocalizedMixin, ft.TextField):
    def __init__(
        self, 
        localization: LocalizationService, 
        text_key: str, 
        default: Optional[str] = None,
        **kwargs
    ):
        self.text_key = text_key
        self.default = default
        super().__init__(localization=localization, **kwargs)
        self._apply_localized_text()
    
    def _apply_localized_text(self):
        self.label = self.localization.get(self.text_key, self.default)

class LocalizedPopupMenuButton(LocalizedMixin, ft.PopupMenuButton):
    def __init__(
        self, 
        localization: LocalizationService, 
        items: List[Dict[str, Any]],
        **kwargs
    ):
        self.menu_items = items
        super().__init__(localization=localization, **kwargs)
        self._rebuild_items()
    
    def _rebuild_items(self):
        self.items = [
            ft.PopupMenuItem(
                text=self.localization.get(
                    item["key"], 
                    item.get("default", f"[{item['key']}]")
                ),
                icon=item.get("icon"),
                on_click=item["on_click"]
            )
            for item in self.menu_items
        ]
    
    def _apply_localized_text(self):
        self._rebuild_items()

class LocalizedNavigationBar(LocalizedMixin, ft.NavigationBar):
    def __init__(
        self, 
        localization: LocalizationService, 
        destinations: List[Dict[str, Any]],
        **kwargs
    ):
        self.destinations_config = destinations
        super().__init__(localization=localization, **kwargs)
        self._rebuild_destinations()
    
    def _rebuild_destinations(self):
        self.destinations = [
            ft.NavigationBarDestination(
                icon=dest["icon"],
                label=self.localization.get(
                    dest["key"], 
                    dest.get("default", f"[{dest['key']}]")
                )
            )
            for dest in self.destinations_config
        ]
    
    def _apply_localized_text(self):
        self._rebuild_destinations()

class LocalizedNavigationDrawer(LocalizedMixin, ft.NavigationDrawer):
    def __init__(
        self, 
        localization: LocalizationService, 
        destinations: List[Dict[str, Any]],
        **kwargs
    ):
        self.destinations_config = destinations
        super().__init__(localization=localization, **kwargs)
        self._rebuild_destinations()
    
    def _rebuild_destinations(self):
        self.controls = [
            ft.NavigationDrawerDestination(
                icon=dest["icon"],
                label=self.localization.get(
                    dest["key"], 
                    dest.get("default", f"[{dest['key']}]")
                )
            )
            for dest in self.destinations_config
        ]
    
    def _apply_localized_text(self):
        self._rebuild_destinations()

class LocalizedTextButton(LocalizedMixin, ft.TextButton):
    def __init__(
        self, 
        localization: LocalizationService, 
        text_key: str, 
        default: Optional[str] = None,
        **kwargs
    ):
        self.text_key = text_key
        self.default = default
        super().__init__(localization=localization, **kwargs)
        self._apply_localized_text()
    
    def _apply_localized_text(self):
        self.text = self.localization.get(self.text_key, self.default)

class LocalizedOutlinedButton(LocalizedMixin, ft.OutlinedButton):
    def __init__(
        self, 
        localization: LocalizationService, 
        text_key: str, 
        default: Optional[str] = None,
        **kwargs
    ):
        self.text_key = text_key
        self.default = default
        super().__init__(localization=localization, **kwargs)
        self._apply_localized_text()
    
    def _apply_localized_text(self):
        self.text = self.localization.get(self.text_key, self.default)

class LocalizedElevatedButton(LocalizedMixin, ft.ElevatedButton):
    def __init__(
        self, 
        localization: LocalizationService, 
        text_key: str, 
        default: Optional[str] = None,
        **kwargs
    ):
        self.text_key = text_key
        self.default = default
        super().__init__(localization=localization, **kwargs)
        self._apply_localized_text()
    
    def _apply_localized_text(self):
        self.text = self.localization.get(self.text_key, self.default)

class LocalizedDropdown(LocalizedMixin, ft.Dropdown):
    def __init__(
        self, 
        localization: LocalizationService, 
        label_config: Dict[str, Any],
        options_config: List[Dict[str, Any]],
        **kwargs
    ):
        """
        Parametre:
        label_config: {"key": "label_key", "default": "Default label"}
        options_config: [{"key": "option1", "default": "Default 1"}, ...]
        """
        self.label_config = label_config
        self.options_config = options_config
        super().__init__(localization=localization, **kwargs)
        self._rebuild_options()
    
    def _rebuild_options(self):
        # Aktualizácia labelu
        self.label = self.localization.get(
            self.label_config["key"],
            self.label_config.get("default", f"[{self.label_config['key']}]")
        )
        
        # Aktualizácia options
        self.options = [
            ft.dropdown.Option(
                text=self.localization.get(
                    opt["key"],
                    opt.get("default", f"[{opt['key']}]")
                ),
                key=opt["key"]
            )
            for opt in self.options_config
        ]
    
    def update_label(self, new_label_config: Dict[str, Any]):
        """Aktualizuje konfiguráciu labelu"""
        self.label_config = new_label_config
        self._rebuild_options()
        self.update()
    
    def update_options(self, new_options_config: List[Dict[str, Any]]):
        """Aktualizuje konfiguráciu options"""
        self.options_config = new_options_config
        self._rebuild_options()
        self.update()
    
    def update_all(self, new_label_config: Dict[str, Any], new_options_config: List[Dict[str, Any]]):
        """Kompletná aktualizácia"""
        self.label_config = new_label_config
        self.options_config = new_options_config
        self._rebuild_options()
        self.update()
    
    def _apply_localized_text(self):
        self._rebuild_options()
        
# Inicializácia
# dropdown = LocalizedDropdown(
#     loc_service,
#     label_config={
#         "key": "country_label",
#         "default": "Vyber krajinu"
#     },
#     options_config=[
#         {"key": "sk_option", "default": "Slovensko"},
#         {"key": "cz_option", "default": "Česko"},
#         {"key": "en_option", "default": "Anglicko"}
#     ]
# )

# Dynamická zmena labelu
# dropdown.update_label({
#     "key": "new_label_key",
#     "default": "Nový defaultný label"
# })

# Dynamická zmena options
# dropdown.update_options([
#     {"key": "de_option", "default": "Nemecko"},
#     {"key": "fr_option", "default": "Francúzsko"}
# ])

# Kompletná aktualizácia
# dropdown.update_all(
#     {"key": "city_label", "default": "Vyber mesto"},
#     [
#         {"key": "ba_option", "default": "Bratislava"},
#         {"key": "pr_option", "default": "Praha"}
#     ]
# )
import flet as ft
from locales.localization import (
    LanguageSelector, 
    LocalizationService,
    LocalizedDropdown,
    LocalizedText,
    LocalizedTextField,
    LocalizedTextButton,
    LocalizedOutlinedButton,
    LocalizedElevatedButton,
    LocalizedNavigationBar,
    LocalizedPopupMenuButton,
    LocalizedNavigationDrawer,
)

class LoginPage(ft.View):
    def __init__(self, page: ft.Page, loc_service: LocalizationService):
        super().__init__()
        self.page = page
        self.loc_service = loc_service
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.language_selector =LanguageSelector(self.loc_service)
        
        self.appbar = ft.AppBar(
            leading_width=40,
            title=LocalizedText(self.loc_service, "app_title", "Flet Localization"),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            actions=[
                self.language_selector,
                ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED),
                LocalizedPopupMenuButton(
                    self.loc_service,
                    items=[
                        {"key": "home", "default": "Domov", "icon": ft.Icons.HOME, "on_click": lambda e: self.page.go("/home")},
                        {"key": "profile", "default": "Profil", "icon": ft.Icons.PERSON, "on_click": lambda e: self.page.go("/profile")},
                        {"key": "settings", "default": "Nastavenia", "icon": ft.Icons.SETTINGS, "on_click": lambda e: self.page.go("/settings")},
                        {"key": "logout", "default": "Odhlasenie", "icon": ft.Icons.LOGOUT, "on_click": lambda e: self.page.go("/logout")},
                        {"key": "more", "default": "Viac", "icon": ft.Icons.MORE_VERT, "on_click": lambda e: self.page.go("/more")},
                    ]
                )
            ]
        )
        
        self.inicialize_view()
        
        self.navigation_bar = LocalizedNavigationBar(
            self.loc_service,
            destinations=[
                {"key": "home", "default": "Domov", "icon": ft.Icons.HOME},
                {"key": "profile", "default": "Profil", "icon": ft.Icons.PERSON},
                {"key": "settings", "default": "Nastavenia", "icon": ft.Icons.SETTINGS},
                {"key": "logout", "default": "Odhlasenie", "icon": ft.Icons.LOGOUT},
                {"key": "more", "default": "Viac", "icon": ft.Icons.MORE_VERT}
            ]
        )
        
        self.drawer = LocalizedNavigationDrawer(
            self.loc_service,
            destinations=[
                {"key": "home", "default": "Domov", "icon": ft.Icons.HOME},
                {"key": "profile", "default": "Profil", "icon": ft.Icons.PERSON},
                {"key": "settings", "default": "Nastavenia", "icon": ft.Icons.SETTINGS},
                {"key": "logout", "default": "Odhlasenie", "icon": ft.Icons.LOGOUT},
                {"key": "more", "default": "Viac", "icon": ft.Icons.MORE_VERT}
            ]
        )
        
    def inicialize_view(self) -> None:
        self.login_text = LocalizedText(
            self.loc_service, 
            "welcome_message", 
            "Vitajte v aplikácií!"
        )
        self.email_field = LocalizedTextField(
            self.loc_service, 
            text_key="email", 
            default="Email",
            hint_text="user@example.com"
        )
        self.password_field = LocalizedTextField(
            self.loc_service, 
            text_key="password", 
            default="Heslo",
            hint_text="Heslo"
        )
        self.text_button = LocalizedTextButton(
            self.loc_service, 
            text_key="login", 
            default="Prihlásit"
        )
        self.outlined_button = LocalizedOutlinedButton(
            self.loc_service, 
            text_key="login", 
            default="Prihlásit"
        )
        self.elevated_button = LocalizedElevatedButton(
            self.loc_service, 
            text_key="login", 
            default="Prihlásit"
        )
        self.dropdown_selector = LocalizedDropdown(
            self.loc_service, 
            label_config={"key": "language", "default": "Jazyk"},
            options_config=[
                {"key": "english_option", "default": "English"},
                {"key": "czech_option", "default": "Czech"},
                {"key": "slovak_option", "default": "Slovak"}
            ]
        )

        self.controls = [
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    controls=[
                        self.login_text,
                        self.email_field,
                        self.password_field,
                        self.text_button,
                        self.outlined_button,
                        self.elevated_button,
                        self.dropdown_selector,
                    ]
                )
            )
        ]
    
    
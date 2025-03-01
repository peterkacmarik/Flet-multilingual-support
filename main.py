import os
import flet as ft
from locales.localization import LocalizationService
from views.login_page import LoginPage

        
def main(page: ft.Page):
    page.title = "Flet Localization"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 400
    page.window.height = 800
    
    # Inicializácia s vlastným fallback jazykom
    loc_service = LocalizationService(
        fallback_locale="cs",
        default_locale="sk"
    )
    
    def route_change(route):
        page.views.clear()
        
        if page.route == "/login":
            page.views.append(LoginPage(page, loc_service))
        page.update()
        
    page.on_route_change = route_change
    page.go("/login")


if __name__ == '__main__':
    ft.app(
        target=main,
        view=ft.AppView.FLET_APP,
        web_renderer=ft.WebRenderer.CANVAS_KIT,
        assets_dir="assets",
    )
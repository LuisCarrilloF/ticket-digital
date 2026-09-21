import flet as ft

from views.home_view import HomeView


def main(page: ft.Page):
    page.title = "Ticket Digital"
    page.window.min_width = 360
    page.window.width = 700
    page.window.max_width = 700
    page.padding = 0
    page.bgcolor = "#EEEEEE"
    HomeView(page)


if __name__ == "__main__":
    ft.run(main,assets_dir="app/assets",)
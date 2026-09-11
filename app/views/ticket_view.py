import flet as ft


class TicketView:
    def __init__(self, page: ft.Page):
        self.page = page
        self._build()

    def _build(self):
        titulo = ft.Text("Nuevo ticket", size=28, weight=ft.FontWeight.BOLD,)
        cliente = ft.TextField(label="Nombre del cliente", hint_text="Ej. Juan Pérez",)
        telefono = ft.TextField(label="Teléfono", hint_text="Ej. 3121234567", keyboard_type=ft.KeyboardType.PHONE,)

        negocio = ft.Dropdown(
            label="Negocio",
            options=[
                ft.DropdownOption(key="diversiones", text="Diversiones Santa Ana"),
                ft.DropdownOption(key="corexis", text="Corexis"),
            ],
        )

        boton_regresar = ft.ElevatedButton(content=ft.Text("Regresar"), on_click=self._regresar,)

        contenido = ft.Column(
            controls=[
                boton_regresar,
                titulo,
                negocio,
                cliente,
                telefono,
            ],
            spacing=15,
        )

        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=contenido,
                expand=True,
                padding=40,
            )
        )

        self.page.update()

    def _regresar(self, e):
        from views.home_view import HomeView

        HomeView(self.page)
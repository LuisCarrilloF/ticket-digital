import flet as ft

from models.business import Business
from views.ticket_view import TicketView


class ClientView:
    def __init__(self, page: ft.Page, business: Business):
        self.page = page
        self.business = business
        self._build()

    def _build(self):
        titulo = ft.Text(
            "Datos del cliente",
            size=28,
            weight=ft.FontWeight.BOLD,
        )
        negocio = ft.Text(
            f"Ticket para {self.business.name}",
            size=15,
            color="#777777",
        )
        nombre = ft.TextField(
            label="Nombre completo",
            hint_text="Ej. Juan Pérez",
            autofocus=True,
        )
        telefono = ft.TextField(
            label="Teléfono",
            hint_text="Ej. 3121234567",
            keyboard_type=ft.KeyboardType.PHONE,
        )
        direccion = ft.TextField(
            label="Dirección",
            hint_text="Ej. Calle 10 #20-30",
            multiline=True,
            min_lines=2,
            max_lines=3,
        )
        mensaje = ft.Text(color="#B3261E")

        def continuar(e):
            campos = [nombre, telefono, direccion]
            if any(not campo.value.strip() for campo in campos):
                mensaje.value = "Completa el nombre, teléfono y dirección del cliente."
                self.page.update()
                return

            TicketView(
                self.page,
                self.business,
                {
                    "full_name": nombre.value.strip(),
                    "phone": telefono.value.strip(),
                    "address": direccion.value.strip(),
                },
            )

        boton_continuar = ft.ElevatedButton(
            content=ft.Text("Continuar"),
            on_click=continuar,
        )
        boton_regresar = ft.TextButton(
            content=ft.Text("Regresar"),
            on_click=self._regresar,
        )

        contenido = ft.Column(
            controls=[
                boton_regresar,
                titulo,
                negocio,
                nombre,
                telefono,
                direccion,
                mensaje,
                boton_continuar,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        )

        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=contenido,
                expand=True,
                padding=40,
                bgcolor="#F8F7F2",
            )
        )
        self.page.update()

    def _regresar(self, e):
        from views.home_view import HomeView

        HomeView(self.page)

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
            color= "#000000",
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
            color="#777777",
            bgcolor= "#FDF6F6"
        )
        telefono = ft.TextField(
            label="Teléfono",
            hint_text="Ej. 3121234567",
            keyboard_type=ft.KeyboardType.PHONE,
            color="#777777",
            bgcolor= "#FDF6F6"
        )
        direccion = ft.TextField(
            label="Dirección",
            hint_text="Ej. Calle 10 #20-30",
            multiline=True,
            min_lines=2,
            max_lines=3,
            color= "#505050",
            bgcolor= "#FDF6F6"
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
            bgcolor= "#000D55",
            color= "#F2F3F8"
        )
        boton_regresar = ft.TextButton(
            content=ft.Text("Regresar"),
            icon=ft.Icons.ARROW_BACK,
            on_click=self._regresar,
            style=ft.ButtonStyle(
                bgcolor="#0C0C0C",
                color="#F2F3F8",
            ),
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
                bgcolor="#EEEEEE",
            )
        )
        self.page.update()

    def _regresar(self, e):
        from views.home_view import HomeView
        HomeView(self.page)

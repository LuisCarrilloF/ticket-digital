import flet as ft
from datetime import datetime

from models.business import Business
from views.ticket_view import TicketView


class ClientView:
    def __init__(self, page: ft.Page, business: Business):
        self.page = page
        self.business = business
        self._build()

    def _build(self):
        titulo = ft.Text(
            "Información del Cliente",
            size=16,
            weight=ft.FontWeight.BOLD,
            color="#000000",
        )
        negocio = ft.Text(
            f"Ticket para {self.business.name}",
            size=13,
            color="#817A73",
        )
        nombre = ft.TextField(
            hint_text="Nombre del cliente",
            autofocus=True,
            color="#000000",
            bgcolor="#FFFFFF",
            border_color="#DED8D1",
            border_radius=12,
            content_padding=ft.Padding(left=14, right=14, top=14, bottom=14),
        )
        telefono = ft.TextField(
            hint_text="Ej. 6141234567",
            keyboard_type=ft.KeyboardType.PHONE,
            on_change=lambda e: limpiar_telefono(e),
            color="#000000",
            bgcolor="#FFFFFF",
            border_color="#DED8D1",
            border_radius=12,
            content_padding=ft.Padding(left=14, right=14, top=14, bottom=14),
        )
        direccion = ft.TextField(
            hint_text="Dirección del evento o domicilio",
            multiline=True,
            min_lines=2,
            max_lines=3,
            color="#000000",
            bgcolor="#FFFFFF",
            border_color="#DED8D1",
            border_radius=12,
            content_padding=ft.Padding(left=14, right=14, top=14, bottom=14),
        )
        notas = ft.TextField(
            hint_text="Detalles del servicio, observaciones...",
            multiline=True,
            min_lines=3,
            max_lines=4,
            color="#000000",
            bgcolor="#FFFFFF",
            border_color="#DED8D1",
            border_radius=12,
            content_padding=ft.Padding(left=14, right=14, top=14, bottom=14),
        )
        mensaje = ft.Text(color="#B3261E")

        def limpiar_telefono(e):
            valor = "".join(
                caracter for caracter in (e.control.value or "") if caracter.isdigit()
            )[:10]
            if e.control.value != valor:
                e.control.value = valor
                e.control.update()

        def continuar(e):
            campos = [nombre, telefono, direccion]
            if any(not (campo.value or "").strip() for campo in campos):
                mensaje.value = "Completa el nombre, teléfono y dirección del cliente."
                self.page.update()
                return

            telefono_valor = (telefono.value or "").strip()
            if len(telefono_valor) != 10 or not telefono_valor.isdigit():
                mensaje.value = "El teléfono debe tener exactamente 10 dígitos."
                self.page.update()
                return

            TicketView(
                self.page,
                self.business,
                {
                    "full_name": nombre.value.strip(),
                    "phone": telefono.value.strip(),
                    "address": direccion.value.strip(),
                    "notes": notas.value.strip(),
                },
            )

        boton_continuar = ft.ElevatedButton(
            content=ft.Text("Agregar conceptos", weight=ft.FontWeight.BOLD),
            icon=ft.Icons.SAVE,
            on_click=continuar,
            bgcolor="#000D55",
            color="#F2F3F8",
            height=52,
            expand=True,
        )
        boton_regresar = ft.TextButton(
            content=ft.Text("Regresar", color="#000000"),
            icon=ft.Icons.ARROW_BACK,
            on_click=self._regresar,
            style=ft.ButtonStyle(color="#000000"),
        )

        fecha = datetime.now()
        dias = [
            "lunes", "martes", "miércoles", "jueves",
            "viernes", "sábado", "domingo",
        ]
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
        ]
        fecha_texto = f"{dias[fecha.weekday()]}, {fecha.day} de {meses[fecha.month - 1]} de {fecha.year}"

        def campo_con_etiqueta(etiqueta, campo, requerido=False):
            texto = ft.Text(
                etiqueta.upper(),
                size=12,
                weight=ft.FontWeight.BOLD,
                color="#817A73",
            )
            if requerido:
                texto = ft.Row(
                    controls=[
                        texto,
                        ft.Text("*", color="#B3261E", size=12, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=2,
                )
            return ft.Column(controls=[texto, campo], spacing=6)

        informacion = ft.Container(
            content=ft.Column(
                controls=[
                    titulo,
                    campo_con_etiqueta("Nombre completo", nombre, requerido=True),
                    campo_con_etiqueta("Teléfono", telefono),
                    campo_con_etiqueta("Dirección / Colonia", direccion),
                    campo_con_etiqueta("Notas adicionales", notas),
                ],
                spacing=12,
            ),
            bgcolor="#FFFFFF",
            border_radius=16,
            padding=20,
            border=ft.Border.all(1, "#E1DDD7"),
        )

        informacion_fecha = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.CALENDAR_MONTH,
                            color="#4B83C5",
                            size=20,
                        ),
                        bgcolor="#FFF0B8",
                        border_radius=30,
                        padding=10,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "FECHA DEL TICKET",
                                size=11,
                                weight=ft.FontWeight.BOLD,
                                color="#817A73",
                            ),
                            ft.Text(
                                fecha_texto,
                                size=13,
                                color="#000000",
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ],
                spacing=12,
            ),
            bgcolor="#FFFFFF",
            border_radius=16,
            padding=16,
            border=ft.Border.all(1, "#E1DDD7"),
        )

        contenido = ft.Column(
            controls=[
                boton_regresar,
                negocio,
                informacion,
                informacion_fecha,
                mensaje,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        contenido,
                        ft.Container(
                            content=boton_continuar,
                            padding=ft.Padding(top=10, bottom=4),
                        ),
                    ],
                    expand=True,
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
                expand=True,
                padding=12,
                bgcolor="#F7F5F0",
            )
        )
        self.page.bgcolor = "#F7F5F0"
        self.page.update()

    def _regresar(self, e):
        from views.home_view import HomeView
        HomeView(self.page)

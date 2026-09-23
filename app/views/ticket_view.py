import flet as ft
from decimal import Decimal, InvalidOperation
from datetime import datetime
from urllib.parse import quote

from models.business import Business
from models.ticket import Ticket, TicketItem
from services.image_loader import image_source
from services.ticket_generator import (
    format_amount,
    generate_ticket,
    generate_ticket_png,
)


class TicketView:
    def __init__(self, page: ft.Page, business: Business, customer: dict):
        self.page = page
        self.business = business
        self.customer = customer
        self.items = []
        self._build()

    def _build(self):
        self.titulo = ft.Text(
            "Agregar conceptos",
            size=24,
            weight=ft.FontWeight.BOLD,
            color="#000000",
        )
        negocio = ft.Text(
            self.business.name,
            size=13,
            color="#817A73",
        )
        self.concepto = ft.TextField(
            hint_text="Descripción del concepto",
            color="#000000",
            bgcolor="#FFFFFF",
            border_color="#DED8D1",
            border_radius=12,
            content_padding=ft.Padding(left=14, right=14, top=12, bottom=12),
        )
        self.cantidad = ft.TextField(
            label="CANTIDAD",
            value="1",
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._validar_cantidad,
            color="#000000",
            bgcolor="#FFFFFF",
            border_color="#DED8D1",
            border_radius=12,
            content_padding=ft.Padding(left=14, right=14, top=12, bottom=12),
        )
        self.precio = ft.TextField(
            label="PRECIO UNITARIO",
            hint_text="$ 0.00",
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._validar_precio,
            color="#000000",
            bgcolor="#FFFFFF",
            border_color="#DED8D1",
            border_radius=12,
            content_padding=ft.Padding(left=14, right=14, top=12, bottom=12),
        )
        self.mensaje = ft.Text(color="#B3261E")
        self.lista_conceptos = ft.Column(spacing=8)
        self.contador_conceptos = ft.Text("0", size=12, color="#000000")
        self.total = ft.Text(
            "Total: $ 0.00",
            size=20,
            weight=ft.FontWeight.BOLD,
            color="#000000",
        )

        boton_regresar = ft.TextButton(
            content=ft.Text("Regresar", color="#000000"),
            on_click=self._regresar,
            icon=ft.Icons.ARROW_BACK,
            style=ft.ButtonStyle(color="#000000"),
        )
        boton_agregar = ft.ElevatedButton(
            content=ft.Text("Agregar al ticket", weight=ft.FontWeight.BOLD),
            icon=ft.Icons.ADD,
            on_click=self._agregar_concepto,
            bgcolor="#000D55",
            color="#F2F3F8",
            height=48,
        )
        boton_generar = ft.ElevatedButton(
            content=ft.Text("Generar ticket"),
            icon=ft.Icons.ARROW_FORWARD,
            on_click=self._generar_ticket,
            bgcolor="#000D55",
            color="#F2F3F8",
            height=52,
            expand=True,
        )

        conceptos_frecuentes = self.business.services or [
            "Servicio general",
            "Producto personalizado",
        ]
        chips = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(concepto, size=12, color="#000000"),
                    bgcolor="#FFFFFF",
                    border=ft.Border.all(1, "#DED8D1"),
                    border_radius=20,
                    padding=ft.Padding(left=12, right=12, top=7, bottom=7),
                    on_click=lambda e, valor=concepto: self._seleccionar_concepto(valor),
                )
                for concepto in conceptos_frecuentes
            ],
            wrap=True,
            spacing=8,
            run_spacing=8,
        )

        formulario = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Agregar concepto",
                        size=15,
                        weight=ft.FontWeight.BOLD,
                        color="#000000",
                    ),
                    self.concepto,
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=self.cantidad,
                                col={"xs": 12, "sm": 6},
                            ),
                            ft.Container(
                                content=self.precio,
                                col={"xs": 12, "sm": 6},
                            ),
                        ],
                        spacing=10,
                    ),
                    boton_agregar,
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
            bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#E1DDD7"),
            border_radius=16,
            padding=16,
        )

        conceptos_agregados = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Conceptos agregados",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color="#000000",
                            ),
                            ft.Container(
                                content=self.contador_conceptos,
                                bgcolor="#FFF0B8",
                                border_radius=20,
                                padding=ft.Padding(left=8, right=8, top=3, bottom=3),
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Divider(height=1, color="#E1DDD7"),
                    self.lista_conceptos,
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text(
                                    "Total",
                                    weight=ft.FontWeight.BOLD,
                                    color="#000000",
                                ),
                                self.total,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        bgcolor="#FFF3C4",
                        padding=12,
                    ),
                ],
                spacing=8,
            ),
            bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#E1DDD7"),
            border_radius=16,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        contenido = ft.Column(
            controls=[
                boton_regresar,
                self.titulo,
                negocio,
                ft.Text(
                    "CONCEPTOS FRECUENTES",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color="#817A73",
                ),
                chips,
                formulario,
                self.mensaje,
                conceptos_agregados,
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
        )

        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        contenido,
                        ft.Container(
                            content=boton_generar,
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

        self.page.update()

    def _seleccionar_concepto(self, concepto):
        self.concepto.value = concepto
        self.concepto.focus()
        self.page.update()

    def _validar_cantidad(self, e):
        valor = "".join(caracter for caracter in (e.control.value or "") if caracter.isdigit())
        if e.control.value != valor:
            e.control.value = valor
            e.control.update()

    def _validar_precio(self, e):
        valor = "".join(
            caracter
            for caracter in (e.control.value or "")
            if caracter.isdigit() or caracter in ".,"
        )
        separador = next((caracter for caracter in valor if caracter in ".,"), None)
        if separador:
            parte_entera, parte_decimal = valor.split(separador, 1)
            valor = parte_entera + separador + parte_decimal.replace(".", "").replace(",", "")
        if e.control.value != valor:
            e.control.value = valor
            e.control.update()

    def _agregar_concepto(self, e):
        concepto = self.concepto.value.strip()
        try:
            cantidad = int(self.cantidad.value.strip())
            precio = Decimal(self.precio.value.strip().replace(",", "."))
        except (AttributeError, ValueError, InvalidOperation):
            self.mensaje.value = "Escribe una cantidad entera y un precio válido."
            self.page.update()
            return

        if not concepto or cantidad <= 0 or precio <= 0:
            self.mensaje.value = "Completa el concepto y usa valores mayores que cero."
            self.page.update()
            return

        self.items.append(TicketItem(concepto, cantidad, precio))
        self.concepto.value = ""
        self.cantidad.value = "1"
        self.precio.value = ""
        self.mensaje.value = ""
        self._actualizar_conceptos()

    def _actualizar_conceptos(self):
        self.lista_conceptos.controls = []
        for indice, item in enumerate(self.items):
            self.lista_conceptos.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(
                            f"{item.concept} - {item.quantity} x "
                            f"{format_amount(item.unit_price)} = "
                            f"{format_amount(item.subtotal)}",
                            expand=True,
                            color="#000000",
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color="#000000",
                            tooltip="Eliminar concepto",
                            on_click=lambda e, i=indice: self._eliminar_concepto(i),
                        ),
                    ]
                )
            )
        total = sum((item.subtotal for item in self.items), Decimal("0"))
        self.contador_conceptos.value = str(len(self.items))
        self.total.value = f"Total: {format_amount(total)}"
        self.page.update()

    def _eliminar_concepto(self, indice):
        self.items.pop(indice)
        self._actualizar_conceptos()

    def _generar_ticket(self, e):
        if not self.items:
            self.mensaje.value = "Agrega al menos un concepto para generar el ticket."
            self.page.update()
            return

        ticket = Ticket(
            self.business.name,
            self.customer,
            self.items.copy(),
            business_logo=self.business.logo,
        )
        self._mostrar_ticket_generado(ticket)

    def _mostrar_ticket_generado(self, ticket):
        contenido_ticket = generate_ticket(ticket)
        fecha = datetime.now()
        numero_ticket = f"{fecha:%Y%m%d}-{fecha:%H%M}"
        self.ticket_generado = contenido_ticket
        self.file_picker = ft.FilePicker()
        self.page.services.append(self.file_picker)
        dias = [
            "lunes", "martes", "miércoles", "jueves",
            "viernes", "sábado", "domingo",
        ]
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
        ]
        fecha_texto = (
            f"{dias[fecha.weekday()]}, {fecha.day} de "
            f"{meses[fecha.month - 1]} de {fecha.year} - {fecha:%I:%M %p}"
        )
        self.ticket_imagen = generate_ticket_png(ticket, numero_ticket, fecha_texto)

        conceptos = ft.Column(spacing=10)
        for item in ticket.items:
            conceptos.controls.append(
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    item.concept,
                                    weight=ft.FontWeight.BOLD,
                                    color="#000000",
                                    expand=True,
                                ),
                                ft.Text(
                                    format_amount(item.subtotal),
                                    weight=ft.FontWeight.BOLD,
                                    color="#000D55",
                                ),
                            ],
                        ),
                        ft.Text(
                            f"{item.quantity} x {format_amount(item.unit_price)}",
                            size=12,
                            color="#817A73",
                        ),
                    ],
                    spacing=2,
                )
            )

        resumen = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(
                                "TOTAL DEL TICKET",
                                size=11,
                                weight=ft.FontWeight.BOLD,
                                color="#817A73",
                            ),
                            ft.Text(
                                format_amount(ticket.total),
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color="#000D55",
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                f"{len(ticket.items)} conceptos",
                                size=11,
                                color="#817A73",
                            ),
                            ft.Text(
                                ticket.customer["full_name"],
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color="#000000",
                            ),
                        ],
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#E1DDD7"),
            border_radius=16,
            padding=16,
        )

        encabezado = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Image(
                            src=image_source(self.business.logo),
                            width=48,
                            height=48,
                        ),
                        width=56,
                        height=56,
                        bgcolor="#FFFFFF",
                        border_radius=12,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                self.business.name,
                                size=17,
                                weight=ft.FontWeight.BOLD,
                                color="#FFFFFF",
                            ),
                            ft.Text(
                                self.business.description,
                                size=11,
                                color="#F2F3F8",
                            ),
                            ft.Container(
                                content=ft.Text(
                                    f"TICKET #{numero_ticket}",
                                    size=11,
                                    color="#FFFFFF",
                                    weight=ft.FontWeight.BOLD,
                                ),
                                bgcolor="#24306E",
                                border_radius=8,
                                padding=ft.Padding(left=8, right=8, top=5, bottom=5),
                            ),
                        ],
                        spacing=5,
                        expand=True,
                    ),
                ],
                spacing=12,
            ),
            bgcolor="#000D55",
            padding=16,
        )

        detalles = ft.Column(
            controls=[
                ft.Text(
                    fecha_texto,
                    size=11,
                    color="#817A73",
                ),
                ft.Text(
                    ticket.customer["full_name"],
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color="#000000",
                ),
                ft.Text(f"Teléfono: {ticket.customer['phone']}", size=12, color="#555555"),
                ft.Text(f"Dirección: {ticket.customer['address']}", size=12, color="#555555"),
            ],
            spacing=6,
        )

        contenido_recibo = ft.Column(
            controls=[
                encabezado,
                ft.Container(content=detalles, padding=16),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "CONCEPTOS",
                                size=11,
                                weight=ft.FontWeight.BOLD,
                                color="#817A73",
                            ),
                            conceptos,
                        ],
                        spacing=12,
                    ),
                    padding=ft.Padding(left=16, right=16, top=4, bottom=16),
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("TOTAL A PAGAR", weight=ft.FontWeight.BOLD, color="#000000"),
                            ft.Text(
                                format_amount(ticket.total),
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color="#000D55",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor="#FFF3C4",
                    padding=16,
                ),
            ],
            spacing=0,
        )

        if ticket.customer.get("notes"):
            contenido_recibo.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("NOTAS", size=11, weight=ft.FontWeight.BOLD, color="#000D55"),
                            ft.Text(ticket.customer["notes"], size=12, color="#000000"),
                        ],
                        spacing=5,
                    ),
                    bgcolor="#FFF3C4",
                    border_radius=12,
                    margin=16,
                    padding=12,
                )
            )

        recibo = ft.Container(
            content=contenido_recibo,
            bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#E1DDD7"),
            border_radius=16,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        boton_guardar = ft.OutlinedButton(
            content=ft.Text("Guardar imagen", weight=ft.FontWeight.BOLD),
            icon=ft.Icons.DOWNLOAD,
            on_click=self._guardar_ticket,
            style=ft.ButtonStyle(color="#000D55"),
            height=48,
            expand=True,
        )
        boton_compartir = ft.ElevatedButton(
            content=ft.Text("Compartir", weight=ft.FontWeight.BOLD),
            icon=ft.Icons.SHARE,
            on_click=self._compartir_ticket,
            bgcolor="#000D55",
            color="#F2F3F8",
            height=48,
            expand=True,
        )

        contenido = ft.Column(
            controls=[
                ft.TextButton(
                    content=ft.Text("Regresar", color="#000000"),
                    icon=ft.Icons.ARROW_BACK,
                    on_click=self._regresar,
                    style=ft.ButtonStyle(color="#000000"),
                ),
                resumen,
                recibo,
                ft.Row(
                    controls=[boton_guardar, boton_compartir],
                    spacing=10,
                ),
                ft.TextButton(
                    content=ft.Text("Crear nuevo ticket", color="#817A73"),
                    on_click=lambda e: TicketView(self.page, self.business, self.customer),
                ),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
        )

        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=contenido,
                expand=True,
                padding=12,
                bgcolor="#F7F5F0",
            )
        )
        self.page.update()

    async def _guardar_ticket(self, e):
        await self.file_picker.save_file(
            dialog_title="Guardar imagen del ticket",
            file_name="ticket.png",
            allowed_extensions=["png"],
            src_bytes=self.ticket_imagen,
        )
        self._mostrar_mensaje("Imagen del ticket guardada correctamente.", "#1B5E20")

    def _compartir_ticket(self, e):
        url = "https://web.whatsapp.com/send?text=" + quote(self.ticket_generado)
        self.page.launch_url(url)
        self._mostrar_mensaje(
            "Se abrió WhatsApp Web. Elige un contacto para compartir el ticket.",
            "#1B5E20",
        )

    def _mostrar_mensaje(self, texto, color):
        self.page.snack_bar = ft.SnackBar(content=ft.Text(texto), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()

    def _regresar(self, e):
        from views.home_view import HomeView

        HomeView(self.page)
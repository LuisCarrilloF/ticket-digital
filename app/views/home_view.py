import flet as ft

from models.business import Business
from services.storage import load_businesses, save_businesses
from views.add_negocio_view import AddNegocioView
from views.client_view import ClientView


class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page

        # --------------------------------
        # CONFIGURACIÓN RESPONSIVE
        # --------------------------------

        self.MIN_WIDTH = 360
        self.MAX_CONTENT_WIDTH = 700

        self.businesses = load_businesses()

        self._build()

    def _build(self):

        # --------------------------------
        # CONFIGURACIÓN DE LA VENTANA
        # --------------------------------

        self.page.window.min_width = self.MIN_WIDTH
        self.page.window.min_height = 600

        # --------------------------------
        # ENCABEZADO
        # --------------------------------

        icono = ft.Icon(
            ft.Icons.RECEIPT,
            size=42,
            color="#848282",
        )

        titulo = ft.Text(
            "Generador de Tickets",
            size=28,
            weight=ft.FontWeight.BOLD,
            color="#000000",
            text_align=ft.TextAlign.CENTER,
        )

        subtitulo = ft.Text(
            "Selecciona tu negocio para comenzar",
            size=15,
            color="#777777",
            text_align=ft.TextAlign.CENTER,
        )

        encabezado = ft.Column(
            controls=[
                icono,
                titulo,
                subtitulo,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        )

        # --------------------------------
        # LISTA RESPONSIVE DE NEGOCIOS
        # --------------------------------

        self.negocios = ft.ResponsiveRow(
            columns=12,
            spacing=12,
            run_spacing=12,
        )

        self._refresh_businesses()

        # --------------------------------
        # BOTÓN AGREGAR NEGOCIO
        # --------------------------------

        self.agregar_negocio = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "+",
                            size=28,
                            color="#777777",
                        ),
                        width=52,
                        height=52,
                        bgcolor="#F0EEE9",
                        border_radius=14,
                        alignment=ft.Alignment.CENTER,
                    ),

                    ft.Column(
                        controls=[
                            ft.Text(
                                "Agregar negocio",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),

                            ft.Text(
                                "Personaliza con logo y nombre",
                                size=13,
                                color="#777777",
                            ),
                        ],
                        spacing=3,
                        expand=True,
                    ),

                    ft.Text(
                        "›",
                        size=30,
                        color="#AAAAAA",
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),

            padding=16,
            border_radius=16,
            border=ft.Border.all(1, "#DDDDD7"),
            bgcolor="#FFFFFF",

            on_click=self._agregar_negocio,
        )

        # --------------------------------
        # CONTENIDO PRINCIPAL
        # --------------------------------

        contenido = ft.Column(
            controls=[
                ft.Row(
                    controls=[encabezado],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                ft.Container(
                    height=20,
                ),

                self.negocios,

                ft.Container(
                    height=10,
                ),

                self.agregar_negocio,
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        # --------------------------------
        # CONTENEDOR CENTRAL
        # --------------------------------

        contenido_centrado = ft.Row(
            controls=[
                ft.Container(
                    content=contenido,
                    width=self.MAX_CONTENT_WIDTH,
                    expand=True,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )

        # --------------------------------
        # PÁGINA
        # --------------------------------

        self.page.controls.clear()

        self.page.add(
            ft.Container(
                content=contenido_centrado,
                expand=True,
                bgcolor="#F8F7F2",
                padding=20,
            )
        )

        self.page.update()

    # ============================================================
    # ACTUALIZAR NEGOCIOS
    # ============================================================

    def _refresh_businesses(self):

        self.negocios.controls.clear()

        for business in self.businesses:

            self.negocios.controls.append(
                ft.Container(
                    content=self._create_business_card(business),
                    col={
                        "xs": 12,
                        "sm": 6,
                        "md": 4,
                        "lg": 4,
                        "xl": 3,
                    },
                )
            )

    # ============================================================
    # TARJETA DE NEGOCIO
    # ============================================================

    def _create_business_card(self, business: Business):

        logo = ft.Image(
            src=business.logo,
            width=55,
            height=55,
        )

        informacion = ft.Column(
            controls=[
                ft.Text(
                    business.name,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    max_lines=1,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),

                ft.Text(
                    business.description,
                    size=13,
                    color="#777777",
                    max_lines=1,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
            ],
            spacing=3,
            expand=True,
        )

        contenido = ft.Row(
            controls=[
                ft.Container(
                    content=logo,
                    width=58,
                    height=58,
                    bgcolor="#F5F3ED",
                    border_radius=14,
                    alignment=ft.Alignment.CENTER,
                ),

                informacion,

                ft.Text(
                    "›",
                    size=30,
                    color="#AAAAAA",
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.Container(
            content=contenido,
            padding=16,
            bgcolor="#FFFFFF",
            border_radius=16,

            shadow=ft.BoxShadow(
                blur_radius=8,
                spread_radius=0,
                color="#18000000",
            ),

            on_click=lambda e, b=business: self._select_business(b),
        )

    # ============================================================
    # SELECCIONAR NEGOCIO
    # ============================================================

    def _select_business(self, business: Business):
        ClientView(self.page, business)

    # ============================================================
    # AGREGAR NEGOCIO
    # ============================================================

    def _agregar_negocio(self, e):
        AddNegocioView(self.page, self._business_saved)

    def _business_saved(self, business):
        if business is not None:
            self.businesses.append(business)
            save_businesses(self.businesses)
        self._build()
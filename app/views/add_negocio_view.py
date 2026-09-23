import base64

import flet as ft

from models.business import Business


class AddNegocioView:
    def __init__(self, page: ft.Page, on_saved):
        self.page = page
        self.on_saved = on_saved
        self.selected_image_path = None
        self.selected_image_data = None
        self.file_picker = ft.FilePicker()
        self.page.services.append(self.file_picker)
        self._build()

    def _build(self):
        self.name_field = ft.TextField(
            label="Nombre del negocio",
            autofocus=True,
            color= "grey",
            bgcolor= "#FFFFFF",
            border_radius= 12,
            border_color= "grey"
        )
        self.description_field = ft.TextField(
            label="Descripción",
            hint_text="Ej. Renta de muebles y artículos",
            color= "grey",
            bgcolor= "#FFFFFF",
            border_radius= 12,
            border_color= "grey"
        )
        self.services_field = ft.TextField(
            label="Servicios o conceptos frecuentes",
            hint_text="Ej. Sillas, Mesas, Manteles, Carpas",
            multiline=True,
            min_lines=2,
            max_lines=3,
            color="grey",
            bgcolor="#FFFFFF",
            border_radius=12,
            border_color="grey",
        )
        self.image_preview = ft.Image(
            src="logos/business_d03b31717a2b49fe92efe014dad60809.png",
            width=120,
            height=120,
        )
        self.image_error = ft.Text(
            color="#B3261E",
            size=12,
        )

        contenido = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            tooltip="Regresar",
                            on_click=self._cancelar,
                            icon_color="black",
                        ),
                        ft.Text(
                            "Agregar negocio",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color= "black"
                        ),
                    ],
                ),
                ft.Text(
                    "Personaliza el nombre, descripción e imagen de tu negocio.",
                    color="grey",
                ),
                ft.Container(
                    content=self.image_preview,
                    width=160,
                    height=160,
                    bgcolor="#FEFEFE", # Color para la imagen
                    border_radius=16,
                    border=ft.Border.all(1, "grey"),
                    alignment=ft.Alignment.CENTER,
                ),
                ft.OutlinedButton(
                    "Elegir imagen",
                    icon=ft.Icons.IMAGE_OUTLINED,
                    on_click=self._choose_image,
                    style=ft.ButtonStyle(
                        bgcolor="#1E0F60",
                        color="#FFFFFF",
                    ),
                ),
                self.image_error,
                self.name_field,
                self.description_field,
                self.services_field,
                ft.Text(
                    "Sepáralos con comas para mostrarlos al crear tickets.",
                    size=12,
                    color="grey",
                ),
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            "Cancelar", # Cancelar Boton
                            on_click=self._cancelar,
                            style=ft.ButtonStyle(
                                bgcolor="red",
                                color="#FFFFFF",
                            ),
                        ),
                        ft.ElevatedButton(
                            "Guardar negocio", #guardar negocio boton
                            icon=ft.Icons.SAVE_OUTLINED,
                            on_click=self._save_business,
                            style=ft.ButtonStyle(
                                bgcolor="#0E085B",
                                color="#FFFFFF",
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            width=520,
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
        )

        self.page.controls.clear()
        self.page.add(
            ft.Container(
                content=contenido,
                expand=True,
                bgcolor="#F8F7F2", # Color de Fondo de la vista
                padding=20,
                alignment=ft.Alignment.TOP_CENTER,
            )
        )
        self.page.update()

    async def _choose_image(self, e):
        files = await self.file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE,
            with_data=True,
        )

        if not files:
            return

        self.selected_image_path = files[0].path
        if files[0].bytes:
            self.selected_image_data = base64.b64encode(files[0].bytes).decode("ascii")
            self.image_preview.src = self.selected_image_data
        elif self.selected_image_path:
            self.image_preview.src = self.selected_image_path
        else:
            self.image_error.value = "No se pudo leer la imagen seleccionada"
            self.image_error.update()
            return
        self.image_error.value = ""
        self.page.update()

    def _save_business(self, e):
        name = self.name_field.value.strip()
        if not name:
            self.name_field.error_text = "Escribe el nombre del negocio"
            self.name_field.update()
            return

        if not self.selected_image_path:
            self.image_error.value = "Selecciona una imagen para continuar"
            self.image_error.update()
            return

        business = Business(
            name=name,
            description=self.description_field.value.strip() or "Nuevo negocio",
            logo=f"base64:{self.selected_image_data}",
            services=[
                service.strip()
                for service in (self.services_field.value or "").split(",")
                if service.strip()
            ],
        )
        self.page.services.remove(self.file_picker)
        self.on_saved(business)

    def _cancelar(self, e):
        self.page.services.remove(self.file_picker)
        self.on_saved(None)

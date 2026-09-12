from pathlib import Path
import shutil
import uuid

import flet as ft

from models.business import Business


class AddNegocioView:
    def __init__(self, page: ft.Page, on_saved):
        self.page = page
        self.on_saved = on_saved
        self.selected_image_path = None
        self.file_picker = ft.FilePicker()
        self.page.services.append(self.file_picker)
        self._build()

    def _build(self):
        self.name_field = ft.TextField(
            label="Nombre del negocio",
            autofocus=True,
        )
        self.description_field = ft.TextField(
            label="Descripción",
            hint_text="Ej. Renta de muebles y artículos",
        )
        self.image_preview = ft.Image(
            src="logos/corexis.png",
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
                        ),
                        ft.Text(
                            "Agregar negocio",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                ),
                ft.Text(
                    "Personaliza el nombre, descripción e imagen de tu negocio.",
                    color="#343333",
                ),
                ft.Container(
                    content=self.image_preview,
                    width=160,
                    height=160,
                    bgcolor="#F5F3ED",
                    border_radius=16,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.OutlinedButton(
                    "Elegir imagen",
                    icon=ft.Icons.IMAGE_OUTLINED,
                    on_click=self._choose_image,
                ),
                self.image_error,
                self.name_field,
                self.description_field,
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            "Cancelar",
                            on_click=self._cancelar,
                        ),
                        ft.ElevatedButton(
                            "Guardar negocio",
                            icon=ft.Icons.SAVE_OUTLINED,
                            on_click=self._save_business,
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
                bgcolor="#F8F7F2",
                padding=20,
                alignment=ft.Alignment.TOP_CENTER,
            )
        )
        self.page.update()

    async def _choose_image(self, e):
        files = await self.file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE,
        )

        if not files:
            return

        self.selected_image_path = files[0].path
        self.image_preview.src = self.selected_image_path
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

        logos_directory = Path(__file__).resolve().parent.parent / "assets" / "logos"
        logos_directory.mkdir(parents=True, exist_ok=True)
        extension = Path(self.selected_image_path).suffix.lower() or ".png"
        logo_name = f"business_{uuid.uuid4().hex}{extension}"
        destination = logos_directory / logo_name
        shutil.copy2(self.selected_image_path, destination)

        business = Business(
            name=name,
            description=self.description_field.value.strip() or "Nuevo negocio",
            logo=f"logos/{logo_name}",
        )
        self.page.services.remove(self.file_picker)
        self.on_saved(business)

    def _cancelar(self, e):
        self.page.services.remove(self.file_picker)
        self.on_saved(None)

# Ticket Digital

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13%2B-3776AB?style=for-the-badge&logo=python" alt="Python 3.13+" />
  <img src="https://img.shields.io/badge/Flet-0.86.5-4F46E5?style=for-the-badge" alt="Flet" />
  <img src="https://img.shields.io/badge/Status-Active-22C55E?style=for-the-badge" alt="Status Active" />
</p>

Ticket Digital es una aplicación desarrollada con Python y Flet para gestionar negocios y generar tickets personalizados para clientes. Está diseñada para facilitar la creación de comprobantes claros, ordenados y listos para compartir o imprimir.

## Visión general

La aplicación permite:

- Registrar múltiples negocios con nombre, descripción y logo
- Guardar información del cliente y sus datos de contacto
- Crear conceptos de compra con cantidades y precios unitarios
- Calcular automáticamente el total del ticket
- generar una vista final del comprobante con diseño profesional
- Almacenar los negocios localmente en el equipo para reutilizar la información

## Características principales

- Interfaz visual moderna construida con Flet
- Gestión de varios negocios desde una sola app
- Soporte para imágenes de logo y personalización visual
- Generación de tickets con formato legible y actualizado
- Persistencia local mediante archivos JSON
- Diseño adaptable para pantallas pequeñas y medianas
- Base lista para ampliar funcionalidades de negocio y ventas

## Stack tecnológico

- Python 3.13+
- Flet
- Pillow
- qrcode

## Estructura del proyecto

```text
ticket-digital/
├── main.py                 # punto de entrada principal de la app
├── requirements.txt        # dependencias del proyecto
├── README.md               # documentación general
├── app/
│   ├── main.py             # arranque de la interfaz Flet
│   ├── assets/             # logos, fuentes y recursos visuales
│   ├── data/               # datos base del proyecto
│   ├── models/             # entidades del dominio (negocio, ticket)
│   ├── services/           # lógica de almacenamiento y generación del ticket
│   └── views/              # pantallas principales de la aplicación
├── tests/
│   ├── test_ticket_generator.py
│   └── test_storage.py
├── build/
│   └── flutter/            # artefactos generados para compilación
├── .venv/                  # entorno virtual local (si se crea)
└── .gitignore
```

## Requisitos previos

- Python 3.13 o superior
- pip actualizado
- Git
- Windows, Linux o macOS

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/LuisCarrilloF/ticket-digital.git
cd ticket-digital
```

2. Crea un entorno virtual:

```powershell
py -3.13 -m venv .venv
```

3. Activa el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```
o con las teclas `Ctrl` + `Shift` + `p`, seleccionas la opción recomendada y vuelves a abrir la terminal.

4. Instala las dependencias:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Ejecución local

Desde la raíz del proyecto:

```powershell
python main.py
```

O bien:

```powershell
flet run
```

El archivo principal de ejecución es [main.py](main.py), que inicializa la app y configura la carpeta de assets.

## Compilación APK

Para generar una versión Android del proyecto:

```powershell
.\venv\Scripts\flet.exe build apk
```

Esto genera el artefacto de compilación dentro de la estructura de Flet/Flutter del proyecto.

## Persistencia de datos

La aplicación guarda la información de negocios en el almacenamiento local del usuario. Por ejemplo, en Windows suele quedar en:

```text
%USERPROFILE%\.ticket_digital\businesses.json
```

Esto permite que la app recuerde los negocios creados entre sesiones.

## Pruebas

El proyecto incluye pruebas para validar la generación del ticket y el almacenamiento local:

```powershell
python -m pytest -q
```

También puedes usar el módulo estándar de Python:

```powershell
python -m unittest discover -s tests
```

## Flujo de uso

1. Abre la aplicación.
2. Agrega o selecciona un negocio.
3. Define los datos del cliente.
4. Añade los conceptos y precios.
5. Genera el ticket final.
6. Revisa el total y comparte o imprime el comprobante.

## Convenciones del proyecto

- La lógica de negocio se separa por responsabilidades dentro de `app/models`, `app/services` y `app/views`.
- La capa visual está construida en Flet.
- La lógica de exportación y generación del ticket se mantiene centralizada para facilitar mantenimiento.

## Roadmap sugerido

- edición y eliminación de negocios
- historial de tickets
- exportación a PDF
- soporte multi-moneda
- catálogo de servicios por negocio
- mejoras de UX y validaciones de formularios

## Contribuciones

Las contribuciones son bienvenidas. Si deseas colaborar:

1. haz un fork del proyecto
2. crea una rama con tu cambio
3. agrega o actualiza pruebas si aplica
4. abre un pull request describiendo claramente el objetivo del cambio

## Licencia

Este proyecto se distribuye bajo una licencia de uso interno y académico. Revisa el archivo de licencia si se agrega en el repositorio antes de usarlo en producción o distribuirlo.

---

Hecho para facilitar la gestión de negocios pequeños y la generación de tickets profesionales con una experiencia rápida y clara.

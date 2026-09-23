import base64
from pathlib import Path


ASSETS_DIRECTORY = Path(__file__).resolve().parent.parent / "assets"


def image_source(logo: str):
    if logo.startswith("base64:"):
        return base64.b64decode(logo.removeprefix("base64:"))

    image_file = ASSETS_DIRECTORY / logo
    if image_file.exists():
        return image_file.read_bytes()

    return logo

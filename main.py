import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "app"))

from app.main import main

if __name__ == "__main__":
    import flet as ft
    ft.run(
        main,
        assets_dir=str(Path(__file__).resolve().parent / "app" / "assets"),
    )
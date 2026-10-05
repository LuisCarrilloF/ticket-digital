import json
import os
from pathlib import Path

from models.business import Business


BUNDLED_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "businesses.json"
APP_DATA_DIR = Path(os.environ.get("FLET_APP_STORAGE_DATA", Path.home()))
DATA_FILE = APP_DATA_DIR / ".ticket_digital" / "businesses.json"


def load_businesses():
	data_file = DATA_FILE if DATA_FILE.exists() else BUNDLED_DATA_FILE
	if not data_file.exists():
		return []

	try:
		data = json.loads(data_file.read_text(encoding="utf-8"))
	except (OSError, json.JSONDecodeError):
		return []

	return [
		Business(
			name=item["name"],
			description=item.get("description", "Nuevo negocio"),
			logo=item["logo"],
			services=item.get("services", []),
		)
		for item in data
	]


def save_businesses(businesses):
	DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
	data = [
		{
			"name": business.name,
			"description": business.description,
			"logo": business.logo,
			"services": business.services,
		}
		for business in businesses
	]
	DATA_FILE.write_text(
		json.dumps(data, ensure_ascii=False, indent=2),
		encoding="utf-8",
	)


def clear_businesses():
	DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
	DATA_FILE.write_text("[]", encoding="utf-8")


def reset_businesses():
	if DATA_FILE.exists():
		DATA_FILE.unlink()
	if BUNDLED_DATA_FILE.exists():
		BUNDLED_DATA_FILE.write_text("[]", encoding="utf-8")

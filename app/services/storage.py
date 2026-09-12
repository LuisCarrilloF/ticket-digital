import json
from pathlib import Path

from models.business import Business


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "businesses.json"


def load_businesses():
	if not DATA_FILE.exists():
		return []

	try:
		data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
	except (OSError, json.JSONDecodeError):
		return []

	return [
		Business(
			name=item["name"],
			description=item.get("description", "Nuevo negocio"),
			logo=item["logo"],
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
		}
		for business in businesses
	]
	DATA_FILE.write_text(
		json.dumps(data, ensure_ascii=False, indent=2),
		encoding="utf-8",
	)

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

import services.storage as storage


class ClearBusinessesTest(unittest.TestCase):
    def test_clear_businesses_writes_empty_store(self):
        temp_dir = Path(__file__).resolve().parent / "tmp_storage"
        temp_dir.mkdir(exist_ok=True)
        data_file = temp_dir / "businesses.json"
        default_file = temp_dir / "default_businesses.json"

        original_data = storage.DATA_FILE
        original_default = storage.BUNDLED_DATA_FILE
        storage.DATA_FILE = data_file
        storage.BUNDLED_DATA_FILE = default_file

        try:
            storage.clear_businesses()
            self.assertTrue(data_file.exists())
            self.assertEqual(data_file.read_text(encoding="utf-8"), "[]")
            self.assertEqual(storage.load_businesses(), [])
        finally:
            storage.DATA_FILE = original_data
            storage.BUNDLED_DATA_FILE = original_default


if __name__ == "__main__":
    unittest.main()

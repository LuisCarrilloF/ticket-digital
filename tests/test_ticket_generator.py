import sys
import unittest
from decimal import Decimal
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from models.ticket import Ticket, TicketItem
from services.ticket_generator import generate_ticket_png


class TicketGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.ticket = Ticket(
            "Diversiones Santa Ana",
            {
                "full_name": "Luis Carrillo",
                "phone": "3122148595",
                "address": "Dirección Revolución 14",
                "notes": "prueba",
            },
            [
                TicketItem("sillas", 100, Decimal("15.00")),
                TicketItem("manteles", 4, Decimal("40.00")),
            ],
            business_description="renta de muebles",
        )

    def render(self, ticket=None):
        return generate_ticket_png(
            ticket or self.ticket,
            "20260923-1628",
            "miércoles, 23 de septiembre de 2026 - 04:28 PM",
        )

    def test_bundled_font_supports_spanish_text(self):
        font_path = Path(__file__).resolve().parents[1] / "app" / "assets" / "fonts" / "NotoSans-Variable.ttf"
        font = ImageFont.truetype(str(font_path), 20)
        font.set_variation_by_name("Regular")

        self.assertIsNotNone(font.getbbox("áéíóúñü ¿¡"))

    def test_generates_valid_png_with_adaptive_height(self):
        basic_image = Image.open(BytesIO(self.render()))
        basic_image.verify()
        basic_image = Image.open(BytesIO(self.render()))
        basic_size = basic_image.size
        self.assertEqual(basic_image.getpixel((10, 10)), (247, 245, 240))
        self.assertEqual(basic_image.getpixel((60, 40)), (0, 13, 85))

        long_ticket = Ticket(
            self.ticket.business_name,
            {
                **self.ticket.customer,
                "address": "Dirección Revolución 14, colonia Centro " * 5,
                "notes": "miércoles, teléfono, dirección, pingüino ¿qué? ¡sí! " * 12,
            },
            [
                TicketItem(
                    "sillas plegables para eventos y reuniones " * 4,
                    100,
                    Decimal("15.00"),
                ),
                *self.ticket.items[1:],
            ],
            business_description="renta de muebles " * 8,
        )
        long_image_data = self.render(long_ticket)
        long_image = Image.open(BytesIO(long_image_data))
        long_image.verify()
        long_size = Image.open(BytesIO(long_image_data)).size

        self.assertEqual(basic_size[0], long_size[0])
        self.assertGreater(long_size[1], basic_size[1])
        self.assertGreater(len(long_image_data), 0)


if __name__ == "__main__":
    unittest.main()
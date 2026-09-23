from dataclasses import dataclass
from decimal import Decimal


@dataclass
class TicketItem:
	concept: str
	quantity: int
	unit_price: Decimal

	@property
	def subtotal(self) -> Decimal:
		return self.unit_price * self.quantity


@dataclass
class Ticket:
	business_name: str
	customer: dict
	items: list[TicketItem]
	business_logo: str = ""
	business_description: str = ""

	@property
	def total(self) -> Decimal:
		return sum((item.subtotal for item in self.items), Decimal("0"))

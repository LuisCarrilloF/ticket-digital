from models.ticket import Ticket
from xml.sax.saxutils import escape
from io import BytesIO


def format_amount(amount) -> str:
	return f"$ {amount:,.2f}"


def generate_ticket(ticket: Ticket) -> str:
	lines = [
		"TICKET DIGITAL",
		ticket.business_name,
		"",
		f"Cliente: {ticket.customer['full_name']}",
		f"Teléfono: {ticket.customer['phone']}",
		f"Dirección: {ticket.customer['address']}",
	]

	if ticket.customer.get("notes"):
		lines.append(f"Notas: {ticket.customer['notes']}")

	lines.extend(["", "CONCEPTOS"])

	for item in ticket.items:
		lines.append(
			f"{item.concept} | {item.quantity} x "
			f"{format_amount(item.unit_price)} = {format_amount(item.subtotal)}"
		)

	lines.extend(["", f"TOTAL: {format_amount(ticket.total)}"])
	return "\n".join(lines)


def generate_ticket_svg(ticket: Ticket, ticket_number: str, date_text: str) -> str:
	rows = []
	y = 485
	for item in ticket.items:
		concept = escape(item.concept)
		subtotal = escape(format_amount(item.subtotal))
		unit_price = escape(format_amount(item.unit_price))
		rows.append(
			f'<text x="70" y="{y}" class="item">{concept}</text>'
			f'<text x="930" y="{y}" text-anchor="end" class="amount">{subtotal}</text>'
			f'<text x="70" y="{y + 28}" class="detail">{item.quantity} x {unit_price}</text>'
		)
		y += 92

	height = max(930, y + 220)
	name = escape(ticket.business_name)
	description = escape(ticket.customer["full_name"])
	phone = escape(ticket.customer["phone"])
	address = escape(ticket.customer["address"])
	notes = escape(ticket.customer.get("notes", ""))
	notes_block = ""
	if notes:
		notes_y = y + 100
		notes_block = (
			f'<rect x="50" y="{notes_y}" width="900" height="100" rx="18" fill="#FFF3C4"/>'
			f'<text x="75" y="{notes_y + 32}" class="label">NOTAS</text>'
			f'<text x="75" y="{notes_y + 68}" class="detail">{notes}</text>'
		)

	return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}">
<rect width="1000" height="{height}" fill="#F7F5F0"/>
<rect x="35" y="35" width="930" height="150" rx="24" fill="#000D55"/>
<text x="70" y="88" class="brand">{name}</text>
<text x="70" y="122" class="description">{description}</text>
<text x="70" y="160" class="ticket">TICKET #{escape(ticket_number)}</text>
<rect x="50" y="215" width="900" height="145" rx="22" fill="#FFFFFF" stroke="#E1DDD7"/>
<text x="75" y="255" class="label">FECHA</text>
<text x="75" y="288" class="detail">{escape(date_text)}</text>
<text x="75" y="326" class="customer">{description}</text>
<text x="560" y="255" class="label">TELÉFONO</text>
<text x="560" y="288" class="detail">{phone}</text>
<text x="560" y="326" class="label">DIRECCIÓN</text>
<text x="560" y="350" class="detail">{address}</text>
<rect x="50" y="390" width="900" height="{y + 40 - 390}" rx="22" fill="#FFFFFF" stroke="#E1DDD7"/>
<text x="75" y="425" class="label">CONCEPTOS</text>
{''.join(rows)}
<rect x="50" y="{y + 25}" width="900" height="90" fill="#FFF3C4"/>
<text x="75" y="{y + 80}" class="customer">TOTAL A PAGAR</text>
<text x="925" y="{y + 80}" text-anchor="end" class="total">{escape(format_amount(ticket.total))}</text>
{notes_block}
<style>
.brand {{ font-family: sans-serif; font-size: 30px; font-weight: 700; fill: #FFFFFF; }}
.description {{ font-family: sans-serif; font-size: 16px; fill: #F2F3F8; }}
.ticket {{ font-family: sans-serif; font-size: 14px; font-weight: 700; fill: #FFFFFF; }}
.label {{ font-family: sans-serif; font-size: 13px; font-weight: 700; fill: #817A73; }}
.customer {{ font-family: sans-serif; font-size: 18px; font-weight: 700; fill: #000000; }}
.item {{ font-family: sans-serif; font-size: 18px; font-weight: 700; fill: #000000; }}
.detail {{ font-family: sans-serif; font-size: 15px; fill: #555555; }}
.amount, .total {{ font-family: sans-serif; font-size: 19px; font-weight: 700; fill: #000D55; }}
.total {{ font-size: 28px; }}
</style>
</svg>'''


def generate_ticket_png(ticket: Ticket, ticket_number: str, date_text: str) -> bytes:
	from PIL import Image, ImageDraw, ImageFont
	from pathlib import Path
	import textwrap

	font_path = Path("C:/Windows/Fonts/arial.ttf")
	font_bold_path = Path("C:/Windows/Fonts/arialbd.ttf")
	if font_path.exists() and font_bold_path.exists():
		font_regular = ImageFont.truetype(str(font_path), 20)
		font_bold = ImageFont.truetype(str(font_bold_path), 20)
		font_small = ImageFont.truetype(str(font_path), 16)
		font_label = ImageFont.truetype(str(font_bold_path), 15)
		font_total = ImageFont.truetype(str(font_bold_path), 32)
	else:
		font_regular = ImageFont.load_default()
		font_bold = ImageFont.load_default()
		font_small = font_regular
		font_label = font_bold
		font_total = font_bold

	width = 720
	margin = 30
	row_height = 88
	header_height = 190
	height = max(980, 760 + len(ticket.items) * row_height)
	image = Image.new("RGB", (width, height), "#F7F5F0")
	draw = ImageDraw.Draw(image)

	def text(position, value, fill="#000000", font=font_regular, anchor=None):
		draw.text(position, value, fill=fill, font=font, anchor=anchor)

	draw.rounded_rectangle(
		(margin, 25, width - margin, header_height),
		radius=24,
		fill="#000D55",
	)
	logo_box = (margin + 20, 50, margin + 130, 160)
	draw.rounded_rectangle(logo_box, radius=18, fill="#FFFFFF")
	logo_file = None
	if not ticket.business_logo.startswith("base64:"):
		logo_file = Path(__file__).resolve().parent.parent / "assets" / ticket.business_logo
	if logo_file and logo_file.exists():
		with Image.open(logo_file) as logo:
			logo.thumbnail((88, 88))
			image.paste(logo.convert("RGB"), (margin + 31, 61))

	text((margin + 145, 58), ticket.business_name, "#FFFFFF", font_bold)
	description = "Renta de muebles y artículos"
	for index, line in enumerate(textwrap.wrap(description, width=34)[:2]):
		text((margin + 145, 92 + index * 24), line, "#F2F3F8", font_small)
	draw.rounded_rectangle((margin + 145, 138, margin + 360, 174), radius=8, fill="#24306E")
	text((margin + 160, 147), f"TICKET #{ticket_number}", "#FFFFFF", font_label)

	info_top = header_height + 30
	draw.rounded_rectangle((margin, info_top, width - margin, info_top + 190), radius=22, fill="#FFFFFF", outline="#E1DDD7")
	text((margin + 25, info_top + 30), date_text, "#817A73", font_small)
	text((margin + 25, info_top + 78), ticket.customer["full_name"], "#000000", font_bold)
	text((margin + 25, info_top + 115), f"Teléfono: {ticket.customer['phone']}", "#555555", font_small)
	text((margin + 25, info_top + 150), f"Dirección: {ticket.customer['address']}", "#555555", font_small)

	concepts_top = info_top + 220
	concepts_bottom = concepts_top + 75 + len(ticket.items) * row_height + 100
	draw.rounded_rectangle(
		(margin, concepts_top, width - margin, concepts_bottom),
		radius=22,
		fill="#FFFFFF",
		outline="#E1DDD7",
	)
	text((margin + 25, concepts_top + 35), "CONCEPTOS", "#817A73", font_label)
	y = concepts_top + 85
	for item in ticket.items:
		text((margin + 25, y), item.concept, "#000000", font_bold)
		text((width - margin - 25, y), format_amount(item.subtotal), "#000D55", font_bold, anchor="ra")
		text((margin + 25, y + 30), f"{item.quantity} x {format_amount(item.unit_price)}", "#555555", font_small)
		y += row_height

	draw.rectangle((margin, y + 20, width - margin, y + 125), fill="#FFF3C4")
	text((margin + 25, y + 60), "TOTAL A PAGAR", "#000000", font_bold)
	text((width - margin - 25, y + 55), format_amount(ticket.total), "#000D55", font_total, anchor="ra")

	if ticket.customer.get("notes"):
		notes_y = y + 135
		draw.rounded_rectangle((margin, notes_y, width - margin, notes_y + 100), radius=18, fill="#FFF3C4")
		text((margin + 25, notes_y + 30), "NOTAS", "#000D55", font_label)
		text((margin + 25, notes_y + 65), ticket.customer["notes"], "#000000", font_small)

	output = BytesIO()
	image.save(output, format="PNG")
	return output.getvalue()

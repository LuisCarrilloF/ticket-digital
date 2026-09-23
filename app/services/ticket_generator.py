from models.ticket import Ticket
from xml.sax.saxutils import escape
from io import BytesIO

from services.image_loader import image_source


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

	assets_dir = Path(__file__).resolve().parent.parent / "assets"
	font_dir = assets_dir / "fonts"

	def load_font(size, bold=False):
		font_names = ("DejaVuSans-Bold.ttf", "NotoSans-Bold.ttf") if bold else ("DejaVuSans.ttf", "NotoSans-Regular.ttf")
		for font_name in font_names:
			font_file = font_dir / font_name
			if font_file.exists():
				try:
					return ImageFont.truetype(str(font_file), size)
				except OSError:
					pass
		return ImageFont.load_default()

	font_regular = load_font(20)
	font_bold = load_font(20, bold=True)
	font_small = load_font(16)
	font_label = load_font(15, bold=True)
	font_total = load_font(32, bold=True)
	width = 720
	margin = 30
	content_width = width - (margin * 2)
	padding = 25
	image = Image.new("RGB", (width, 4000), "#F7F5F0")
	draw = ImageDraw.Draw(image)

	def wrap(value, font, max_width):
		words = str(value or "").split()
		lines = []
		current = ""
		for word in words:
			candidate = f"{current} {word}".strip()
			if current and draw.textlength(candidate, font=font) > max_width:
				lines.append(current)
				current = word
			else:
				current = candidate
		if current:
			lines.append(current)
		return lines or [""]

	def line_height(font):
		return max(20, draw.textbbox((0, 0), "Ag", font=font)[3] + 5)

	def draw_lines(x, y, value, font, fill, max_width, spacing=4):
		lines = wrap(value, font, max_width)
		height = line_height(font)
		for line in lines:
			draw.text((x, y), line, fill=fill, font=font)
			y += height + spacing
		return y, len(lines)

	def load_logo():
		try:
			logo_data = image_source(ticket.business_logo or "")
			if not isinstance(logo_data, bytes):
				return None
			with Image.open(BytesIO(logo_data)) as source:
				logo = source.convert("RGBA")
				logo.thumbnail((100, 100))
				return logo.copy()
		except (OSError, ValueError, TypeError):
			return None

	header_top = 25
	description = ticket.business_description or ""
	description_lines = wrap(description, font_small, 365)
	header_height = max(190, 55 + len(description_lines) * 24 + 55)
	draw.rounded_rectangle((margin, header_top, width - margin, header_top + header_height), radius=24, fill="#000D55")
	logo_box = (margin + 20, header_top + 25, margin + 130, header_top + 135)
	draw.rounded_rectangle(logo_box, radius=18, fill="#FFFFFF")
	logo = load_logo()
	if logo:
		logo_x = logo_box[0] + (110 - logo.width) // 2
		logo_y = logo_box[1] + (110 - logo.height) // 2
		image.paste(logo, (logo_x, logo_y), logo)

	draw_lines(margin + 145, header_top + 28, ticket.business_name, font_bold, "#FFFFFF", 365)
	draw_lines(margin + 145, header_top + 65, description, font_small, "#F2F3F8", 365)
	ticket_y = header_top + header_height - 45
	draw.rounded_rectangle((margin + 145, ticket_y, margin + 360, ticket_y + 36), radius=8, fill="#24306E")
	draw.text((margin + 160, ticket_y + 9), f"TICKET #{ticket_number}", fill="#FFFFFF", font=font_label)

	info_top = header_top + header_height + 30
	info_lines = []
	info_lines.extend(wrap(date_text, font_small, content_width - padding * 2))
	info_lines.extend(wrap(ticket.customer.get("full_name", ""), font_bold, content_width - padding * 2))
	info_lines.extend(wrap(f"Teléfono: {ticket.customer.get('phone', '')}", font_small, content_width - padding * 2))
	info_lines.extend(wrap(f"Dirección: {ticket.customer.get('address', '')}", font_small, content_width - padding * 2))
	info_height = 35 + sum(line_height(font_small) + 4 for _ in info_lines[:1]) + 15
	info_height += sum(line_height(font_bold) + 4 for _ in wrap(ticket.customer.get("full_name", ""), font_bold, content_width - padding * 2))
	info_height += sum(line_height(font_small) + 4 for _ in info_lines[2:]) + 20
	draw.rounded_rectangle((margin, info_top, width - margin, info_top + info_height), radius=22, fill="#FFFFFF", outline="#E1DDD7")
	y = info_top + 30
	y, _ = draw_lines(margin + padding, y, date_text, font_small, "#817A73", content_width - padding * 2)
	y += 12
	y, _ = draw_lines(margin + padding, y, ticket.customer.get("full_name", ""), font_bold, "#000000", content_width - padding * 2)
	y += 4
	y, _ = draw_lines(margin + padding, y, f"Teléfono: {ticket.customer.get('phone', '')}", font_small, "#555555", content_width - padding * 2)
	draw_lines(margin + padding, y, f"Dirección: {ticket.customer.get('address', '')}", font_small, "#555555", content_width - padding * 2)

	concepts_top = info_top + info_height + 20
	row_data = []
	for item in ticket.items:
		concept_lines = wrap(item.concept, font_bold, content_width - padding * 2 - 180)
		row_data.append((item, concept_lines, max(70, len(concept_lines) * (line_height(font_bold) + 3) + 42)))
	concepts_height = 60 + sum(row[2] for row in row_data) + 125
	draw.rounded_rectangle((margin, concepts_top, width - margin, concepts_top + concepts_height), radius=22, fill="#FFFFFF", outline="#E1DDD7")
	draw.text((margin + padding, concepts_top + 30), "CONCEPTOS", fill="#817A73", font=font_label)
	y = concepts_top + 75
	for item, concept_lines, row_height in row_data:
		for line in concept_lines:
			draw.text((margin + padding, y), line, fill="#000000", font=font_bold)
			y += line_height(font_bold) + 3
		draw.text((width - margin - padding, y - len(concept_lines) * (line_height(font_bold) + 3)), format_amount(item.subtotal), fill="#000D55", font=font_bold, anchor="ra")
		draw.text((margin + padding, y + 5), f"{item.quantity} x {format_amount(item.unit_price)}", fill="#555555", font=font_small)
		y += row_height - len(concept_lines) * (line_height(font_bold) + 3) - 5

	total_top = concepts_top + concepts_height - 125
	draw.rectangle((margin, total_top, width - margin, total_top + 105), fill="#FFF3C4")
	draw.text((margin + padding, total_top + 38), "TOTAL A PAGAR", fill="#000000", font=font_bold)
	draw.text((width - margin - padding, total_top + 30), format_amount(ticket.total), fill="#000D55", font=font_total, anchor="ra")

	bottom = concepts_top + concepts_height
	if ticket.customer.get("notes"):
		notes_lines = wrap(ticket.customer["notes"], font_small, content_width - padding * 2)
		notes_height = 55 + len(notes_lines) * (line_height(font_small) + 3)
		draw.rounded_rectangle((margin, bottom + 15, width - margin, bottom + 15 + notes_height), radius=18, fill="#FFF3C4")
		draw.text((margin + padding, bottom + 38), "NOTAS", fill="#000D55", font=font_label)
		draw.multiline_text((margin + padding, bottom + 65), "\n".join(notes_lines), fill="#000000", font=font_small, spacing=3)
		bottom += 15 + notes_height

	image = image.crop((0, 0, width, bottom + 30))
	output = BytesIO()
	image.save(output, format="PNG")
	return output.getvalue()

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
	font_file = font_dir / "NotoSans-Variable.ttf"

	def load_font(size, bold=False):
		if font_file.is_file():
			font = ImageFont.truetype(str(font_file), size)
			if bold:
				font.set_variation_by_name("Bold")
			return font
		return ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", size)

	font_regular = load_font(20)
	font_bold = load_font(21, bold=True)
	font_small = load_font(18)
	font_label = load_font(16, bold=True)
	font_total = load_font(34, bold=True)
	width = 900
	margin = 36
	content_width = width - (margin * 2)
	padding = 28
	text_content = [
		ticket.business_name,
		ticket.business_description,
		date_text,
		*(str(value) for value in ticket.customer.values()),
		*(item.concept + str(item.quantity) + str(item.unit_price) for item in ticket.items),
	]
	canvas_height = max(4000, 1500 + 2 * sum(len(value) for value in text_content) + 180 * len(ticket.items))
	image = Image.new("RGB", (width, canvas_height), "#F7F5F0")
	draw = ImageDraw.Draw(image)

	def wrap(value, font, max_width):
		words = str(value or "").split()
		lines = []
		current = ""
		for word in words:
			candidate = f"{current} {word}".strip()
			if draw.textlength(candidate, font=font) <= max_width:
				current = candidate
				continue
			if current:
				lines.append(current)
				current = ""
			for character in word:
				candidate = current + character
				if current and draw.textlength(candidate, font=font) > max_width:
					lines.append(current)
					current = character
				else:
					current = candidate
		if current:
			lines.append(current)
		return lines or [""]

	def line_height(font):
		return max(20, draw.textbbox((0, 0), "Ag", font=font)[3] + 5)

	def draw_lines(x, y, value, font, fill, max_width, spacing=4, anchor=None):
		lines = value if isinstance(value, list) else wrap(value, font, max_width)
		height = line_height(font)
		for line in lines:
			draw.text((x, y), line, fill=fill, font=font, anchor=anchor)
			y += height + spacing
		return y, len(lines)

	def fitting_font(value, preferred, minimum, max_width, bold=True):
		font = load_font(preferred, bold)
		while font.size > minimum and draw.textlength(value, font=font) > max_width:
			font = load_font(font.size - 1, bold)
		return font

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
	logo_size = 132
	logo_text_x = margin + 175
	header_text_width = width - margin - padding - logo_text_x
	name_lines = wrap(ticket.business_name, font_bold, header_text_width)
	description_lines = wrap(description, font_small, header_text_width)
	name_height = len(name_lines) * (line_height(font_bold) + 3)
	description_height = len(description_lines) * (line_height(font_small) + 3)
	header_height = max(190, padding * 2 + max(logo_size, name_height + description_height + 48))
	draw.rounded_rectangle((margin, header_top, width - margin, header_top + header_height), radius=24, fill="#000D55")
	logo_box = (margin + 20, header_top + (header_height - logo_size) // 2, margin + 20 + logo_size, header_top + (header_height + logo_size) // 2)
	draw.rounded_rectangle(logo_box, radius=18, fill="#FFFFFF")
	logo = load_logo()
	if logo:
		logo_x = logo_box[0] + (logo_size - logo.width) // 2
		logo_y = logo_box[1] + (logo_size - logo.height) // 2
		image.paste(logo, (logo_x, logo_y), logo)

	header_y = header_top + (header_height - (name_height + description_height + 48)) // 2
	header_y, _ = draw_lines(logo_text_x, header_y, name_lines, font_bold, "#FFFFFF", header_text_width, spacing=3)
	header_y, _ = draw_lines(logo_text_x, header_y, description_lines, font_small, "#F2F3F8", header_text_width, spacing=3)
	ticket_text = f"TICKET #{ticket_number}"
	ticket_y = header_top + header_height - padding - line_height(font_label) - 10
	ticket_width = draw.textlength(ticket_text, font=font_label) + 28
	draw.rounded_rectangle((logo_text_x, ticket_y, logo_text_x + ticket_width, ticket_y + 40), radius=9, fill="#24306E")
	draw.text((logo_text_x + 14, ticket_y + 10), ticket_text, fill="#FFFFFF", font=font_label)

	info_top = header_top + header_height + 30
	info_width = content_width - padding * 2
	info_fields = [
		(date_text, font_small, "#817A73", 8),
		(ticket.customer.get("full_name", ""), font_bold, "#000000", 4),
		(f"Teléfono: {ticket.customer.get('phone', '')}", font_small, "#555555", 4),
		(f"Dirección: {ticket.customer.get('address', '')}", font_small, "#555555", 0),
	]
	info_lines = [(wrap(value, font, info_width), font, color, spacing) for value, font, color, spacing in info_fields]
	info_height = padding * 2 + sum(len(lines) * (line_height(font) + spacing) for lines, font, _, spacing in info_lines)
	draw.rounded_rectangle((margin, info_top, width - margin, info_top + info_height), radius=22, fill="#FFFFFF", outline="#E1DDD7")
	y = info_top + padding
	for lines, font, color, spacing in info_lines:
		y, _ = draw_lines(margin + padding, y, lines, font, color, info_width, spacing=spacing)

	concepts_top = info_top + info_height + 20
	row_data = []
	amount_width = 220
	concept_width = content_width - padding * 2 - amount_width - 16
	for item in ticket.items:
		concept_lines = wrap(item.concept, font_bold, concept_width)
		amount_text = format_amount(item.subtotal)
		amount_font = fitting_font(amount_text, font_bold.size, 16, amount_width)
		detail = f"{item.quantity} x {format_amount(item.unit_price)}"
		row_height = max(
			line_height(font_small) + 8 + line_height(font_bold) * len(concept_lines),
			line_height(amount_font) + line_height(font_small) + 8,
		) + 24
		row_data.append((item, concept_lines, amount_text, amount_font, detail, row_height))
	concepts_height = padding + line_height(font_label) + 28 + sum(row[5] for row in row_data) + 130
	draw.rounded_rectangle((margin, concepts_top, width - margin, concepts_top + concepts_height), radius=22, fill="#FFFFFF", outline="#E1DDD7")
	draw.text((margin + padding, concepts_top + padding), "CONCEPTOS", fill="#817A73", font=font_label)
	y = concepts_top + padding + line_height(font_label) + 28
	for _, concept_lines, amount_text, amount_font, detail, row_height in row_data:
		row_top = y
		draw_lines(margin + padding, row_top, concept_lines, font_bold, "#000000", concept_width, spacing=3)
		draw.text((width - margin - padding, row_top), amount_text, fill="#000D55", font=amount_font, anchor="ra")
		detail_y = row_top + len(concept_lines) * (line_height(font_bold) + 3) + 5
		draw.text((margin + padding, detail_y), detail, fill="#555555", font=font_small)
		y += row_height

	total_top = concepts_top + concepts_height - 125
	draw.rectangle((margin, total_top, width - margin, total_top + 105), fill="#FFF3C4")
	draw.text((margin + padding, total_top + 38), "TOTAL A PAGAR", fill="#000000", font=font_bold)
	total_text = format_amount(ticket.total)
	total_font = fitting_font(total_text, font_total.size, 22, content_width - padding * 2 - 210)
	draw.text((width - margin - padding, total_top + 30), total_text, fill="#000D55", font=total_font, anchor="ra")

	bottom = concepts_top + concepts_height
	if ticket.customer.get("notes"):
		notes_lines = []
		for note_line in str(ticket.customer["notes"]).splitlines() or [""]:
			notes_lines.extend(wrap(note_line, font_small, content_width - padding * 2))
		notes_height = padding * 2 + line_height(font_label) + 8 + len(notes_lines) * (line_height(font_small) + 3)
		draw.rounded_rectangle((margin, bottom + 15, width - margin, bottom + 15 + notes_height), radius=18, fill="#FFF3C4")
		draw.text((margin + padding, bottom + 15 + padding), "NOTAS", fill="#000D55", font=font_label)
		draw_lines(margin + padding, bottom + 15 + padding + line_height(font_label) + 8, notes_lines, font_small, "#000000", content_width - padding * 2, spacing=3)
		bottom += 15 + notes_height

	image = image.crop((0, 0, width, bottom + 30))
	output = BytesIO()
	image.save(output, format="PNG")
	return output.getvalue()

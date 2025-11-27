from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import qrcode
from reportlab.pdfbase.pdfmetrics import stringWidth

def generate_vin_pdf(vin_no, unique_id, output_file="output.pdf"):
    page_width, page_height = A4  # Portrait

    c = canvas.Canvas(output_file, pagesize=A4)

    # ---- BORDER ----
    margin = 7 * mm
    c.setLineWidth(3)
    c.rect(margin, margin, page_width - 2 * margin, page_height - 2 * margin)

    # ---- VIN NO (top text) ----
    vin_font_size = 80
    c.setFont("Helvetica-Bold", vin_font_size)
    
    text_width = stringWidth(vin_no, "Helvetica-Bold", vin_font_size)
    c.drawString((page_width - text_width) / 2, page_height - 40 * mm, vin_no)

    # ---- QR CODE ----
    qr_size = 180 * mm  # large QR
    qr = qrcode.QRCode(box_size=10, border=1)
    qr.add_data(f"VIN NO: {vin_no} UNIQUE ID: {unique_id}")
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    qr_x = (page_width - qr_size) / 2
    qr_y = (page_height / 2) - (qr_size / 2)
    c.drawImage(ImageReader(img), qr_x, qr_y, qr_size, qr_size)

    # ---- UNIQUE ID (bottom text) ----
    uid_font_size = 115
    c.setFont("Helvetica-Bold", uid_font_size)
    uid_text_width = stringWidth(unique_id, "Helvetica-Bold", uid_font_size)

    c.drawString((page_width - uid_text_width) / 2, margin + 20 * mm, unique_id)

    # Save PDF
    c.save()
    print(f"PDF saved as {output_file}")


# Example usage:
generate_vin_pdf("VIN1234567", "@AA1234", "vin_label.pdf")

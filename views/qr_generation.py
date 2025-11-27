import streamlit as st
import pandas as pd
from datetime import datetime
import io
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from utils.data_manager import get_new_unique_id

def draw_qr_page(c, vin_no, date):
    """
    Draws a single page with QR code on the given canvas.
    """
    page_width, page_height = A4
    
    # Get a new unique ID
    try:
        unique_id = get_new_unique_id()
    except Exception as e:
        st.error(f"Error generating Unique ID: {e}")
        unique_id = "ERROR-UID"

    # ---- BORDER ----
    margin = 7 * mm
    c.setLineWidth(3)
    c.rect(margin, margin, page_width - 2 * margin, page_height - 2 * margin)

    # ---- VIN NO (top text) ----
    vin_font_size = 80
    c.setFont("Helvetica-Bold", vin_font_size)
    
    text_width = stringWidth(str(vin_no), "Helvetica-Bold", vin_font_size)
    c.drawString((page_width - text_width) / 2, page_height - 40 * mm, str(vin_no))

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

def generate_pdf(vin_no, date):
    """
    Generates a single-page PDF with QR code and returns the bytes.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    draw_qr_page(c, vin_no, date)
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

def generate_bulk_pdf(vin_list, date):
    """
    Generates a multi-page PDF with QR codes for each VIN in the list.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    for vin_no in vin_list:
        draw_qr_page(c, vin_no, date)
        c.showPage()
        
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

def show():
    st.header("QR Generation")
    
    option = st.radio("Select Input Method:", ["Manually", "Using CSV file"])
    
    if option == "Manually":
        col1, col2 = st.columns(2)
        with col1:
            vin_no = st.text_input("VIN No.")
        with col2:
            date_input = st.date_input("Date", value=datetime.today())
        
        if st.button("Generate QR"):
            if vin_no:
                st.success(f"Generating QR for VIN: {vin_no} on {date_input}")
                
                # Generate PDF
                pdf_data = generate_pdf(vin_no, date_input)
                
                # Show Download Button
                st.download_button(
                    label="Download PDF",
                    data=pdf_data,
                    file_name=f"QR_Report_{vin_no}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Please enter a VIN No.")
                
    elif option == "Using CSV file":
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        
        # Date input for CSV batch
        date_input = st.date_input("Select Date for Batch", value=datetime.today())
        
        if uploaded_file is not None:
            st.success("File uploaded successfully!")
            df = pd.read_csv(uploaded_file)
            st.write("Preview:", df.head())
            
            if st.button("Generate QRs from CSV"):
                # Check for VIN NO column (case-insensitive)
                vin_col = next((col for col in df.columns if col.upper() == "VIN NO"), None)
                
                if vin_col:
                    st.info(f"Generating QRs for {len(df)} rows...")
                    
                    # Generate Bulk PDF
                    vin_list = df[vin_col].tolist()
                    pdf_data = generate_bulk_pdf(vin_list, date_input)
                    
                    st.success("Bulk PDF Generated!")
                    
                    # Show Download Button
                    st.download_button(
                        label="Download Bulk PDF",
                        data=pdf_data,
                        file_name=f"Bulk_QR_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("CSV must contain a 'VIN NO' column.")

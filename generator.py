import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

def create_overlay(excel_file, overlay_file, client_name, date):
    df = pd.read_excel(excel_file)

    # Take Name and Number from the first row of Excel
    excel_name = str(df.loc[0, "Name"]) if "Name" in df.columns else ""
    #excel_number = str(df.loc[0, "Number"]) if "Number" in df.columns else ""
    if "Number" in df.columns:
        number_val = df.loc[0, "Number"]
        # Handle both int-like and string cases
        if pd.api.types.is_number(number_val):
            # Remove decimal if it's a whole number
            excel_number = str(int(number_val))
        else:
            excel_number = str(number_val)
    else:
        excel_number = ""

    c = canvas.Canvas(overlay_file, pagesize=A4)

    # === Client and Date ===
    c.setFont("Times-Bold", 12)
    c.drawString(50, 710, client_name)
    c.drawString(470, 710, date)

    # === Excel Name and Number at top right ===
    if excel_name or excel_number:
        c.setFont("Times-Bold", 12)
        c.drawRightString(550, 815, f"{excel_name}   {excel_number}")
    
    # === Table ===
    start_y = 600
    row_height = 33
    x_positions = [25, 60, 260, 385, 453, 508]

    # for i, row in df.iterrows():
    #     y = start_y - i * row_height
    #     c.setFont("Times-Bold", 10)
    #     c.drawString(x_positions[0] + 2, y, str(i+1))
    #     c.drawString(x_positions[1] + 2, y, str(row["Item"]))
    #     c.drawString(x_positions[2] + 2, y, str(row["Make"]))
    #     c.drawString(x_positions[3] + 2, y, str(row["Quantity"]))
    #     c.drawString(x_positions[4] + 2, y, str(row["Rate"]))
    #     c.drawString(x_positions[5] + 2, y, str(row["Packing"]))
    col_widths  = [35, 200, 125, 68, 55, 70]

    # === Table rows ===
    for i, row in df.iterrows():
        y = start_y - i * row_height
        c.setFont("Times-Bold", 11)

        values = [
            str(i+1),
            str(row["Item"]),
            str(row["Make"]),
            str(row["Rate"]),
            str(row["Per"]),
            str(row["Packing"])
        ]

        for j, text in enumerate(values):
            text_width = c.stringWidth(text, "Times-Roman", 10)
            x_center = x_positions[j] + (col_widths[j] / 2) - (text_width / 2)
            c.drawString(x_center, y, text)
    c.save()

def merge_with_template(template_file, overlay_file, output_file):
    template_pdf = PdfReader(template_file)
    overlay_pdf = PdfReader(overlay_file)
    writer = PdfWriter()

    for page, overlay in zip(template_pdf.pages, overlay_pdf.pages):
        page.merge_page(overlay)
        writer.add_page(page)

    with open(output_file, "wb") as f:
        writer.write(f)

def generate_quotation(excel_file, template_file="quotation FINAL-1.pdf", output_file="quotation_output.pdf", client_name="M/s ................", date="................"):
    overlay_file = "overlay.pdf"
    create_overlay(excel_file, overlay_file, client_name, date)
    merge_with_template(template_file, overlay_file, output_file)
    return output_file

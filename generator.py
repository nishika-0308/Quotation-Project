from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

def create_overlay(df, overlay_file, client_name, date, excel_name="", excel_number=""):
    c = canvas.Canvas(overlay_file, pagesize=A4)

    # === Client and Date ===
    c.setFont("Times-Bold", 12)
    c.drawString(50, 710, client_name)
    c.drawString(470, 710, date)

    # === Excel Name and Number at top right ===
    if excel_name or excel_number:
        c.setFont("Times-Bold", 12)
        c.drawRightString(550, 815, f"{excel_name}   {excel_number}")

    # === Table calibration ===
    start_y = 600
    row_height = 33
    x_positions = [25, 62, 260, 385, 453, 508]
    col_widths  = [37, 198, 125, 68, 55, 70]

    # === Table rows (left aligned text) ===
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
            if j == 1:  # Item column → left aligned
                c.drawString(x_positions[j] + 2, y, text)
            else:  # Center align all other columns
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

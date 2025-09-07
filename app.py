import streamlit as st
from datetime import datetime
from generator import generate_quotation, create_overlay, merge_with_template

st.title("📄 Quotation Generator")

st.write("Upload your excel file, enter client details, and choose what to generate.")

# File upload
excel_file = st.file_uploader("Upload Excel file", type=["xlsx"])

# Inputs
client_name = st.text_input("Client Name")
date_val = st.text_input("Date (dd-mm-yyyy)", value=datetime.today().strftime("%d-%m-%Y"))

# Build safe filenames
def make_filenames(client, date):
    safe_client = "".join(c for c in client if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    safe_date = date.replace("/", "-").replace(" ", "_")
    overlay_file = f"overlay_{safe_client}_{safe_date}.pdf"
    output_file = f"quotation_{safe_client}_{safe_date}.pdf"
    return overlay_file, output_file

# === Button: Generate Quotation PDF ===
if st.button("Generate Quotation PDF"):
    if excel_file and client_name:
        with open("uploaded.xlsx", "wb") as f:
            f.write(excel_file.getbuffer())

        overlay_file, output_file = make_filenames(client_name, date_val)

        create_overlay("uploaded.xlsx", overlay_file, client_name, date_val)
        merge_with_template("quotation FINAL.pdf", overlay_file, output_file)

        with open(output_file, "rb") as f:
            st.download_button(
                "⬇️ Download Quotation PDF",
                f,
                file_name=output_file
            )
    else:
        st.error("Please upload an Excel file and enter client name.")


# === Button: Generate Overlay PDF ===
if st.button("Generate Print Overlay PDF"):
    if excel_file and client_name:
        with open("uploaded.xlsx", "wb") as f:
            f.write(excel_file.getbuffer())

        overlay_file, _ = make_filenames(client_name, date_val)

        create_overlay("uploaded.xlsx", overlay_file, client_name, date_val)

        with open(overlay_file, "rb") as f:
            st.download_button(
                "⬇️ Download Print Overlay PDF",
                f,
                file_name=overlay_file
            )
    else:
        st.error("Please upload an Excel file and enter client name.")
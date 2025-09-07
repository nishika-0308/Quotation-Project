import streamlit as st
from datetime import datetime
from generator import generate_quotation, create_overlay, merge_with_template

st.title("📄 Quotation Generator")

st.write("Upload your Excel file, enter client details, and download a ready quotation PDF.")

# File upload
excel_file = st.file_uploader("Upload Excel file", type=["xlsx"])

# Inputs
client_name = st.text_input("Client Name")
date_val = st.text_input("Date (dd-mm-yyyy)", value=datetime.today().strftime("%d-%m-%Y"))

if st.button("Generate PDF"):
    if excel_file and client_name:
        # Save uploaded file temporarily
        with open("uploaded.xlsx", "wb") as f:
            f.write(excel_file.getbuffer())

        # Create overlay first
        overlay_file = "overlay.pdf"
        create_overlay("uploaded.xlsx", overlay_file, client_name, date_val)

        # Merge with template
        output_file = f"quotation_output.pdf"
        merge_with_template("quotation FINAL copy.pdf", overlay_file, output_file)

        # Download Quotation
        with open(output_file, "rb") as f:
            st.download_button(
                "⬇️ Download Quotation PDF",
                f,
                file_name=output_file
            )

        # Download Overlay
        with open(overlay_file, "rb") as f:
            st.download_button(
                "⬇️ Download Overlay PDF",
                f,
                file_name="overlay.pdf"
            )

    else:
        st.error("Please upload an Excel file and enter client name.")

import streamlit as st
from datetime import datetime
import os
from generator import generate_quotation

st.title("📄 Quotation Generator")

st.write("Upload your excel file, enter client details, and download a ready quotation PDF.")

# File upload
excel_file = st.file_uploader("Upload Excel file", type=["xlsx"])

# Inputs
client_name = st.text_input("Client Name")
date_val = st.text_input("Date (dd-mm-yyyy)", value=datetime.today().strftime("%d-%m-%Y"))

# Generate
if st.button("Generate PDF"):
    if excel_file and client_name:
        # Save uploaded file temporarily
        with open("uploaded.xlsx", "wb") as f:
            f.write(excel_file.getbuffer())

        output_file = "quotation_output.pdf"
        generate_quotation(
            "uploaded.xlsx",
            template_file="quotation FINAL.pdf",
            output_file=output_file,
            client_name=client_name,
            date=date_val
        )

        # Download button
        with open(output_file, "rb") as f:
            st.download_button("⬇️ Download Quotation PDF", f, file_name="quotation.pdf")

    else:
        st.error("Please upload an Excel file and enter client name.")

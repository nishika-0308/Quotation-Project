import streamlit as st
from datetime import datetime
import os
from generator import generate_quotation

st.title("📄 Quotation Generator")

st.write("Upload your Excel file, enter client details, and download a ready quotation PDF.")

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

        # === Create custom filename ===
        safe_client = "".join(c for c in client_name if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
        safe_date = date_val.replace("/", "-").replace(" ", "_")
        output_file = f"quotation_{safe_client}_{safe_date}.pdf"

        # Generate quotation
        generate_quotation(
            "uploaded.xlsx",
            template_file="quotation FINAL.pdf",
            output_file=output_file,
            client_name=client_name,
            date=date_val
        )

        # Download button with custom name
        with open(output_file, "rb") as f:
            st.download_button(
                "⬇️ Download Quotation PDF",
                f,
                file_name=output_file
            )

    else:
        st.error("Please upload an Excel file and enter client name.")
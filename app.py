import streamlit as st
from datetime import datetime
import pandas as pd
from generator import create_overlay, merge_with_template

st.title("📄 Quotation Generator")

# SAVE_FILE = "saved_items.csv"

# # Load saved items
# if os.path.exists(SAVE_FILE):
#     saved_items = pd.read_csv(SAVE_FILE)["item"].dropna().tolist()
# else:
#     saved_items = []
st.write("Choose how you want to provide input: either upload an Excel file or enter manually.")

# Option: Excel upload OR manual entry
input_mode = st.radio("Select input mode:", ["Upload Excel", "Manual Entry"])

client_name = ""
date_val = datetime.today().strftime("%d-%m-%Y")
excel_name = ""
excel_number = ""
chemicals_df = None

if input_mode == "Upload Excel":
    # === Excel Upload ===
    excel_file = st.file_uploader("Upload Excel file", type=["xlsx"])
    client_name = st.text_input("Client Name")
    date_val = st.text_input("Date (dd-mm-yyyy)", value=date_val)

    if excel_file:
        df = pd.read_excel(excel_file)

        # Read Name & Number from first row if present
        if "Name" in df.columns:
            excel_name = str(df.loc[0, "Name"])
        if "Number" in df.columns:
            number_val = df.loc[0, "Number"]
            if isinstance(number_val, (int, float)):
                excel_number = str(int(number_val))
            else:
                excel_number = str(number_val)

        chemicals_df = df[["Item", "Make", "Rate", "Per", "Packing"]]

elif input_mode == "Manual Entry":
    # === Manual Entry ===
    client_name = st.text_input("Client Name")
    date_val = st.text_input("Date (dd-mm-yyyy)", value=date_val)
    excel_name = st.text_input("Location Name")
    excel_number = st.text_input("Contact Number")

    st.write("### Enter Chemical Details")
    data = pd.DataFrame({
        "Item": [""],
        "Make": [""],
        "Rate": [""],
        "Per": [""],
        "Packing": [""]
    })
    chemicals_df = st.data_editor(data, num_rows="dynamic")

# === Helper: Build safe filenames ===
def make_filenames(client, date):
    safe_client = "".join(c for c in client if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    safe_date = date.replace("/", "-").replace(" ", "_")
    overlay_file = f"overlay_{safe_client}_{safe_date}.pdf"
    output_file = f"quotation_{safe_client}_{safe_date}.pdf"
    return overlay_file, output_file

# === Buttons ===

if st.button("Generate Quotation PDF"):
    if client_name and chemicals_df is not None and not chemicals_df.empty:
        overlay_file, output_file = make_filenames(client_name, date_val)
        create_overlay(chemicals_df, overlay_file, client_name, date_val, excel_name, excel_number)
        merge_with_template("quotation FINAL.pdf", overlay_file, output_file)

        with open(output_file, "rb") as f:
            st.download_button("⬇️ Download Quotation PDF", f, file_name=output_file)
    else:
        st.error("Please enter details and at least one chemical.")
    # === Overlay PDF Generation ===
if st.button("Generate Overlay PDF"):
    if client_name and chemicals_df is not None and not chemicals_df.empty:
        overlay_file, _ = make_filenames(client_name, date_val)
        create_overlay(chemicals_df, overlay_file, client_name, date_val, excel_name, excel_number)

        with open(overlay_file, "rb") as f:
            st.download_button("⬇️ Download Overlay PDF", f, file_name=overlay_file)
    else:
        st.error("Please enter details and at least one chemical.")
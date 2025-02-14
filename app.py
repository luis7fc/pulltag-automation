import streamlit as st
import pandas as pd
import copy
import json

# Load or initialize the opportunity dictionary
OPPORTUNITY_FILE = "opportunity.json"

try:
    with open(OPPORTUNITY_FILE, "r") as f:
        opportunity = json.load(f)
except FileNotFoundError:
    opportunity = {
        "magnolia": {
            "10red": 100, "10blk": 100, "8grn": 100, "34flex": 100,
            "rom103": 50, "sf1base": 1, "sf1hem": 1
        },
        "mission oaks": {
            "10red": 100, "10blk": 100, "8grn": 100, "34flex": 100,
            "rom103": 50, "sf1base": 1
        }
    }

st.title("📊 Job Lot Processor & Opportunity Manager")

import streamlit as st
import json

# Load or initialize the opportunity dictionary
OPPORTUNITY_FILE = "opportunity.json"

try:
    with open(OPPORTUNITY_FILE, "r") as f:
        opportunity = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    opportunity = {}

# Ensure Streamlit session state stores the dictionary
if "opportunity" not in st.session_state:
    st.session_state.opportunity = opportunity

# Sidebar for managing opportunities
st.sidebar.header("⚙️ Manage Opportunities")

# Input for job name
job_name_input = st.sidebar.text_input("Enter a job name:")
if job_name_input:
    job_name = job_name_input.lower()

    # Get existing materials or start fresh
    existing_materials = st.session_state.opportunity.get(job_name, {})

    st.sidebar.subheader(f"🛠️ Edit Materials for '{job_name_input}'")

    # Editable fields for existing materials
    updated_materials = {}
    for material, qty in existing_materials.items():
        updated_qty = st.sidebar.number_input(f"{material}", value=qty, step=1)
        updated_materials[material] = updated_qty

    # New material entry
    new_material = st.sidebar.text_input("Add new material:")
    new_qty = st.sidebar.number_input("Quantity", min_value=0, step=1, value=0)

    if st.sidebar.button("➕ Add Material"):
        if new_material:
            updated_materials[new_material] = new_qty
            st.session_state.opportunity[job_name] = updated_materials
            st.sidebar.success(f"Added '{new_material}' with quantity {new_qty}")

    # Save updated job materials
    if st.sidebar.button("✅ Save Job"):
        if updated_materials:
            st.session_state.opportunity[job_name] = updated_materials
            with open(OPPORTUNITY_FILE, "w") as f:
                json.dump(st.session_state.opportunity, f, indent=4)
            st.sidebar.success(f"Updated '{job_name_input}' successfully! ✅")
        else:
            st.sidebar.warning("No materials added! Please enter at least one material.")

# Display updated dictionary live
st.sidebar.write("📝 Jobs currently in the dictionary:")
st.sidebar.json(st.session_state.opportunity)


# File uploader for processing Excel
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    activities_dict = {}

    for index, row in df.iterrows():
        lot_number = str(row['Lot #']).strip()
        job_name = str(row['Job Name']).strip().lower()
        job_number = str(row['Job Number']).strip()  # New column being used
        battery_status = str(row['Battery']).strip().lower()

        # New key format: "Lot # - Job Name - Job Number"
        activity_key = f"{lot_number} - {job_name} - {job_number}"

        if job_name in normalized_opportunity:
            materials = copy.deepcopy(normalized_opportunity[job_name])
        else:
            materials = {}

        if "battery_wire" in materials and battery_status != "yes":
            del materials["battery_wire"]

        activities_dict[activity_key] = materials

    # Sum up total wire allocations
    total_wire_allocated = {}
    for activity, materials in activities_dict.items():
        if isinstance(materials, dict):
            for material, quantity in materials.items():
                if material == "battery_wire" and isinstance(quantity, dict):
                    for bat_material, bat_quantity in quantity.items():
                        total_wire_allocated[bat_material] = total_wire_allocated.get(bat_material, 0) + bat_quantity
                else:
                    if isinstance(quantity, (int, float)):
                        total_wire_allocated[material] = total_wire_allocated.get(material, 0) + quantity

    # Display results
    st.subheader("📋 Final Activities Dictionary")
    st.json(activities_dict)

    st.subheader("⚡ Total Wire Allocation")
    for material, total in total_wire_allocated.items():
        st.write(f"- **{material}**: {total}")

st.info("Upload an Excel file to generate the activities dictionary.")

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# Function to generate a PDF
def generate_pdf(activities_dict):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 10)

    y_position = 750  # Start position for text

    pdf.drawString(100, 780, "Activities Dictionary Report")
    pdf.line(100, 775, 500, 775)  # Underline

    for activity, materials in activities_dict.items():
        pdf.drawString(100, y_position, f"{activity}:")
        y_position -= 15
        if isinstance(materials, dict):
            for material, quantity in materials.items():
                pdf.drawString(120, y_position, f"- {material}: {quantity}")
                y_position -= 15

        y_position -= 10  # Extra space between jobs

        if y_position < 50:  # Prevent text from running off the page
            pdf.showPage()
            y_position = 750

    pdf.save()
    buffer.seek(0)
    return buffer

# Streamlit section for PDF download
st.subheader("📥 Download Report")
if st.button("Generate & Download PDF"):
    pdf_buffer = generate_pdf(activities_dict)
    st.download_button(
        label="📄 Download PDF",
        data=pdf_buffer,
        file_name="activities_report.pdf",
        mime="application/pdf"
    )


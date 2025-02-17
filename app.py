import streamlit as st
import pandas as pd
import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Define the CSV file for storing opportunities
OPPORTUNITY_FILE = "opportunity.csv"

# Default opportunities (ensuring first-time app startup loads correctly)
DEFAULT_OPPORTUNITIES = {
    "magnolia": {"10red": 125, "10blk": 100, "8grn": 100, "34flex": 100, "rom103": 50, "sf1base": 1, "sf1hem": 1},
    "mission oaks": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "rom103": 50, "sf1base": 1},
    "abbey court ii": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 100, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25},
    "alder creek ii": {"34nstp": 25, "nailplt": 10, "qfp100": 1, "sf1base": 1, "rom143": 25, "rom43": 35, "rom63": 25, "184cshld": 25, "34flex": 100, "8grn": 100, "10blk": 100, "10red": 100},
    "gosford west": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25},
    "greenwood ii": {"34nstp": 25, "nailplt": 10, "qfp100": 1, "sf1base": 1, "rom143": 25, "rom63": 25, "rom43": 35, "184cshld": 25, "34flex": 100, "8grn": 100, "10red": 100, "10blk": 100},
    "santa fe trail": {"10blk": 100, "10red": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25},
    "serenade": {"10blk": 100, "10red": 100, "8grn": 100, "184cshld": 25, "34flex": 100, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25},
    "victory oaks": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25},
    "wild oak": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "rom43": 35, "rom63": 25, "rom143": 25, "184cshld": 25, "sf1base": 1, "qfp100": 1, "34nstp": 25, "nailplt": 10},
    "abbey park": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom43": 35, "rom63": 50, "rom143": 50, "sf1base": 2, "qfp100": 1, "nailplt": 10, "34nstp": 10, "sf1hem": 2},
    "acres at copper heights": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25, "sf1hem": 1},
    "canyon ridge at the preserve": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom43": 35, "rom63": 50, "rom143": 50, "sf1base": 2, "qfp100": 1, "nailplt": 10, "34nstp": 25, "sf1hem": 2},
    "ella gardens east": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25, "sf1hem": 1},
    "deauville 6389": {"10red": 200, "10blk": 200, "8grn": 150, "34flex": 100, "184cshld": 25, "sf1base": 2, "nailplt": 10, "34nstp": 25, "rom83": 50, "sf1dsa": 2},
    "deauville 6339": {"10red": 150, "10blk": 150, "8grn": 100, "34flex": 100, "184cshld": 25, "sf1base": 2, "nailplt": 10, "34nstp": 25, "rom83": 50, "sf1dsa": 2},
    "ivy gate at farmstead": {"sf1hem": 1, "34nstp": 25, "nailplt": 10, "qfp100": 1, "sf1base": 1, "rom143": 25, "rom63": 25, "rom43": 35, "184cshld": 25, "34flex": 100, "8grn": 100, "10red": 100, "10blk": 100},
    "trilogy nevina": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "sf1base": 1, "nailplt": 10, "34nstp": 25, "rom83": 25, "sf1dsa": 1},
    "orchards at copper heights" : {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25, "sf1hem": 1},
    "orchard view" : {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom63": 75, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25},
    "kings estates phase iii": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom83": 25, "sf1base": 1, "nailplt": 10, "34nstp": 25, "sf1dsa": 1},
    "oakcrest": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom103": 25, "rom63": 50, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25},
    "palm crossing tract 7093": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom83": 25, "sf1base": 1, "nailplt": 10, "34nstp": 25, "sf1dsa": 1},
    "citrea tract 6383": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom103": 50, "sf1base": 1, "nailplt": 10, "34nstp": 25},
    "ovation at riverstone": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25, "sf1hem": 1}    
    "encore at riverstone": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25, "sf1hem": 1}    

}

# --- FUNCTIONS ---

# Convert dictionary to DataFrame
def dict_to_dataframe(opportunities):
    data = []
    for job, materials in opportunities.items():
        for material, quantity in materials.items():
            data.append([job, material, quantity])
    return pd.DataFrame(data, columns=["Job Name", "Material", "Quantity"])

# Convert DataFrame back to dictionary
def dataframe_to_dict(df):
    opportunities = {}
    for _, row in df.iterrows():
        job = row["Job Name"]
        material = row["Material"]
        quantity = int(row["Quantity"])

        if job not in opportunities:
            opportunities[job] = {}
        opportunities[job][material] = quantity
    return opportunities

# Load opportunities from CSV or initialize defaults
def load_opportunities():
    if os.path.exists(OPPORTUNITY_FILE):
        df = pd.read_csv(OPPORTUNITY_FILE)
        return dataframe_to_dict(df)
    else:
        save_opportunities(DEFAULT_OPPORTUNITIES)
        return DEFAULT_OPPORTUNITIES  

# Save opportunities to CSV
def save_opportunities(opportunities):
    df = dict_to_dataframe(opportunities)
    df.to_csv(OPPORTUNITY_FILE, index=False)

# Function to sum all activity material quantities
def sum_total_materials(activities_dict):
    total_materials = {}
    for materials in activities_dict.values():
        for material, quantity in materials.items():
            total_materials[material] = total_materials.get(material, 0) + quantity
    return total_materials

# Function to generate a PDF report
def generate_pdf(activities_dict, total_materials):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 10)
    y_position = 750  # Start position for text

    pdf.drawString(100, 780, "Activities Dictionary Report")
    pdf.line(100, 775, 500, 775)  # Underline

    for activity, materials in activities_dict.items():
        pdf.drawString(100, y_position, f"{activity}:")
        y_position -= 15
        for material, quantity in materials.items():
            pdf.drawString(120, y_position, f"- {material}: {quantity}")
            y_position -= 15
            if y_position < 50:  # Prevent text from running off the page
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y_position = 750

        y_position -= 10  # Extra space between activities

    # Add total material summary
    pdf.showPage()  # New page for totals
    y_position = 750
    pdf.drawString(100, 780, "Total Material Allocation")
    pdf.line(100, 775, 500, 775)

    for material, total in total_materials.items():
        pdf.drawString(120, y_position, f"- {material}: {total}")
        y_position -= 15
        if y_position < 50:  # Prevent text from running off the page
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y_position = 750

    pdf.save()
    buffer.seek(0)
    return buffer

# Ensure session state is properly initialized with the updated opportunity dictionary
if "opportunity" not in st.session_state:
    st.session_state.opportunity = load_opportunities()

# --- UI ELEMENTS ---
st.title("📊 Job Lot Processor & Opportunity Manager")

# Sidebar for managing opportunities
st.sidebar.header("⚙️ Manage Opportunities")

# Display updated dictionary live in the sidebar
st.sidebar.write("📝 Jobs currently in the dictionary:")
st.sidebar.json(st.session_state.opportunity)

# Allow user to add/edit jobs in the dictionary
st.sidebar.subheader("➕ Add or Edit a Job")

# Input for job name
job_name_input = st.sidebar.text_input("Enter a job name:")
if job_name_input:
    job_name = job_name_input.lower()
    existing_materials = st.session_state.opportunity.get(job_name, {})

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
            save_opportunities(st.session_state.opportunity)
            st.sidebar.success(f"Added '{new_material}' with quantity {new_qty}")

    if st.sidebar.button("✅ Save Job"):
        if updated_materials:
            st.session_state.opportunity[job_name] = updated_materials
            save_opportunities(st.session_state.opportunity)
            st.sidebar.success(f"Updated '{job_name_input}' successfully! ✅")
        else:
            st.sidebar.warning("No materials added! Please enter at least one material.")

# --- FILE UPLOAD SECTION ---
st.subheader("📂 Upload Excel File for Job Processing")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    df.columns = df.columns.str.strip().str.lower()
    required_columns = {"lot #", "job name", "job number", "battery"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        st.error(f"⚠️ Missing required columns: {', '.join(missing_columns)}. Please check your Excel file.")
    else:
        activities_dict = {}

        for index, row in df.iterrows():
            lot_number = str(row["lot #"]).strip()
            job_name = str(row["job name"]).strip().lower()
            job_number = str(row["job number"]).strip()
            battery_status = str(row["battery"]).strip().lower()
            activity_key = f"{lot_number} - {job_name} - {job_number}"

            materials = st.session_state.opportunity.get(job_name, {}).copy()
            if "battery_wire" in materials and battery_status != "yes":
                del materials["battery_wire"]

            activities_dict[activity_key] = materials

        total_materials = sum_total_materials(activities_dict)

        st.subheader("📋 Final Activities Dictionary")
        st.json(activities_dict)

        st.subheader("🔢 Total Material Allocation")
        st.json(total_materials)

        if st.button("📄 Generate & Download PDF"):
            pdf_buffer = generate_pdf(activities_dict, total_materials)
            st.download_button("📥 Download PDF", data=pdf_buffer, file_name="activities_report.pdf", mime="application/pdf")

        st.success("✅ File processed successfully!")

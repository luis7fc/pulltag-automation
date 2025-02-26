import streamlit as st
import pandas as pd
import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

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
    "ovation at riverstone": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25, "sf1hem": 1},    
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

# --- Hard-Coded Defaults ---
DEFAULTS = {
    "line_id": "IL",
    "location": "FNOSolar",
    "conversion_factor": 1,
    "equipment_id": "",
    "equipment_cost_code": "",  # Now blank
    "category": "M",  # Now set to "M"
    "requisition_number": "",  # Now blank
}

# --- Hardcoded Item Data (itemcode → {description, job_cost_code, unit_of_measure}) ---
ITEM_DATA = {
    "10BLK": {"description": "#10 AWG THHN Wire Black", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "10RED": {"description": "#10 AWG THHN Wire Red", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "10WHT": {"description": "#10 AWG THHN Wire White", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "6BLK": {"description": "#6 AWG THHN Wire Black", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "6GRN": {"description": "#6 AWG THHN Wire Green", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "6RED": {"description": "#6 AWG THHN Wire Red", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "6WHT": {"description": "#6 AWG THHN Wire White", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "8BLK": {"description": "#8 AWG THHN Wire Black", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "8GRN": {"description": "#8 AWG THHN Wire Green", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "8RED": {"description": "#8 AWG THHN Wire Red", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "8WHT": {"description": "#8 AWG THHN Wire White", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "184CSHLD": {"description": "#18/4c Shielded Wire, 500'", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "1FLEX": {"description": '1" Aluminum Flex/FMC', "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "ROM103": {"description": "Romex 10-3", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "ROM122": {"description": "Romex 12-2", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "ROM123": {"description": "Romex 12-3", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "ROM142": {"description": "Romex 14-2", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "ROM143": {"description": "Romex 14-3", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "ROM83": {"description": "Romex 8-3", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "34EMT": {"description": 'EMT 3/4" Unthreaded Conduit', "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "34FLEX": {"description": '3/4" Aluminum Flex/FMC', "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "34NSTP": {"description": '3/4" Nail Strap (galv J-Nail)', "job_cost_code": "BOS", "unit_of_measure": "EA"},
    "NAILPLT": {"description": "Steel Nail Plate", "job_cost_code": "BOS", "unit_of_measure": "EA"},
    "SF1BASE": {"description": 'Solar Sub Flashing 3/4", 15"x12", Galv', "job_cost_code": "BOS", "unit_of_measure": "EA"},
    "SF1CMP": {"description": 'Solar Flashing 3/4" Galv 17" x 17", 2.5" Cone', "job_cost_code": "BOS", "unit_of_measure": "EA"},
    "SF1DSA": {"description": 'Solar Flashing 3/4" DSAlum, 2.5" Cone', "job_cost_code": "BOS", "unit_of_measure": "EA"},
    "SF1HEM": {"description": 'Solar Flashing 3/4" Galv Shake w/ Hem, 2.5" Cone', "job_cost_code": "BOS", "unit_of_measure": "EA"},
    "QFP100": {"description": 'Quickflash P-100 1/2"-3/4" Cond', "job_cost_code": "BOS", "unit_of_measure": "EA"},
    "QFP50": {"description": 'Quickflash P-50 1/2"-3/4" Cond', "job_cost_code": "BOS", "unit_of_measure": "EA"},
    "4BLK": {"description": "#4 Black", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "4RED": {"description": "#4 Red", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "4WHT": {"description": "#4 White", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "ROM43": {"description": "Romex 4-3", "job_cost_code": "BOS", "unit_of_measure": "FT"},
    "ROM63": {"description": "Romex 6-3", "job_cost_code": "BOS", "unit_of_measure": "FT"},
}


# --- TXT File Generation Function ---
def generate_sage_txt(activities_dict, defaults, item_data):
    """
    Generate a tab-delimited TXT string using the Sage criteria.
    
    - Extracts job number and lot number from activities_dict keys.
    - Pulls item descriptions, job cost codes, and unit of measure from ITEM_DATA.
    - Uses today's date as the issue date.
    """
    today_date = datetime.today().strftime("%m-%d-%y")  # Format: MM-DD-YY

    header1 = f"I\tTest Import\t{today_date}\t{today_date}"
    header2 = ";line ID\tlocation\titem code\tquantity\tunit of measure\tdescription\tconversion factor\tequipment id\tequipment cost code\tjob\tlot\tcost code\tcategory\trequisition number\tissue date"
    lines = [header1, header2]

    # Iterate over activities_dict and build data rows.
    for key, materials in activities_dict.items():
        try:
            lot_number, job_name, job_number = key.split(" - ")
        except ValueError:
            continue  # Skip improperly formatted keys

        for item_code, quantity in materials.items():
            # Pull item details or use defaults if missing
            item_details = item_data.get(item_code, {"description": "", "job_cost_code": "", "unit_of_measure": "EA"})
            description = item_details["description"]
            job_cost_code = item_details["job_cost_code"]
            unit_of_measure = item_details["unit_of_measure"]

            row = [
                defaults["line_id"],
                defaults["location"],
                item_code,
                str(quantity),
                unit_of_measure,  # Now pulled from ITEM_DATA
                description,
                str(defaults["conversion_factor"]),
                defaults["equipment_id"],
                defaults["equipment_cost_code"],  # Now blank
                job_number,       # Column J: Job number
                lot_number,       # Column K: Lot number
                job_cost_code,    # Column L: Job Cost Code
                defaults["category"],  # Now "M"
                defaults["requisition_number"],  # Now blank
                today_date  # Issue Date = Date the report is generated
            ]
            lines.append("\t".join(row))
    
    return "\n".join(lines)


st.subheader("Generate TXT Output")
if st.button("Generate & Download TXT"):
    sage_txt = generate_sage_txt(activities_dict, DEFAULTS, ITEM_DATA)
    st.download_button("Download TXT", data=sage_txt, file_name="sage_output.txt", mime="text/plain")


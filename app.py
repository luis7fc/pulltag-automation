import streamlit as st
import pandas as pd
import json
import os

# Define the JSON file for storing opportunities
OPPORTUNITY_FILE = "opportunity.json"

# Default opportunities (ensuring first-time app startup loads correctly)
DEFAULT_OPPORTUNITIES = {
    "magnolia": {"10red": 125, "10blk": 100, "8grn": 100, "34flex": 100, "rom103": 50, "sf1base": 1, "sf1hem": 1},
    "mission oaks": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "rom103": 50, "sf1base": 1},
    "citrea 303": {"8grn": 100},
    "abbey court ii": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 100, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25},
    "alder creek ii": {"34nstp": 25, "nailplt": 10, "qfp100": 1, "sf1base": 1, "rom143": 25, "rom43": 35, "rom63": 25, "184cshld": 25, "34flex": 100, "8grn": 100, "10blk": 100, "10red": 100},
    "gosford west": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25},
    "greenwood ii": {"34nstp": 25, "nailplt": 10, "qfp100": 1, "sf1base": 1, "rom143": 25, "rom63": 25, "rom43": 35, "184cshld": 25, "34flex": 100, "8grn": 100, "10red": 100, "10blk": 100},
    "santa fe trail": {"10blk": 100, "10red": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25},
    "serenade": {"10blk": 100, "10red": 100, "8grn": 100, "184cshld": 25, "34flex": 100, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25},
    "victory oaks": {"10red": 100, "10blk": 100, "8grn": 100, "34flex": 100, "184cshld": 25, "rom43": 35, "rom63": 25, "rom143": 25, "sf1base": 1, "qfp100": 1, "nailplt": 10, "34nstp": 25},
}

# Function to load opportunities from JSON or initialize defaults
def load_opportunities():
    if os.path.exists(OPPORTUNITY_FILE):
        try:
            with open(OPPORTUNITY_FILE, "r") as f:
                data = json.load(f)
                return data if data else DEFAULT_OPPORTUNITIES  # Use defaults if file is empty
        except json.JSONDecodeError:
            return DEFAULT_OPPORTUNITIES  # Return defaults if JSON is corrupted
    return DEFAULT_OPPORTUNITIES  # Return defaults if file doesn't exist

# Function to save opportunities to JSON
def save_opportunities(opportunities):
    with open(OPPORTUNITY_FILE, "w") as f:
        json.dump(opportunities, f, indent=4)

# Ensure session state is properly initialized with the opportunity dictionary
if "opportunity" not in st.session_state:
    st.session_state.opportunity = load_opportunities()
    save_opportunities(st.session_state.opportunity)  # Save to file to ensure persistence

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

    # Get existing materials or start fresh
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

    # Save updated job materials
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
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

        # Normalize column names to lowercase (avoid case-sensitivity issues)
        df.columns = df.columns.str.strip().str.lower()

        # Required columns
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

                # Ensure job exists in the dictionary
                if job_name in st.session_state.opportunity:
                    materials = st.session_state.opportunity[job_name].copy()
                else:
                    materials = {}

                # Handle battery wire removal
                if "battery_wire" in materials and battery_status != "yes":
                    del materials["battery_wire"]

                activities_dict[activity_key] = materials

            # Display results
            st.subheader("📋 Final Activities Dictionary")
            st.json(activities_dict)

            st.success("✅ File processed successfully!")

    except Exception as e:
        st.error(f"⚠️ Error processing file: {str(e)}")

st.info("Upload an Excel file to generate the activities dictionary.")

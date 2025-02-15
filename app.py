import streamlit as st
import pandas as pd
import copy
import json
import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Define the JSON file for saving opportunities
OPPORTUNITY_FILE = "opportunity.json"

# Default opportunities
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

# Function to load opportunities from a JSON file
def load_opportunities():
    """Load opportunities from a JSON file if it exists, else use defaults."""
    if os.path.exists(OPPORTUNITY_FILE):
        try:
            with open(OPPORTUNITY_FILE, "r") as f:
                data = json.load(f)
                if data:
                    return data  # Return existing data
        except json.JSONDecodeError:
            pass  # If file is corrupted, fall back to defaults
    return DEFAULT_OPPORTUNITIES  # Return defaults if file is empty or missing

# Function to save opportunities to a JSON file
def save_opportunities(opportunities):
    """Save opportunities to a JSON file."""
    with open(OPPORTUNITY_FILE, "w") as f:
        json.dump(opportunities, f, indent=4)

# Load existing opportunities or initialize with defaults
opportunity = load_opportunities()
save_opportunities(opportunity)  # Ensure the data is written to file

# Ensure Streamlit session state stores the dictionary
if "opportunity" not in st.session_state:
    st.session_state.opportunity = opportunity

# Streamlit App Title
st.title("📊 Job Lot Processor & Opportunity Manager")

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
            save_opportunities(st.session_state.opportunity)  # Save immediately
            st.sidebar.success(f"Added '{new_material}' with quantity {new_qty}")

    # Save updated job materials
    if st.sidebar.button("✅ Save Job"):
        if updated_materials:
            st.session_state.opportunity[job_name] = updated_materials
            save_opportunities(st.session_state.opportunity)  # Save immediately
            st.sidebar.success(f"Updated '{job_name_input}' successfully! ✅")
        else:
            st.sidebar.warning("No materials added! Please enter at least one material.")

# Display updated dictionary live
st.sidebar.write("📝 Jobs currently in the dictionary:")
st.sidebar.json(st.session_state.opportunity)

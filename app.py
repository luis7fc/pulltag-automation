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

# Default opportunities (for first-time use)
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
if not os.path.exists(OPPORTUNITY_FILE):
    save_opportunities(DEFAULT_OPPORTUNITIES)  # Save defaults if file does not exist

opportunity = load_opportunities()

# Ensure Streamlit session state stores the dictionary
if "opportunity" not in st.session_state or not st.session_state.opportunity:
    st.session_state.opportunity = opportunity  # Force reload if session is empty

# Streamlit App Title
st.title("📊 Job Lot Processor & Opportunity Manager")

# Sidebar for managing opportunities
st.sidebar.header("⚙️ Manage Opportunities")

# Display updated dictionary live in the sidebar
st.sidebar.write("📝 Jobs currently in the dictionary:")
st.sidebar.json(st.session_state.opportunity)


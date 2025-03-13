import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="Sales Metrics Simulator", layout="wide", initial_sidebar_state="expanded")

# Main application
st.title("Sales Metrics Simulator")
st.write("Welcome to the Sales Metrics Simulator.")

# Create a simple form
with st.form("basic_form"):
    st.write("Enter some basic metrics:")
    revenue = st.number_input("Revenue", min_value=0.0, value=1000.0)
    cost = st.number_input("Cost", min_value=0.0, value=500.0)
    submitted = st.form_submit_button("Calculate")

if submitted:
    profit = revenue - cost
    st.success(f"Profit: £{profit:,.2f}")

# Simple sidebar
with st.sidebar:
    st.header("About")
    st.write("This is a simple metrics calculator.")
    
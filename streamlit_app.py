import streamlit as st
import pandas as pd
import datetime

# Set page configuration
st.set_page_config(page_title="Sales Metrics Simulator", layout="wide", initial_sidebar_state="expanded")

# Initialize session state for simulations
if 'simulations' not in st.session_state:
    st.session_state.simulations = {}
    st.session_state.sim_counter = 0

# Main title
st.title("Sales Metrics Simulator")
st.write("Enter your sales metrics to generate an analysis.")

# Create tabs
tab_input, tab_results = st.tabs(["Input Metrics", "View Results"])

# Input tab
with tab_input:
    with st.form("metrics_form"):
        # Simulation name
        sim_name = st.text_input("Simulation Name", value=f"Simulation {st.session_state.sim_counter + 1}")
        
        # Create columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Sales Metrics")
            leads = st.number_input("Number of leads", min_value=0, value=100, key="leads")
            conversion_rate = st.number_input("Conversion rate (%)", min_value=0.0, max_value=100.0, value=20.0, key="conversion_rate") / 100
            deal_size = st.number_input("Average deal size (£)", min_value=0.0, value=1000.0, key="deal_size")
        
        with col2:
            st.markdown("### Cost Metrics")
            cost_per_lead = st.number_input("Cost per lead (£)", min_value=0.0, value=10.0, key="cost_per_lead")
            fixed_costs = st.number_input("Fixed costs (£)", min_value=0.0, value=5000.0, key="fixed_costs")
            commission_rate = st.number_input("Commission rate (%)", min_value=0.0, max_value=100.0, value=10.0, key="commission_rate") / 100
        
        # Submit button
        submitted = st.form_submit_button("Run Simulation")
    
    # Process form submission
    if submitted:
        # Calculate basic metrics
        customers = leads * conversion_rate
        revenue = customers * deal_size
        variable_costs = leads * cost_per_lead
        commission = revenue * commission_rate
        total_costs = fixed_costs + variable_costs + commission
        profit = revenue - total_costs
        roi = (profit / total_costs) * 100 if total_costs > 0 else 0
        
        # Create results dictionary
        results = {
            "inputs": {
                "leads": leads,
                "conversion_rate": conversion_rate,
                "deal_size": deal_size,
                "cost_per_lead": cost_per_lead,
                "fixed_costs": fixed_costs,
                "commission_rate": commission_rate
            },
            "customers": customers,
            "revenue": revenue,
            "variable_costs": variable_costs,
            "commission": commission,
            "total_costs": total_costs,
            "profit": profit,
            "roi": roi
        }
        
        # Save to session state
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sim_id = f"Sim {st.session_state.sim_counter + 1}"
        
        st.session_state.simulations[sim_id] = {
            "name": sim_name,
            "timestamp": timestamp,
            "data": results
        }
        
        st.session_state.sim_counter += 1
        
        # Success message
        st.success(f"Simulation '{sim_name}' completed successfully!")

# Results tab
with tab_results:
    if len(st.session_state.simulations) == 0:
        st.info("No simulations have been run yet. Go to the 'Input Metrics' tab to run a simulation.")
    else:
        # Select a simulation to view
        sim_options = list(st.session_state.simulations.keys())
        selected_sim = st.selectbox(
            "Select a simulation to view",
            options=sim_options,
            format_func=lambda x: f"{x}: {st.session_state.simulations[x]['name']}"
        )
        
        if selected_sim:
            sim = st.session_state.simulations[selected_sim]
            data = sim["data"]
            
            # Display results
            st.header(f"Results for '{sim['name']}'")
            st.write(f"Generated on: {sim['timestamp']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Revenue", f"£{data['revenue']:,.2f}")
                st.metric("Profit", f"£{data['profit']:,.2f}")
                st.metric("ROI", f"{data['roi']:,.2f}%")
            
            with col2:
                st.metric("Customers", f"{data['customers']:,.0f}")
                st.metric("Total Costs", f"£{data['total_costs']:,.2f}")
                st.metric("Conversion Rate", f"{data['inputs']['conversion_rate']:.2%}")

# Sidebar
with st.sidebar:
    st.header("Simulation History")
    
    if len(st.session_state.simulations) == 0:
        st.info("No simulations have been run yet.")
    else:
        for sim_id, sim in st.session_state.simulations.items():
            st.write(f"**{sim_id}**: {sim['name']}")
            st.write(f"*Run at: {sim['timestamp']}*")
            
            # Show key metrics
            st.write(f"Revenue: £{sim['data']['revenue']:,.2f}")
            st.write(f"Profit: £{sim['data']['profit']:,.2f}")
            
            # Add delete button
            if st.button(f"Delete {sim_id}", key=f"delete_{sim_id}"):
                del st.session_state.simulations[sim_id]
                st.success(f"Deleted {sim_id}")
                st.experimental_rerun()
            
            st.write("---")
    
    # Clear all simulations button
    if st.button("Clear All Simulations"):
        st.session_state.simulations = {}
        st.session_state.sim_counter = 0
        st.experimental_rerun()
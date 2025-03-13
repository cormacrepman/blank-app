import streamlit as st
import pandas as pd
import numpy as np
import json
import base64
import datetime

# Set page configuration
st.set_page_config(page_title="Sales Metrics Simulator", layout="wide", initial_sidebar_state="expanded")

# Initialize session state for simulations
if 'simulations' not in st.session_state:
    st.session_state.simulations = {}
    st.session_state.sim_counter = 0

# Utility functions
def get_csv_download_link(df, filename, text):
    """Generate a download link for a CSV file"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def get_json_download_link(data, filename, text):
    """Generate a download link for a JSON file"""
    json_str = json.dumps(data, indent=4)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="{filename}">{text}</a>'
    return href

def calculate_metrics(inputs):
    """Calculate all metrics from input data"""
    # Basic calculations
    leads = inputs.get('leads', 0)
    conversion_rate = inputs.get('conversion_rate', 0)
    deal_size = inputs.get('deal_size', 0)
    cost_per_lead = inputs.get('cost_per_lead', 0)
    fixed_costs = inputs.get('fixed_costs', 0)
    commission_rate = inputs.get('commission_rate', 0)
    churn_rate = inputs.get('churn_rate', 0)
    
    # Sales metrics
    customers = leads * conversion_rate
    revenue = customers * deal_size
    
    # Cost metrics
    variable_costs = leads * cost_per_lead
    commission = revenue * commission_rate
    total_costs = fixed_costs + variable_costs + commission
    
    # Performance metrics
    profit = revenue - total_costs
    roi = (profit / total_costs) * 100 if total_costs > 0 else 0
    profit_margin = (profit / revenue) * 100 if revenue > 0 else 0
    customer_retention = 1 - churn_rate
    
    # Return calculated metrics
    return {
        "inputs": inputs,
        "customers": customers,
        "revenue": revenue,
        "variable_costs": variable_costs,
        "commission": commission,
        "total_costs": total_costs,
        "profit": profit,
        "roi": roi,
        "profit_margin": profit_margin,
        "customer_retention": customer_retention
    }

# Main title
st.title("Sales Metrics Simulator")
st.write("Enter your sales metrics to generate an analysis.")

# Create tabs
tab_input, tab_compare, tab_download = st.tabs(["Run Simulation", "Compare Simulations", "Download Data"])

# Tab 1: Input Form
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
            
            st.markdown("### Marketing Metrics")
            cost_per_lead = st.number_input("Cost per lead (£)", min_value=0.0, value=10.0, key="cost_per_lead")
            marketing_spend = st.number_input("Marketing spend (£)", min_value=0.0, value=3000.0, key="marketing_spend")
            media_spend = st.number_input("Media spend (£)", min_value=0.0, value=2000.0, key="media_spend")
        
        with col2:
            st.markdown("### Offer Metrics")
            churn_rate = st.number_input("Churn rate (%)", min_value=0.0, max_value=100.0, value=15.0, key="churn_rate") / 100
            contract_length = st.number_input("Contract length (months)", min_value=1, value=12, key="contract_length")
            price_of_renewal = st.number_input("Price of renewal (£)", min_value=0.0, value=900.0, key="price_of_renewal")
            
            st.markdown("### Financial Metrics")
            fixed_costs = st.number_input("Fixed costs (£)", min_value=0.0, value=5000.0, key="fixed_costs")
            commission_rate = st.number_input("Commission rate (%)", min_value=0.0, max_value=100.0, value=10.0, key="commission_rate") / 100
            operating_expenses = st.number_input("Operating expenses (£)", min_value=0.0, value=8000.0, key="operating_expenses")
        
        # Submit button
        submitted = st.form_submit_button("Run Simulation")
    
    # Process form submission
    if submitted:
        # Prepare input data
        input_data = {
            "leads": leads,
            "conversion_rate": conversion_rate,
            "deal_size": deal_size,
            "cost_per_lead": cost_per_lead,
            "marketing_spend": marketing_spend,
            "media_spend": media_spend,
            "churn_rate": churn_rate,
            "contract_length": contract_length,
            "price_of_renewal": price_of_renewal,
            "fixed_costs": fixed_costs,
            "commission_rate": commission_rate,
            "operating_expenses": operating_expenses
        }
        
        # Calculate metrics
        results = calculate_metrics(input_data)
        
        # Save to session state
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sim_id = f"Sim {st.session_state.sim_counter + 1}"
        
        if sim_name.strip() == "":
            sim_name = sim_id
        
        st.session_state.simulations[sim_id] = {
            "name": sim_name,
            "timestamp": timestamp,
            "data": results
        }
        
        st.session_state.sim_counter += 1
        
        # Success message
        st.success(f"Simulation '{sim_name}' completed successfully!")
        
        # Display results
        st.header(f"Results for '{sim_name}'")
        
        # Results in tabs
        result_tab1, result_tab2 = st.tabs(["Revenue & Profit", "Customer Metrics"])
        
        with result_tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Revenue", f"£{results['revenue']:,.2f}")
                st.metric("Total Costs", f"£{results['total_costs']:,.2f}")
                st.metric("Profit", f"£{results['profit']:,.2f}")
            with col2:
                st.metric("ROI", f"{results['roi']:,.2f}%")
                st.metric("Profit Margin", f"{results['profit_margin']:,.2f}%")
                st.metric("Variable Costs", f"£{results['variable_costs']:,.2f}")
        
        with result_tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Leads", f"{results['inputs']['leads']:,.0f}")
                st.metric("Conversion Rate", f"{results['inputs']['conversion_rate']:.2%}")
                st.metric("Customers", f"{results['customers']:,.0f}")
            with col2:
                st.metric("Churn Rate", f"{results['inputs']['churn_rate']:.2%}")
                st.metric("Customer Retention", f"{results['customer_retention']:.2%}")
                st.metric("Contract Length", f"{results['inputs']['contract_length']} months")

# Tab 2: Compare Simulations
with tab_compare:
    if len(st.session_state.simulations) == 0:
        st.warning("No simulations have been run. Please run at least one simulation in the 'Run Simulation' tab.")
    else:
        st.subheader("Compare Simulations")
        
        # Select simulations to compare
        sim_options = list(st.session_state.simulations.keys())
        selected_sims = st.multiselect(
            "Select simulations to compare",
            options=sim_options,
            default=sim_options,
            format_func=lambda x: f"{x}: {st.session_state.simulations[x]['name']}"
        )
        
        if selected_sims:
            # Choose metrics to compare
            metric_options = {
                "revenue": "Revenue",
                "profit": "Profit",
                "roi": "ROI",
                "profit_margin": "Profit Margin",
                "customers": "Customers",
                "variable_costs": "Variable Costs",
                "total_costs": "Total Costs",
                "customer_retention": "Customer Retention"
            }
            
            selected_metrics = st.multiselect(
                "Select metrics to compare",
                options=list(metric_options.keys()),
                default=["revenue", "profit", "roi", "customers"],
                format_func=lambda x: metric_options[x]
            )
            
            if selected_metrics:
                # Create comparison dataframe
                comparison_data = []
                
                for sim_id in selected_sims:
                    sim = st.session_state.simulations[sim_id]
                    row = {"Simulation": sim["name"]}
                    
                    for metric in selected_metrics:
                        row[metric_options[metric]] = sim["data"][metric]
                    
                    comparison_data.append(row)
                
                df_comparison = pd.DataFrame(comparison_data)
                
                # Display comparison table
                st.dataframe(df_comparison)
                
                # Input parameter comparison
                st.subheader("Input Parameter Comparison")
                
                # Select parameters to compare
                input_params = list(st.session_state.simulations[selected_sims[0]]['data']['inputs'].keys())
                param_options = {
                    "leads": "Leads",
                    "conversion_rate": "Conversion Rate",
                    "deal_size": "Deal Size",
                    "cost_per_lead": "Cost Per Lead",
                    "marketing_spend": "Marketing Spend",
                    "media_spend": "Media Spend",
                    "churn_rate": "Churn Rate",
                    "contract_length": "Contract Length",
                    "price_of_renewal": "Price of Renewal",
                    "fixed_costs": "Fixed Costs",
                    "commission_rate": "Commission Rate",
                    "operating_expenses": "Operating Expenses"
                }
                
                selected_params = st.multiselect(
                    "Select input parameters to compare",
                    options=input_params,
                    default=[],
                    format_func=lambda x: param_options.get(x, x)
                )
                
                if selected_params:
                    # Create input comparison dataframe
                    input_comparison_data = []
                    
                    for sim_id in selected_sims:
                        sim = st.session_state.simulations[sim_id]
                        row = {"Simulation": sim["name"]}
                        
                        for param in selected_params:
                            # Get parameter value
                            value = sim["data"]["inputs"].get(param, None)
                            row[param_options.get(param, param)] = value
                        
                        input_comparison_data.append(row)
                    
                    df_input_comparison = pd.DataFrame(input_comparison_data)
                    
                    # Display input comparison table
                    st.dataframe(df_input_comparison)

# Tab 3: Download Data
with tab_download:
    if len(st.session_state.simulations) == 0:
        st.warning("No simulations have been run. Please run at least one simulation in the 'Run Simulation' tab.")
    else:
        st.subheader("Download Simulation Data")
        
        # Select simulation to download
        sim_options = list(st.session_state.simulations.keys())
        
        selected_sim = st.selectbox(
            "Select simulation to download",
            options=sim_options,
            format_func=lambda x: f"{x}: {st.session_state.simulations[x]['name']}"
        )
        
        if selected_sim:
            sim = st.session_state.simulations[selected_sim]
            
            st.write(f"### Download options for: {sim['name']}")
            
            # Create dataframes for different aspects of the simulation
            
            # 1. Input parameters
            input_data = sim['data']['inputs']
            df_inputs = pd.DataFrame([input_data])
            
            # 2. Output metrics
            output_data = {k: v for k, v in sim['data'].items() if k != 'inputs'}
            df_outputs = pd.DataFrame([output_data])
            
            # 3. All combined
            combined_data = {**input_data, **output_data}
            df_combined = pd.DataFrame([combined_data])
            
            # Download links
            st.markdown(get_csv_download_link(df_inputs, f"{sim['name']}_inputs.csv", "Download Input Parameters (CSV)"), unsafe_allow_html=True)
            st.markdown(get_csv_download_link(df_outputs, f"{sim['name']}_outputs.csv", "Download Output Metrics (CSV)"), unsafe_allow_html=True)
            st.markdown(get_csv_download_link(df_combined, f"{sim['name']}_combined.csv", "Download All Data (CSV)"), unsafe_allow_html=True)
            st.markdown(get_json_download_link(sim['data'], f"{sim['name']}_full.json", "Download Full Simulation Data (JSON)"), unsafe_allow_html=True)
            
            # Download all simulations
            st.write("### Download All Simulations")
            
            # Create a combined dataframe of all simulations
            all_sims_data = []
            
            for sim_id, sim_data in st.session_state.simulations.items():
                row = {
                    "Simulation ID": sim_id,
                    "Simulation Name": sim_data["name"],
                    "Timestamp": sim_data["timestamp"]
                }
                
                # Add input parameters
                for param, value in sim_data["data"]["inputs"].items():
                    row[f"Input: {param}"] = value
                
                # Add output metrics
                for metric, value in {k: v for k, v in sim_data["data"].items() if k != 'inputs'}.items():
                    row[f"Output: {metric}"] = value
                
                all_sims_data.append(row)
            
            df_all_sims = pd.DataFrame(all_sims_data)
            
            st.markdown(get_csv_download_link(df_all_sims, "all_simulations.csv", "Download All Simulations (CSV)"), unsafe_allow_html=True)
            st.markdown(get_json_download_link(st.session_state.simulations, "all_simulations.json", "Download All Simulations (JSON)"), unsafe_allow_html=True)

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
            st.write(f"ROI: {sim['data']['roi']:,.2f}%")
            
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
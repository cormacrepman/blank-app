import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
import base64

# Initialize session state for storing simulations if it doesn't exist
if 'simulations' not in st.session_state:
    st.session_state.simulations = {}
    st.session_state.sim_counter = 0

# Set page title and configuration
st.set_page_config(page_title="Comprehensive Sales Metrics Simulator", layout="wide")

st.title("Comprehensive Sales Metrics Simulator")
st.write("Enter your sales metrics to generate a comprehensive analysis. You can run multiple simulations to compare results.")

# Create tabs for input form and simulation comparison
tab_input, tab_compare, tab_download = st.tabs(["Run Simulation", "Compare Simulations", "Download Data"])

# Function to calculate metrics based on inputs
def calculate_metrics(inputs):
    # Extract all inputs from the dictionary
    locals().update(inputs)
    
    # Calculate derived metrics
    customer_retention_rate = 1 - churn_rate
    opportunities = leads_generated * lead_conversion_rate
    customers = opportunities * opportunity_conversion_rate
    revenue_generated = customers * average_deal_size
    profit_margin = (revenue_generated - (cogs + operating_expenses)) / revenue_generated if revenue_generated > 0 else 0
    total_cost_leads = leads_generated * cost_per_lead
    total_cost_meetings = meetings_held * cost_per_meeting
    total_sales_team_commission = revenue_generated * sales_commission_rate
    total_marketing_spend = marketing_spend + product_dev_cost
    discounts_given = revenue_generated * discount_rate
    refunds_given = revenue_generated * refund_rate
    seasonality_adjusted_revenue = revenue_generated * (1 + seasonality_adjustment)

    # Calculate profit and other metrics
    gross_profit = revenue_generated - cogs
    operating_profit = gross_profit - operating_expenses
    net_profit = operating_profit - total_sales_team_commission - total_marketing_spend
    break_even_point = total_cost_leads + total_cost_meetings
    roi = (net_profit / total_marketing_spend) * 100 if total_marketing_spend > 0 else 0
    cltv_cac_ratio = avg_customer_lifetime_value / customer_acquisition_cost if customer_acquisition_cost > 0 else 0
    
    # Return all calculated metrics
    return {
        # Input parameters (for reference)
        "inputs": inputs,
        # Derived metrics
        "opportunities": opportunities,
        "customers": customers,
        "revenue_generated": revenue_generated,
        "profit_margin": profit_margin,
        "customer_retention_rate": customer_retention_rate,
        "total_cost_leads": total_cost_leads,
        "total_cost_meetings": total_cost_meetings,
        "total_sales_team_commission": total_sales_team_commission,
        "total_marketing_spend": total_marketing_spend,
        "discounts_given": discounts_given,
        "refunds_given": refunds_given,
        "seasonality_adjusted_revenue": seasonality_adjusted_revenue,
        "gross_profit": gross_profit,
        "operating_profit": operating_profit,
        "net_profit": net_profit,
        "break_even_point": break_even_point,
        "roi": roi,
        "cltv_cac_ratio": cltv_cac_ratio
    }

# Function to get download link for a dataframe
def get_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download {text}</a>'
    return href

# Function to get download link for JSON data
def get_json_download_link(data, filename, text):
    json_str = json.dumps(data, indent=4)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{filename}">Download {text}</a>'
    return href

# Input form tab
with tab_input:
    with st.form("sales_metrics_form"):
        # Optional simulation name
        sim_name = st.text_input("Simulation Name (optional)", value=f"Simulation {st.session_state.sim_counter + 1}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Lead and Conversion Metrics")
            leads_generated = st.number_input("Number of leads generated", min_value=0.0, value=100.0)
            lead_conversion_rate = st.number_input("Lead conversion rate (%)", min_value=0.0, max_value=100.0, value=20.0) / 100
            opportunity_conversion_rate = st.number_input("Opportunity conversion rate (%)", min_value=0.0, max_value=100.0, value=30.0) / 100
            average_deal_size = st.number_input("Average deal size (revenue per deal)", min_value=0.0, value=1000.0)
            cost_per_lead = st.number_input("Cost per lead", min_value=0.0, value=10.0)
            cost_per_meeting = st.number_input("Cost per meeting", min_value=0.0, value=50.0)
            meetings_held = st.number_input("Number of meetings held", min_value=0, value=30)
            follow_ups_per_lead = st.number_input("Number of follow-ups per lead", min_value=0, value=3)
            sales_cycle_length = st.number_input("Sales cycle length (days)", min_value=0, value=30)
        
        with col2:
            st.subheader("Financial & Customer Metrics")
            cogs = st.number_input("Cost of goods sold (COGS)", min_value=0.0, value=5000.0)
            customer_acquisition_cost = st.number_input("Customer acquisition cost (CAC)", min_value=0.0, value=200.0)
            contract_length = st.number_input("Average contract length (months)", min_value=0, value=12)
            avg_customer_lifetime_value = st.number_input("Average customer lifetime value (CLTV)", min_value=0.0, value=5000.0)
            churn_rate = st.number_input("Churn rate (%)", min_value=0.0, max_value=100.0, value=10.0) / 100
            operating_expenses = st.number_input("Total operating expenses", min_value=0.0, value=10000.0)
            sales_team_salary = st.number_input("Total sales team salary", min_value=0.0, value=20000.0)
            sales_commission_rate = st.number_input("Sales commission rate (%)", min_value=0.0, max_value=100.0, value=5.0) / 100
        
        st.subheader("Additional Factors")
        col3, col4 = st.columns(2)
        
        with col3:
            marketing_spend = st.number_input("Total marketing spend", min_value=0.0, value=5000.0)
            product_dev_cost = st.number_input("Product development cost", min_value=0.0, value=10000.0)
        
        with col4:
            discount_rate = st.number_input("Average discount rate (%)", min_value=0.0, max_value=100.0, value=10.0) / 100
            refund_rate = st.number_input("Refund rate (%)", min_value=0.0, max_value=100.0, value=5.0) / 100
            seasonality_adjustment = st.number_input("Seasonality adjustment (% change in sales)", min_value=-100.0, max_value=100.0, value=10.0) / 100
        
        submitted = st.form_submit_button("Run Simulation")

    # Calculate metrics when form is submitted
    if submitted:
        # Collect all inputs into a dictionary
        input_data = {
            "leads_generated": leads_generated,
            "lead_conversion_rate": lead_conversion_rate,
            "opportunity_conversion_rate": opportunity_conversion_rate,
            "average_deal_size": average_deal_size,
            "cost_per_lead": cost_per_lead,
            "cost_per_meeting": cost_per_meeting,
            "meetings_held": meetings_held,
            "follow_ups_per_lead": follow_ups_per_lead,
            "sales_cycle_length": sales_cycle_length,
            "cogs": cogs,
            "customer_acquisition_cost": customer_acquisition_cost,
            "contract_length": contract_length,
            "avg_customer_lifetime_value": avg_customer_lifetime_value,
            "churn_rate": churn_rate,
            "operating_expenses": operating_expenses,
            "sales_team_salary": sales_team_salary,
            "sales_commission_rate": sales_commission_rate,
            "marketing_spend": marketing_spend,
            "product_dev_cost": product_dev_cost,
            "discount_rate": discount_rate,
            "refund_rate": refund_rate,
            "seasonality_adjustment": seasonality_adjustment
        }
        
        # Calculate metrics
        results = calculate_metrics(input_data)
        
        # Store simulation with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sim_id = f"Sim {st.session_state.sim_counter + 1}"
        
        if sim_name.strip() == "":
            sim_name = sim_id
        
        st.session_state.simulations[sim_id] = {
            "name": sim_name,
            "timestamp": timestamp,
            "data": results
        }
        
        st.session_state.sim_counter += 1
        
        # Display results for this simulation
        st.success(f"Simulation '{sim_name}' completed and saved!")
        
        # Display results in an organized way
        st.header(f"Results for {sim_name}")
        
        # Results in tabs
        result_tab1, result_tab2, result_tab3 = st.tabs(["Revenue & Profit", "Customer Metrics", "Cost Analysis"])
        
        with result_tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Revenue Generated", f"£{results['revenue_generated']:,.2f}")
                st.metric("Gross Profit", f"£{results['gross_profit']:,.2f}")
                st.metric("Operating Profit", f"£{results['operating_profit']:,.2f}")
            with col2:
                st.metric("Net Profit", f"£{results['net_profit']:,.2f}")
                st.metric("Profit Margin", f"{results['profit_margin']:.2%}")
                st.metric("Seasonality Adjusted Revenue", f"£{results['seasonality_adjusted_revenue']:,.2f}")
        
        with result_tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Leads Generated", f"{results['inputs']['leads_generated']:,.0f}")
                st.metric("Opportunities", f"{results['opportunities']:,.0f}")
                st.metric("Customers", f"{results['customers']:,.0f}")
            with col2:
                st.metric("Customer Acquisition Cost (CAC)", f"£{results['inputs']['customer_acquisition_cost']:,.2f}")
                st.metric("Customer Lifetime Value (CLTV)", f"£{results['inputs']['avg_customer_lifetime_value']:,.2f}")
                st.metric("CLTV to CAC Ratio", f"{results['cltv_cac_ratio']:.2f}x" if results['cltv_cac_ratio'] > 0 else "N/A")
                st.metric("Customer Retention Rate", f"{results['customer_retention_rate']:.2%}")
        
        with result_tab3:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Break-even Point", f"£{results['break_even_point']:,.2f}")
                st.metric("ROI for Marketing", f"{results['roi']:.2f}%")
                st.metric("Total Cost of Leads", f"£{results['total_cost_leads']:,.2f}")
                st.metric("Total Cost of Meetings", f"£{results['total_cost_meetings']:,.2f}")
            with col2:
                st.metric("Total Sales Commission", f"£{results['total_sales_team_commission']:,.2f}")
                st.metric("Total Marketing Spend", f"£{results['total_marketing_spend']:,.2f}")
                st.metric("Discounts Given", f"£{results['discounts_given']:,.2f}")
                st.metric("Refunds Given", f"£{results['refunds_given']:,.2f}")
        
        # Visualizations
        st.subheader("Key Metrics Visualization")
        
        # Revenue breakdown
        revenue_data = {
            'Category': ['Gross Revenue', 'After Discounts', 'After Refunds', 'Seasonality Adjusted'],
            'Amount': [
                results['revenue_generated'], 
                results['revenue_generated'] - results['discounts_given'],
                results['revenue_generated'] - results['discounts_given'] - results['refunds_given'],
                results['seasonality_adjusted_revenue']
            ]
        }
        
        df_revenue = pd.DataFrame(revenue_data)
        fig_revenue = px.bar(df_revenue, x='Category', y='Amount', title='Revenue Breakdown')
        st.plotly_chart(fig_revenue)
        
        # Profit waterfall
        profit_data = {
            'Stage': ['Revenue', 'COGS', 'Gross Profit', 'Operating Expenses', 'Commissions', 'Marketing', 'Net Profit'],
            'Value': [
                results['revenue_generated'], 
                -results['inputs']['cogs'], 
                results['gross_profit'], 
                -results['inputs']['operating_expenses'], 
                -results['total_sales_team_commission'], 
                -results['total_marketing_spend'], 
                results['net_profit']
            ],
            'Type': ['Revenue', 'Cost', 'Profit', 'Cost', 'Cost', 'Cost', 'Profit']
        }
        
        df_profit = pd.DataFrame(profit_data)
        fig_profit = px.bar(df_profit, x='Stage', y='Value', color='Type', 
                            title='Profit Waterfall', 
                            color_discrete_map={'Revenue': 'green', 'Cost': 'red', 'Profit': 'blue'})
        st.plotly_chart(fig_profit)

# Comparison tab
with tab_compare:
    if len(st.session_state.simulations) == 0:
        st.warning("No simulations have been run. Please run at least one simulation in the 'Run Simulation' tab.")
    else:
        st.subheader("Compare Simulations")
        
        # Select simulations to compare
        sim_options = list(st.session_state.simulations.keys())
        sim_names = [st.session_state.simulations[sim]['name'] for sim in sim_options]
        
        selected_sims = st.multiselect(
            "Select simulations to compare",
            options=sim_options,
            default=sim_options,
            format_func=lambda x: f"{x}: {st.session_state.simulations[x]['name']}"
        )
        
        if selected_sims:
            # Choose metrics to compare
            metric_options = {
                "revenue_generated": "Revenue Generated",
                "gross_profit": "Gross Profit",
                "operating_profit": "Operating Profit",
                "net_profit": "Net Profit",
                "profit_margin": "Profit Margin",
                "roi": "ROI",
                "opportunities": "Opportunities",
                "customers": "Customers",
                "cltv_cac_ratio": "CLTV/CAC Ratio",
                "break_even_point": "Break-even Point",
                "total_cost_leads": "Total Cost of Leads",
                "total_cost_meetings": "Total Cost of Meetings",
                "total_sales_team_commission": "Total Sales Commission",
                "total_marketing_spend": "Total Marketing Spend",
                "seasonality_adjusted_revenue": "Seasonality Adjusted Revenue"
            }
            
            selected_metrics = st.multiselect(
                "Select metrics to compare",
                options=list(metric_options.keys()),
                default=["revenue_generated", "net_profit", "roi", "customers"],
                format_func=lambda x: metric_options[x]
            )
            
            if selected_metrics:
                # Create comparison dataframe
                comparison_data = []
                
                for sim_id in selected_sims:
                    sim = st.session_state.simulations[sim_id]
                    row = {"Simulation": sim["name"]}
                    
                    for metric in selected_metrics:
                        if metric == "profit_margin" or metric == "cltv_cac_ratio":
                            # Format as percentage
                            row[metric_options[metric]] = sim["data"][metric]
                        else:
                            row[metric_options[metric]] = sim["data"][metric]
                    
                    comparison_data.append(row)
                
                df_comparison = pd.DataFrame(comparison_data)
                
                # Display comparison table
                st.dataframe(df_comparison)
                
                # Visualize comparisons
                st.subheader("Comparison Charts")
                
                for metric in selected_metrics:
                    # Create a bar chart for each selected metric
                    metric_name = metric_options[metric]
                    
                    chart_data = {
                        'Simulation': [st.session_state.simulations[sim_id]['name'] for sim_id in selected_sims],
                        'Value': [st.session_state.simulations[sim_id]['data'][metric] for sim_id in selected_sims]
                    }
                    
                    df_chart = pd.DataFrame(chart_data)
                    
                    if metric in ["profit_margin", "cltv_cac_ratio"]:
                        # Format as percentage
                        fig = px.bar(df_chart, x='Simulation', y='Value', title=f"Comparison of {metric_name}",
                                    labels={"Value": f"{metric_name} (%)"})
                        # Convert to percentage for display
                        fig.update_layout(yaxis_tickformat='.2%')
                    else:
                        fig = px.bar(df_chart, x='Simulation', y='Value', title=f"Comparison of {metric_name}")
                        if metric in ["revenue_generated", "gross_profit", "operating_profit", "net_profit", 
                                    "break_even_point", "total_cost_leads", "total_cost_meetings", 
                                    "total_sales_team_commission", "total_marketing_spend", 
                                    "seasonality_adjusted_revenue"]:
                            # Add pound symbol
                            fig.update_layout(yaxis_title=f"{metric_name} (£)")
                    
                    st.plotly_chart(fig)
                
                # Input parameter comparison
                st.subheader("Input Parameter Comparison")
                
                # Select parameters to compare
                input_params = list(st.session_state.simulations[selected_sims[0]]['data']['inputs'].keys())
                param_options = {
                    "leads_generated": "Leads Generated",
                    "lead_conversion_rate": "Lead Conversion Rate",
                    "opportunity_conversion_rate": "Opportunity Conversion Rate",
                    "average_deal_size": "Average Deal Size",
                    "cost_per_lead": "Cost Per Lead",
                    "cost_per_meeting": "Cost Per Meeting",
                    "meetings_held": "Meetings Held",
                    "cogs": "COGS",
                    "customer_acquisition_cost": "CAC",
                    "avg_customer_lifetime_value": "CLTV",
                    "churn_rate": "Churn Rate",
                    "operating_expenses": "Operating Expenses",
                    "sales_commission_rate": "Sales Commission Rate",
                    "marketing_spend": "Marketing Spend",
                    "product_dev_cost": "Product Development Cost",
                    "discount_rate": "Discount Rate",
                    "refund_rate": "Refund Rate",
                    "seasonality_adjustment": "Seasonality Adjustment"
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
                            if param in ["lead_conversion_rate", "opportunity_conversion_rate", "churn_rate", 
                                        "sales_commission_rate", "discount_rate", "refund_rate", "seasonality_adjustment"]:
                                # Format as percentage
                                row[param_options.get(param, param)] = sim["data"]["inputs"][param]
                            else:
                                row[param_options.get(param, param)] = sim["data"]["inputs"][param]
                        
                        input_comparison_data.append(row)
                    
                    df_input_comparison = pd.DataFrame(input_comparison_data)
                    
                    # Display input comparison table
                    st.dataframe(df_input_comparison)
                    
                    # Visualize input comparisons
                    for param in selected_params:
                        # Create a bar chart for each selected parameter
                        param_name = param_options.get(param, param)
                        
                        chart_data = {
                            'Simulation': [st.session_state.simulations[sim_id]['name'] for sim_id in selected_sims],
                            'Value': [st.session_state.simulations[sim_id]['data']['inputs'][param] for sim_id in selected_sims]
                        }
                        
                        df_chart = pd.DataFrame(chart_data)
                        
                        if param in ["lead_conversion_rate", "opportunity_conversion_rate", "churn_rate", 
                                  "sales_commission_rate", "discount_rate", "refund_rate", "seasonality_adjustment"]:
                            # Format as percentage
                            fig = px.bar(df_chart, x='Simulation', y='Value', title=f"Comparison of {param_name}",
                                        labels={"Value": f"{param_name} (%)"})
                            # Convert to percentage for display
                            fig.update_layout(yaxis_tickformat='.2%')
                        else:
                            fig = px.bar(df_chart, x='Simulation', y='Value', title=f"Comparison of {param_name}")
                        
                        st.plotly_chart(fig)

# Download data tab
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
            st.markdown(get_download_link(df_inputs, f"{sim['name']}_inputs.csv", "Input Parameters (CSV)"), unsafe_allow_html=True)
            st.markdown(get_download_link(df_outputs, f"{sim['name']}_outputs.csv", "Output Metrics (CSV)"), unsafe_allow_html=True)
            st.markdown(get_download_link(df_combined, f"{sim['name']}_combined.csv", "All Data (CSV)"), unsafe_allow_html=True)
            st.markdown(get_json_download_link(sim['data'], f"{sim['name']}_full.json", "Full Simulation Data (JSON)"), unsafe_allow_html=True)
            
            # Option to download all simulations
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
            
            st.markdown(get_download_link(df_all_sims, "all_simulations.csv", "All Simulations (CSV)"), unsafe_allow_html=True)
            st.markdown(get_json_download_link(st.session_state.simulations, "all_simulations.json", "All Simulations (JSON)"), unsafe_allow_html=True)

# Add a sidebar with information
with st.sidebar:
    st.header("Simulation History")
    
    if len(st.session_state.simulations) == 0:
        st.info("No simulations have been run yet.")
    else:
        for sim_id, sim in st.session_state.simulations.items():
            st.write(f"**{sim_id}**: {sim['name']}")
            st.write(f"*Run at: {sim['timestamp']}*")
            
            # Show key metrics
            st.write(f"Revenue: £{sim['data']['revenue_generated']:,.2f}")
            st.write(f"Net Profit: £{sim['data']['net_profit']:,.2f}")
            st.write(f"ROI: {sim['data']['roi']:.2f}%")
            st.write("---")
    
    # Clear all simulations button
    if st.button("Clear All Simulations"):
        st.session_state.simulations = {}
        st.session_state.sim_counter = 0
        st.experimental_rerun()
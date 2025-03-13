import streamlit as st
import pandas as pd
import numpy as np
import json
import base64
import datetime
import io

# Set page configuration
st.set_page_config(page_title="Sales Metrics Simulator", layout="wide", initial_sidebar_state="expanded")

# Try to import optional dependencies with fallbacks
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

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

def get_pdf_download_link(pdf_bytes, filename, text):
    """Generate a download link for a PDF file"""
    if pdf_bytes is None:
        return ""
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}" target="_blank">{text}</a>'
    return href

def create_pdf_report(sim_data, sim_name):
    """Create a PDF report for a simulation"""
    if not REPORTLAB_AVAILABLE:
        return None
    
    # Create buffer for PDF
    buffer = io.BytesIO()
    
    # Create the PDF object
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Set styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Add title
    elements.append(Paragraph(f"Simulation Report: {sim_name}", title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Add timestamp
    elements.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Add summary section
    elements.append(Paragraph("Summary Results", subtitle_style))
    
    # Create summary table
    summary_data = [
        ["Metric", "Value"],
        ["Revenue", f"£{sim_data['revenue']:,.2f}"],
        ["Net Profit", f"£{sim_data['net_profit']:,.2f}"],
        ["ROI", f"{sim_data['roi']:.2f}%"],
        ["Customers", f"{sim_data['customers']:.0f}"],
        ["Customer Lifetime Value", f"£{sim_data['customer_lifetime_value']:,.2f}"]
    ]
    
    # Create the table
    summary_table = Table(summary_data, colWidths=[2.5*inch, 2.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.25*inch))
    
    # Build the PDF
    doc.build(elements)
    
    # Get the value of the PDF
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

def calculate_metrics(inputs):
    """Calculate all metrics from input data"""
    # Extract inputs by category
    
    # Sales metrics
    leads = inputs.get('leads', 0)
    lead_booking_rate = inputs.get('lead_booking_rate', 0)  # Renamed
    meeting_conversion_rate = inputs.get('meeting_conversion_rate', 0)  # Renamed
    average_deal_size = inputs.get('average_deal_size', 0)
    sales_cycle_length = inputs.get('sales_cycle_length', 0)
    sales_commission_rate = inputs.get('sales_commission_rate', 0)
    number_of_sdrs = inputs.get('number_of_sdrs', 0)
    time_to_sell_days = inputs.get('time_to_sell_days', 0)
    
    # Marketing metrics
    cost_per_lead = inputs.get('cost_per_lead', 0)
    cost_per_booked_meeting = inputs.get('cost_per_booked_meeting', 0)  # New
    marketing_spend = inputs.get('marketing_spend', 0)
    media_spend = inputs.get('media_spend', 0)
    total_addressable_market = inputs.get('total_addressable_market', 0)  # Moved
    funnel_conversion_rate = inputs.get('funnel_conversion_rate', 0)
    click_through_rate = inputs.get('click_through_rate', 0)
    organic_views = inputs.get('organic_views', 0)
    cost_per_thousand_impressions = inputs.get('cost_per_thousand_impressions', 0)
    
    # Offer metrics
    price_of_offer = inputs.get('price_of_offer', 0)  # Moved
    churn_rate = inputs.get('churn_rate', 0)
    contract_length = inputs.get('contract_length', 0)
    price_of_renewal = inputs.get('price_of_renewal', 0)
    rate_of_renewals = inputs.get('rate_of_renewals', 0)
    discount_rate = inputs.get('discount_rate', 0)
    refund_rate = inputs.get('refund_rate', 0)
    customer_acquisition_cost = inputs.get('customer_acquisition_cost', 0)
    
    # Operations metrics
    fixed_costs = inputs.get('fixed_costs', 0)
    cogs = inputs.get('cogs', 0)
    operating_expenses = inputs.get('operating_expenses', 0)
    cost_to_fulfil = inputs.get('cost_to_fulfil', 0)
    
    # Cash metrics
    initial_number_of_customers = inputs.get('initial_number_of_customers', 0)
    cash_in_bank = inputs.get('cash_in_bank', 0)
    
    # Calculate derived metrics
    
    # Sales and customer metrics
    booked_meetings = leads * lead_booking_rate  # Renamed
    customers = booked_meetings * meeting_conversion_rate  # Renamed
    revenue = customers * average_deal_size
    
    # Include Cost per Booked Meeting in calculations
    total_meeting_costs = booked_meetings * cost_per_booked_meeting  # New calculation
    
    # Cost metrics
    variable_costs = leads * cost_per_lead
    commission = revenue * sales_commission_rate
    total_marketing_costs = marketing_spend + media_spend
    total_variable_costs = variable_costs + commission + total_meeting_costs  # Updated to include meeting costs
    total_costs = fixed_costs + total_variable_costs + cogs + operating_expenses
    
    # Performance metrics
    gross_profit = revenue - cogs
    operating_profit = gross_profit - operating_expenses
    net_profit = operating_profit - commission - total_marketing_costs
    profit_margin = (net_profit / revenue) * 100 if revenue > 0 else 0
    roi = (net_profit / total_costs) * 100 if total_costs > 0 else 0
    customer_retention = 1 - churn_rate
    
    # Lifetime value metrics
    customer_lifetime = 1 / churn_rate if churn_rate > 0 else 0
    customer_lifetime_value = (average_deal_size * profit_margin / 100) * customer_lifetime
    cac_ratio = customer_lifetime_value / customer_acquisition_cost if customer_acquisition_cost > 0 else 0
    
    # Special calculations
    discounts_given = revenue * discount_rate
    refunds_given = revenue * refund_rate
    seasonality_adjusted_revenue = revenue  # Placeholder for more complex calculation
    
    # Return all calculated metrics
    return {
        "inputs": inputs,
        "booked_meetings": booked_meetings,
        "customers": customers,
        "revenue": revenue,
        "variable_costs": variable_costs,
        "commission": commission,
        "total_marketing_costs": total_marketing_costs,
        "total_variable_costs": total_variable_costs,
        "total_costs": total_costs,
        "gross_profit": gross_profit,
        "operating_profit": operating_profit,
        "net_profit": net_profit,
        "profit_margin": profit_margin,
        "roi": roi,
        "customer_retention": customer_retention,
        "customer_lifetime": customer_lifetime,
        "customer_lifetime_value": customer_lifetime_value,
        "cac_ratio": cac_ratio,
        "discounts_given": discounts_given,
        "refunds_given": refunds_given,
        "seasonality_adjusted_revenue": seasonality_adjusted_revenue,
        "total_meeting_costs": total_meeting_costs  # Add new calculated metric
    }

# Main title
st.title("Comprehensive Sales Metrics Simulator")
st.write("Enter your sales metrics to generate a comprehensive analysis.")

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
            lead_booking_rate = st.number_input("Lead booking rate (%)", min_value=0.0, max_value=100.0, value=20.0, key="lead_booking_rate") / 100
            meeting_conversion_rate = st.number_input("Meeting conversion rate (%)", min_value=0.0, max_value=100.0, value=30.0, key="meeting_conversion_rate") / 100
            average_deal_size = st.number_input("Average deal size (£)", min_value=0.0, value=1000.0, key="average_deal_size")
            sales_cycle_length = st.number_input("Sales cycle length (days)", min_value=0, value=30, key="sales_cycle_length")
            number_of_sdrs = st.number_input("Number of SDRs", min_value=0, value=2, key="number_of_sdrs")
            time_to_sell_days = st.number_input("Time to sell (days)", min_value=0, value=45, key="time_to_sell_days")
            sales_commission_rate = st.number_input("Sales commission rate (%)", min_value=0.0, max_value=100.0, value=5.0, key="sales_commission_rate") / 100
            
            st.markdown("### Marketing Metrics")
            cost_per_lead = st.number_input("Cost per lead (£)", min_value=0.0, value=10.0, key="cost_per_lead")
            cost_per_booked_meeting = st.number_input("Cost per booked meeting (£)", min_value=0.0, value=50.0, key="cost_per_booked_meeting")
            marketing_spend = st.number_input("Marketing spend (£)", min_value=0.0, value=5000.0, key="marketing_spend")
            media_spend = st.number_input("Media spend (£)", min_value=0.0, value=3000.0, key="media_spend")
            total_addressable_market = st.number_input("Total addressable market", min_value=0, value=100000, key="total_addressable_market")
            funnel_conversion_rate = st.number_input("Funnel conversion rate (%)", min_value=0.0, max_value=100.0, value=15.0, key="funnel_conversion_rate") / 100
            click_through_rate = st.number_input("Click through rate (%)", min_value=0.0, max_value=100.0, value=2.5, key="click_through_rate") / 100
            organic_views = st.number_input("Organic views per month", min_value=0, value=5000, key="organic_views")
            cost_per_thousand_impressions = st.number_input("Cost per thousand impressions (£)", min_value=0.0, value=25.0, key="cost_per_thousand_impressions")
        
        with col2:
            st.markdown("### Offer Metrics")
            price_of_offer = st.number_input("Price of offer (£)", min_value=0.0, value=500.0, key="price_of_offer")
            churn_rate = st.number_input("Churn rate (%)", min_value=0.0, max_value=100.0, value=10.0, key="churn_rate") / 100
            contract_length = st.number_input("Contract length (months)", min_value=1, value=12, key="contract_length")
            price_of_renewal = st.number_input("Price of renewal (£)", min_value=0.0, value=450.0, key="price_of_renewal")
            rate_of_renewals = st.number_input("Rate of renewals (%)", min_value=0.0, max_value=100.0, value=70.0, key="rate_of_renewals") / 100
            discount_rate = st.number_input("Discount rate (%)", min_value=0.0, max_value=100.0, value=10.0, key="discount_rate") / 100
            refund_rate = st.number_input("Refund rate (%)", min_value=0.0, max_value=100.0, value=5.0, key="refund_rate") / 100
            customer_acquisition_cost = st.number_input("Customer acquisition cost (£)", min_value=0.0, value=200.0, key="customer_acquisition_cost")
            
            st.markdown("### Operations Metrics")
            cogs = st.number_input("Cost of goods sold (£)", min_value=0.0, value=5000.0, key="cogs")
            operating_expenses = st.number_input("Operating expenses (£)", min_value=0.0, value=10000.0, key="operating_expenses")
            fixed_costs = st.number_input("Fixed costs per month (£)", min_value=0.0, value=15000.0, key="fixed_costs")
            cost_to_fulfil = st.number_input("Cost to fulfil (£)", min_value=0.0, value=200.0, key="cost_to_fulfil")
            
            st.markdown("### Cash Metrics")
            initial_number_of_customers = st.number_input("Initial number of customers", min_value=0, value=100, key="initial_number_of_customers")
            cash_in_bank = st.number_input("Cash in the bank (£)", min_value=0.0, value=50000.0, key="cash_in_bank")
        
        # Submit button
        submitted = st.form_submit_button("Run Simulation")
    
    # Process form submission
    if submitted:
        # Prepare input data
        input_data = {
            # Sales Metrics
            "leads": leads,
            "lead_booking_rate": lead_booking_rate,
            "meeting_conversion_rate": meeting_conversion_rate,
            "average_deal_size": average_deal_size,
            "sales_cycle_length": sales_cycle_length,
            "number_of_sdrs": number_of_sdrs,
            "time_to_sell_days": time_to_sell_days,
            "sales_commission_rate": sales_commission_rate,
            
            # Marketing Metrics
            "cost_per_lead": cost_per_lead,
            "cost_per_booked_meeting": cost_per_booked_meeting,
            "marketing_spend": marketing_spend,
            "media_spend": media_spend,
            "total_addressable_market": total_addressable_market,
            "funnel_conversion_rate": funnel_conversion_rate,
            "click_through_rate": click_through_rate,
            "organic_views": organic_views,
            "cost_per_thousand_impressions": cost_per_thousand_impressions,
            
            # Offer Metrics
            "price_of_offer": price_of_offer,
            "churn_rate": churn_rate,
            "contract_length": contract_length,
            "price_of_renewal": price_of_renewal,
            "rate_of_renewals": rate_of_renewals,
            "discount_rate": discount_rate,
            "refund_rate": refund_rate,
            "customer_acquisition_cost": customer_acquisition_cost,
            
            # Operations Metrics
            "cogs": cogs,
            "operating_expenses": operating_expenses,
            "fixed_costs": fixed_costs,
            "cost_to_fulfil": cost_to_fulfil,
            
            # Cash Metrics
            "initial_number_of_customers": initial_number_of_customers,
            "cash_in_bank": cash_in_bank
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
        result_tab1, result_tab2, result_tab3 = st.tabs(["Revenue & Profit", "Customer Metrics", "Cost Analysis"])
        
        with result_tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Revenue", f"£{results['revenue']:,.2f}")
                st.metric("Gross Profit", f"£{results['gross_profit']:,.2f}")
                st.metric("Operating Profit", f"£{results['operating_profit']:,.2f}")
            with col2:
                st.metric("Net Profit", f"£{results['net_profit']:,.2f}")
                st.metric("Profit Margin", f"{results['profit_margin']:.2f}%")
                st.metric("ROI", f"{results['roi']:,.2f}%")
            
            # Revenue breakdown visualization
            st.subheader("Revenue Breakdown")
            revenue_data = pd.DataFrame({
                'Category': ['Revenue', 'Discounts', 'Refunds', 'Net Revenue'],
                'Amount': [
                    results['revenue'],
                    -results['discounts_given'],
                    -results['refunds_given'],
                    results['revenue'] - results['discounts_given'] - results['refunds_given']
                ]
            })
            st.bar_chart(revenue_data.set_index('Category'))
        
        with result_tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Leads", f"{results['inputs']['leads']:,.0f}")
                st.metric("Booked Meetings", f"{results['booked_meetings']:,.0f}")
                st.metric("Customers", f"{results['customers']:,.0f}")
            with col2:
                st.metric("Customer Acquisition Cost", f"£{results['inputs']['customer_acquisition_cost']:,.2f}")
                st.metric("Customer Lifetime Value", f"£{results['customer_lifetime_value']:,.2f}")
                st.metric("CLTV/CAC Ratio", f"{results['cac_ratio']:.2f}x")
                st.metric("Customer Retention", f"{results['customer_retention']:.2%}")
        
        with result_tab3:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Costs", f"£{results['total_costs']:,.2f}")
                st.metric("Fixed Costs", f"£{results['inputs']['fixed_costs']:,.2f}")
                st.metric("Variable Costs", f"£{results['total_variable_costs']:,.2f}")
            with col2:
                st.metric("Marketing Costs", f"£{results['total_marketing_costs']:,.2f}")
                st.metric("COGS", f"£{results['inputs']['cogs']:,.2f}")
                st.metric("Commission", f"£{results['commission']:,.2f}")
                st.metric("Meeting Costs", f"£{results['total_meeting_costs']:,.2f}")
            
            # Cost breakdown visualization
            st.subheader("Cost Breakdown")
            cost_data = pd.DataFrame({
                'Category': ['Fixed Costs', 'Marketing', 'COGS', 'Commission', 'Meeting Costs', 'Other Variable'],
                'Amount': [
                    results['inputs']['fixed_costs'],
                    results['total_marketing_costs'],
                    results['inputs']['cogs'],
                    results['commission'],
                    results['total_meeting_costs'],
                    results['total_variable_costs'] - results['commission'] - results['total_meeting_costs']
                ]
            })
            st.bar_chart(cost_data.set_index('Category'))

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
                "gross_profit": "Gross Profit",
                "operating_profit": "Operating Profit",
                "net_profit": "Net Profit",
                "profit_margin": "Profit Margin",
                "roi": "ROI",
                "booked_meetings": "Booked Meetings",
                "customers": "Customers",
                "customer_lifetime_value": "Customer Lifetime Value",
                "cac_ratio": "CLTV/CAC Ratio",
                "total_costs": "Total Costs",
                "total_marketing_costs": "Total Marketing Costs",
                "total_meeting_costs": "Total Meeting Costs"
            }
            
            selected_metrics = st.multiselect(
                "Select metrics to compare",
                options=list(metric_options.keys()),
                default=["revenue", "net_profit", "roi", "customers"],
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
                
                # Visualization of selected metrics
                st.subheader("Comparison Chart")
                chart_data = pd.DataFrame({
                    sim["name"]: [sim["data"][metric] for metric in selected_metrics]
                    for sim_id, sim in st.session_state.simulations.items() if sim_id in selected_sims
                }, index=[metric_options[metric] for metric in selected_metrics])
                
                st.bar_chart(chart_data.T)
                
                # Input parameter comparison
                st.subheader("Input Parameter Comparison")
                
                # Define parameter categories
                param_categories = {
                    "Sales": ["leads", "lead_booking_rate", "meeting_conversion_rate", "average_deal_size", 
                             "sales_cycle_length", "number_of_sdrs", "time_to_sell_days", 
                             "sales_commission_rate"],
                    "Marketing": ["cost_per_lead", "cost_per_booked_meeting", "marketing_spend", "media_spend", 
                                 "total_addressable_market", "funnel_conversion_rate", 
                                 "click_through_rate", "organic_views", "cost_per_thousand_impressions"],
                    "Offer": ["price_of_offer", "churn_rate", "contract_length", "price_of_renewal", "rate_of_renewals", 
                             "discount_rate", "refund_rate", "customer_acquisition_cost"],
                    "Operations": ["cogs", "operating_expenses", "fixed_costs", "cost_to_fulfil"],
                    "Cash": ["initial_number_of_customers", "cash_in_bank"]
                }
                
                # Let user select a category
                selected_category = st.selectbox(
                    "Select parameter category",
                    options=list(param_categories.keys())
                )
                
                if selected_category:
                    # Get parameters for this category
                    category_params = param_categories[selected_category]
                    
                    # Create parameter comparison dataframe
                    param_comparison_data = []
                    
                    for sim_id in selected_sims:
                        sim = st.session_state.simulations[sim_id]
                        row = {"Simulation": sim["name"]}
                        
                        for param in category_params:
                            # Get parameter value
                            value = sim["data"]["inputs"].get(param, None)
                            row[param] = value
                        
                        param_comparison_data.append(row)
                    
                    df_param_comparison = pd.DataFrame(param_comparison_data)
                    
                    # Display parameter comparison table
                    st.dataframe(df_param_comparison)

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
        
        # Create tabs for different download formats
        download_tabs = st.tabs(["CSV/JSON", "PDF Report"])
        
        with download_tabs[0]:
            if selected_sim:  # Check if selected_sim exists
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
                
                # CSV and JSON downloads
                st.markdown(get_csv_download_link(df_inputs, f"{sim['name']}_inputs.csv", "Download Input Parameters (CSV)"), unsafe_allow_html=True)
                st.markdown(get_csv_download_link(df_outputs, f"{sim['name']}_outputs.csv", "Download Output Metrics (CSV)"), unsafe_allow_html=True)
                st.markdown(get_csv_download_link(df_combined, f"{sim['name']}_combined.csv", "Download All Data (CSV)"), unsafe_allow_html=True)
                st.markdown(get_json_download_link(sim['data'], f"{sim['name']}_full.json", "Download Full Simulation Data (JSON)"), unsafe_allow_html=True)
            
            # Show all simulations download (outside the if statement since this doesn't depend on selected_sim)
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
            
            st.markdown(get_csv_download_link(df_all_sims), "all_simulations.csv",
            st.markdown(get_csv_download_link(df_all_sims), "all_simulations.csv", "Download All Simulations (CSV)"), unsafe_allow_html=True)
            st.markdown(get_json_download_link(st.session_state.simulations, "all_simulations.json", "Download All Simulations (JSON)"), unsafe_allow_html=True)
        
        with download_tabs[1]:
            # PDF Report
            if REPORTLAB_AVAILABLE and selected_sim:  # Check both REPORTLAB_AVAILABLE and selected_sim
                sim = st.session_state.simulations[selected_sim]
                st.write("Generate a comprehensive PDF report of this simulation.")
                
                # Generate PDF
                pdf_bytes = create_pdf_report(sim['data'], sim['name'])
                
                # Download button
                st.markdown(get_pdf_download_link(pdf_bytes, f"{sim['name']}_report.pdf", "Download PDF Report"), unsafe_allow_html=True)
                
                # Preview button
                if st.button("Preview PDF in Browser"):
                    # Convert PDF to base64 string
                    b64 = base64.b64encode(pdf_bytes).decode()
                    # Display PDF in an iframe
                    pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="700" height="1000" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
            elif not REPORTLAB_AVAILABLE:
                st.warning("PDF report generation requires ReportLab. Install with: pip install reportlab")
                st.code("pip install reportlab", language="bash")
            elif not selected_sim:
                st.info("Please select a simulation from the dropdown above to generate a PDF report.")

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
            st.write(f"Net Profit: £{sim['data']['net_profit']:,.2f}")
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
        
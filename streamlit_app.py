import streamlit as st
import pandas as pd
import json
from datetime import datetime
import base64

# Try to import plotly, but provide fallbacks if it's not available
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.error("Plotly package is not installed. Install with: pip install plotly")

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
    # Calculate derived metrics using dictionary access
    customer_retention_rate = 1 - inputs.get('churn_rate', 0)
    opportunities = inputs.get('leads_generated', 0) * inputs.get('lead_conversion_rate', 0)
    customers = opportunities * inputs.get('opportunity_conversion_rate', 0)
    revenue_generated = customers * inputs.get('average_deal_size', 0)
    profit_margin = (revenue_generated - (inputs.get('cogs', 0) + inputs.get('operating_expenses', 0))) / revenue_generated if revenue_generated > 0 else 0
    total_cost_leads = inputs.get('leads_generated', 0) * inputs.get('cost_per_lead', 0)
    total_cost_meetings = inputs.get('meetings_held', 0) * inputs.get('cost_per_meeting', 0)
    total_sales_team_commission = revenue_generated * inputs.get('sales_commission_rate', 0)
    total_marketing_spend = inputs.get('marketing_spend', 0) + inputs.get('product_dev_cost', 0)
    discounts_given = revenue_generated * inputs.get('discount_rate', 0)
    refunds_given = revenue_generated * inputs.get('refund_rate', 0)
    seasonality_adjusted_revenue = revenue_generated * (1 + inputs.get('seasonality_adjustment', 0))

    # Calculate profit and other metrics
    gross_profit = revenue_generated - inputs.get('cogs', 0)
    operating_profit = gross_profit - inputs.get('operating_expenses', 0)
    net_profit = operating_profit - total_sales_team_commission - total_marketing_spend
    break_even_point = total_cost_leads + total_cost_meetings
    roi = (net_profit / total_marketing_spend) * 100 if total_marketing_spend > 0 else 0
    cltv_cac_ratio = inputs.get('avg_customer_lifetime_value', 0) / inputs.get('customer_acquisition_cost', 0) if inputs.get('customer_acquisition_cost', 0) > 0 else 0
    
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
        
        # Create two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Sales Metrics")
            average_deal_size = st.number_input("Average deal size (revenue per deal)", min_value=0.0, value=1000.0, key="average_deal_size")
            leads_generated = st.number_input("Number of leads generated", min_value=0.0, value=100.0, key="leads_generated")
            lead_conversion_rate = st.number_input("Lead conversion rate (%)", min_value=0.0, max_value=100.0, value=20.0, key="lead_conversion_rate") / 100
            opportunity_conversion_rate = st.number_input("Opportunity conversion rate (%)", min_value=0.0, max_value=100.0, value=30.0, key="opportunity_conversion_rate") / 100
            meetings_held = st.number_input("Number of meetings held", min_value=0, value=30, key="meetings_held")
            follow_ups_per_lead = st.number_input("Number of follow-ups per lead", min_value=0, value=3, key="follow_ups_per_lead")
            sales_cycle_length = st.number_input("Sales cycle length (days)", min_value=0, value=30, key="sales_cycle_length")
            price_of_offer = st.number_input("Price of offer", min_value=0.0, value=500.0, key="price_of_offer")
            number_of_sdrs = st.number_input("Number of SDRs", min_value=0, value=2, key="number_of_sdrs")
            contact_per_month_per_sdr = st.number_input("Number of contacts per month per SDR", min_value=0, value=200, key="contact_per_month_per_sdr")
            average_deals_per_sales_rep_per_month = st.number_input("Average deals per sales rep per month", min_value=0.0, value=5.0, key="average_deals_per_sales_rep_per_month")
            cost_to_sell_percentage = st.number_input("Cost to sell (%)", min_value=0.0, max_value=100.0, value=15.0, key="cost_to_sell_percentage") / 100
            time_to_sell_days = st.number_input("Time to sell (days)", min_value=0, value=45, key="time_to_sell_days")
            outbound_salary = st.number_input("Outbound salary", min_value=0.0, value=4000.0, key="outbound_salary")
            sales_team_salary = st.number_input("Total sales team salary", min_value=0.0, value=20000.0, key="sales_team_salary")
            sales_commission_rate = st.number_input("Sales commission rate (%)", min_value=0.0, max_value=100.0, value=5.0, key="sales_commission_rate") / 100
            time_to_market_inbound = st.number_input("Time to market inbound (days)", min_value=0, value=60, key="time_to_market_inbound")
            time_to_market_organic = st.number_input("Time to market organic (days)", min_value=0, value=90, key="time_to_market_organic")
            time_to_market_outbound = st.number_input("Time to market outbound (days)", min_value=0, value=45, key="time_to_market_outbound")
            
            st.markdown("### Marketing Metrics")
            cost_per_lead = st.number_input("Cost per lead", min_value=0.0, value=10.0, key="cost_per_lead")
            cost_per_meeting = st.number_input("Cost per meeting", min_value=0.0, value=50.0, key="cost_per_meeting")
            funnel_conversion_rate = st.number_input("Funnel conversion rate (%)", min_value=0.0, max_value=100.0, value=15.0, key="funnel_conversion_rate") / 100
            conversion_rate_outbound = st.number_input("Conversion rate outbound (%)", min_value=0.0, max_value=100.0, value=3.0, key="conversion_rate_outbound") / 100
            click_through_rate = st.number_input("Click through rate (%)", min_value=0.0, max_value=100.0, value=2.5, key="click_through_rate") / 100
            lead_to_customer_conversion_rate_inbound = st.number_input("Lead to customer conversion rate inbound (%)", min_value=0.0, max_value=100.0, value=10.0, key="lead_to_customer_conversion_rate_inbound") / 100
            organic_views_per_month = st.number_input("Organic views per month", min_value=0, value=5000, key="organic_views_per_month")
            organic_view_to_lead_conversion_rate = st.number_input("Organic view to lead conversion rate (%)", min_value=0.0, max_value=100.0, value=2.0, key="organic_view_to_lead_conversion_rate") / 100
            lead_to_customer_conversion_rate_organic = st.number_input("Lead to customer conversion rate organic (%)", min_value=0.0, max_value=100.0, value=5.0, key="lead_to_customer_conversion_rate_organic") / 100
            cost_per_thousand_impressions = st.number_input("Cost per thousand impressions (CPM)", min_value=0.0, value=25.0, key="cost_per_thousand_impressions")
            marketing_spend = st.number_input("Total marketing spend", min_value=0.0, value=5000.0, key="marketing_spend")
            media_spend = st.number_input("Media spend", min_value=0.0, value=3000.0, key="media_spend")
        
        with col2:
            st.markdown("### Offer Metrics")
            churn_rate = st.number_input("Churn rate (%)", min_value=0.0, max_value=100.0, value=10.0, key="churn_rate") / 100
            contract_length = st.number_input("Average contract length (months)", min_value=0, value=12, key="contract_length")
            discount_rate = st.number_input("Average discount rate (%)", min_value=0.0, max_value=100.0, value=10.0, key="discount_rate") / 100
            refund_rate = st.number_input("Refund rate (%)", min_value=0.0, max_value=100.0, value=5.0, key="refund_rate") / 100
            refund_period = st.number_input("Refund period (days)", min_value=0, value=14, key="refund_period")
            customer_acquisition_cost = st.number_input("Customer acquisition cost (CAC)", min_value=0.0, value=200.0, key="customer_acquisition_cost")
            avg_customer_lifetime_value = st.number_input("Average customer lifetime value (CLTV)", min_value=0.0, value=5000.0, key="avg_customer_lifetime_value")
            price_of_renewal = st.number_input("Price of renewal", min_value=0.0, value=450.0, key="price_of_renewal")
            rate_of_renewals = st.number_input("Rate of renewals (%)", min_value=0.0, max_value=100.0, value=70.0, key="rate_of_renewals") / 100
            transaction_fees = st.number_input("Transaction fees (%)", min_value=0.0, max_value=100.0, value=2.5, key="transaction_fees") / 100
            seasonality_adjustment = st.number_input("Seasonality adjustment (% change in sales)", min_value=-100.0, max_value=100.0, value=10.0, key="seasonality_adjustment") / 100
            
            st.markdown("### Operations Metrics")
            cogs = st.number_input("Cost of goods sold (COGS)", min_value=0.0, value=5000.0, key="cogs")
            operating_expenses = st.number_input("Total operating expenses", min_value=0.0, value=10000.0, key="operating_expenses")
            fixed_costs_per_month = st.number_input("Fixed costs per month", min_value=0.0, value=15000.0, key="fixed_costs_per_month")
            product_dev_cost = st.number_input("Product development cost", min_value=0.0, value=10000.0, key="product_dev_cost")
            cost_to_fulfil = st.number_input("Cost to fulfil", min_value=0.0, value=200.0, key="cost_to_fulfil")
            time_to_collect = st.number_input("Time to collect (days)", min_value=0, value=30, key="time_to_collect")
            
            st.markdown("### Cash Metrics")
            total_addressable_market = st.number_input("Total addressable market", min_value=0, value=100000, key="total_addressable_market")
            initial_number_of_customers = st.number_input("Initial number of customers", min_value=0, value=100, key="initial_number_of_customers")
            cash_in_the_bank = st.number_input("Cash in the bank", min_value=0.0, value=50000.0, key="cash_in_the_bank")
            assets = st.number_input("Assets", min_value=0.0, value=75000.0, key="assets")
            liabilities = st.number_input("Liabilities", min_value=0.0, value=25000.0, key="liabilities")
            debt = st.number_input("Debt", min_value=0.0, value=10000.0, key="debt")
            debt_interest_rate = st.number_input("Debt interest rate (%)", min_value=0.0, max_value=100.0, value=5.0, key="debt_interest_rate") / 100
        
        st.markdown("### Additional Notes")
        col3, col4 = st.columns(2)
        
        with col3:
            st.info("All metrics have been categorized in the main sections above.")
        
        with col4:
            st.info("Click 'Run Simulation' to calculate and visualize results.")
        
        submitted = st.form_submit_button("Run Simulation")

    # Calculate metrics when form is submitted
    if submitted:
        # Collect all inputs into a dictionary
        input_data = {
            # Sales Metrics
            "leads_generated": leads_generated,
            "lead_conversion_rate": lead_conversion_rate,
            "opportunity_conversion_rate": opportunity_conversion_rate,
            "average_deal_size": average_deal_size,
            "meetings_held": meetings_held,
            "follow_ups_per_lead": follow_ups_per_lead,
            "sales_cycle_length": sales_cycle_length,
            "price_of_offer": price_of_offer,
            "number_of_sdrs": number_of_sdrs,
            "contact_per_month_per_sdr": contact_per_month_per_sdr,
            "average_deals_per_sales_rep_per_month": average_deals_per_sales_rep_per_month,
            "cost_to_sell_percentage": cost_to_sell_percentage,
            "time_to_sell_days": time_to_sell_days,
            "outbound_salary": outbound_salary,
            "sales_team_salary": sales_team_salary,
            "sales_commission_rate": sales_commission_rate,
            "time_to_market_inbound": time_to_market_inbound,
            "time_to_market_organic": time_to_market_organic,
            "time_to_market_outbound": time_to_market_outbound,
            
            # Marketing Metrics
            "cost_per_lead": cost_per_lead,
            "cost_per_meeting": cost_per_meeting,
            "funnel_conversion_rate": funnel_conversion_rate,
            "conversion_rate_outbound": conversion_rate_outbound,
            "click_through_rate": click_through_rate,
            "lead_to_customer_conversion_rate_inbound": lead_to_customer_conversion_rate_inbound,
            "organic_views_per_month": organic_views_per_month,
            "organic_view_to_lead_conversion_rate": organic_view_to_lead_conversion_rate,
            "lead_to_customer_conversion_rate_organic": lead_to_customer_conversion_rate_organic,
            "cost_per_thousand_impressions": cost_per_thousand_impressions,
            "marketing_spend": marketing_spend,
            "media_spend": media_spend,
            
            # Offer Metrics
            "churn_rate": churn_rate,
            "contract_length": contract_length,
            "discount_rate": discount_rate,
            "refund_rate": refund_rate,
            "refund_period": refund_period,
            "customer_acquisition_cost": customer_acquisition_cost,
            "avg_customer_lifetime_value": avg_customer_lifetime_value,
            "price_of_renewal": price_of_renewal,
            "rate_of_renewals": rate_of_renewals,
            "transaction_fees": transaction_fees,
            "seasonality_adjustment": seasonality_adjustment,
            
            # Operations Metrics
            "cogs": cogs,
            "operating_expenses": operating_expenses,
            "fixed_costs_per_month": fixed_costs_per_month,
            "product_dev_cost": product_dev_cost,
            "cost_to_fulfil": cost_to_fulfil,
            "time_to_collect": time_to_collect,
            
            # Cash Metrics
            "total_addressable_market": total_addressable_market,
            "initial_number_of_customers": initial_number_of_customers,
            "cash_in_the_bank": cash_in_the_bank,
            "assets": assets,
            "liabilities": liabilities,
            "debt": debt,
            "debt_interest_rate": debt_interest_rate
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
        
        if PLOTLY_AVAILABLE:
            fig_revenue = px.bar(df_revenue, x='Category', y='Amount', title='Revenue Breakdown')
            st.plotly_chart(fig_revenue)
        else:
            st.warning("Plotly visualization unavailable. Please install plotly package.")
            st.dataframe(df_revenue)
        
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
        
        if PLOTLY_AVAILABLE:
            fig_profit = px.bar(df_profit, x='Stage', y='Value', color='Type', 
                                title='Profit Waterfall', 
                                color_discrete_map={'Revenue': 'green', 'Cost': 'red', 'Profit': 'blue'})
            st.plotly_chart(fig_profit)
        else:
            st.warning("Plotly visualization unavailable. Please install plotly package.")
            st.dataframe(df_profit)

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
                    
                    if PLOTLY_AVAILABLE:
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
                    else:
                        st.warning("Plotly visualization unavailable. Please install plotly package.")
                        st.dataframe(df_chart)
                
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
                    "seasonality_adjustment": "Seasonality Adjustment",
                    "price_of_offer": "Price of Offer",
                    "price_of_renewal": "Price of Renewal",
                    "rate_of_renewals": "Rate of Renewals",
                    "media_spend": "Media Spend",
                    "funnel_conversion_rate": "Funnel Conversion Rate",
                    "lead_to_customer_conversion_rate_inbound": "Lead to Customer Conversion Rate Inbound",
                    "fixed_costs_per_month": "Fixed Costs Per Month",
                    "cost_per_thousand_impressions": "Cost Per Thousand Impressions (CPM)",
                    "conversion_rate_outbound": "Conversion Rate Outbound",
                    "click_through_rate": "Click Through Rate",
                    "time_to_market_inbound": "Time to Market Inbound",
                    "organic_views_per_month": "Organic Views Per Month",
                    "organic_view_to_lead_conversion_rate": "Organic View to Lead Conversion Rate",
                    "lead_to_customer_conversion_rate_organic": "Lead to Customer Conversion Rate Organic",
                    "time_to_market_organic": "Time to Market Organic",
                    "time_to_market_outbound": "Time to Market Outbound",
                    "outbound_salary": "Outbound Salary",
                    "number_of_sdrs": "Number of SDRs",
                    "contact_per_month_per_sdr": "Contact Per Month Per SDR",
                    "average_deals_per_sales_rep_per_month": "Average Deals Per Sales Rep Per Month",
                    "cost_to_sell_percentage": "Cost to Sell %",
                    "time_to_sell_days": "Time to Sell Days",
                    "cost_to_fulfil": "Cost to Fulfil",
                    "time_to_collect": "Time to Collect",
                    "refund_period": "Refund Period",
                    "total_addressable_market": "Total Addressable Market",
                    "initial_number_of_customers": "Initial Number of Customers",
                    "cash_in_the_bank": "Cash in the Bank",
                    "assets": "Assets",
                    "liabilities": "Liabilities",
                    "debt": "Debt",
                    "debt_interest_rate": "Debt Interest Rate",
                    "transaction_fees": "Transaction Fees"
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
                                       "sales_commission_rate", "discount_rate", "refund_rate", "seasonality_adjustment",
                                       "rate_of_renewals", "funnel_conversion_rate", "lead_to_customer_conversion_rate_inbound",
                                       "conversion_rate_outbound", "click_through_rate", "organic_view_to_lead_conversion_rate",
                                       "lead_to_customer_conversion_rate_organic", "cost_to_sell_percentage", 
                                       "debt_interest_rate", "transaction_fees"]:
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
                        
                        if PLOTLY_AVAILABLE:
                            if param in ["lead_conversion_rate", "opportunity_conversion_rate", "churn_rate", 
                                      "sales_commission_rate", "discount_rate", "refund_rate", "seasonality_adjustment",
                                      "rate_of_renewals", "funnel_conversion_rate", "lead_to_customer_conversion_rate_inbound",
                                      "conversion_rate_outbound", "click_through_rate", "organic_view_to_lead_conversion_rate",
                                      "lead_to_customer_conversion_rate_organic", "cost_to_sell_percentage", 
                                      "debt_interest_rate", "transaction_fees"]:
                                # Format as percentage
                                fig = px.bar(df_chart, x='Simulation', y='Value', title=f"Comparison of {param_name}",
                                            labels={"Value": f"{param_name} (%)"})
                                # Convert to percentage for display
                                fig.update_layout(yaxis_tickformat='.2%')
                            else:
                                fig = px.bar(df_chart, x='Simulation', y='Value', title=f"Comparison of {param_name}")
                            
                            st.plotly_chart(fig)
                        else:
                            st.warning("Plotly visualization unavailable. Please install plotly package.")
                            st.dataframe(df_chart)
                            
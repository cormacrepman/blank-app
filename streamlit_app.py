
import streamlit as st

# Set page title and configuration
st.set_page_config(page_title="Comprehensive Sales Metrics Simulator", layout="wide")

st.title("Comprehensive Sales Metrics Simulator")
st.write("Enter your sales metrics to generate a comprehensive analysis")

# Create a form for user inputs
with st.form("sales_metrics_form"):
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
    
    submitted = st.form_submit_button("Calculate Metrics")

# Calculate metrics when form is submitted
if submitted:
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

    # Display results in an organized way
    st.header("Sales Metrics Results")
    
    # Results in tabs
    tab1, tab2, tab3 = st.tabs(["Revenue & Profit", "Customer Metrics", "Cost Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Revenue Generated", f"£{revenue_generated:,.2f}")
            st.metric("Gross Profit", f"£{gross_profit:,.2f}")
            st.metric("Operating Profit", f"£{operating_profit:,.2f}")
        with col2:
            st.metric("Net Profit", f"£{net_profit:,.2f}")
            st.metric("Profit Margin", f"{profit_margin:.2%}")
            st.metric("Seasonality Adjusted Revenue", f"£{seasonality_adjusted_revenue:,.2f}")
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Leads Generated", f"{leads_generated:,.0f}")
            st.metric("Opportunities", f"{opportunities:,.0f}")
            st.metric("Customers", f"{customers:,.0f}")
        with col2:
            st.metric("Customer Acquisition Cost (CAC)", f"£{customer_acquisition_cost:,.2f}")
            st.metric("Customer Lifetime Value (CLTV)", f"£{avg_customer_lifetime_value:,.2f}")
            st.metric("CLTV to CAC Ratio", f"{avg_customer_lifetime_value/customer_acquisition_cost:.2f}x" if customer_acquisition_cost > 0 else "N/A")
            st.metric("Customer Retention Rate", f"{customer_retention_rate:.2%}")
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Break-even Point", f"£{break_even_point:,.2f}")
            st.metric("ROI for Marketing", f"{roi:.2f}%")
            st.metric("Total Cost of Leads", f"£{total_cost_leads:,.2f}")
            st.metric("Total Cost of Meetings", f"£{total_cost_meetings:,.2f}")
        with col2:
            st.metric("Total Sales Commission", f"£{total_sales_team_commission:,.2f}")
            st.metric("Total Marketing Spend", f"£{total_marketing_spend:,.2f}")
            st.metric("Discounts Given", f"£{discounts_given:,.2f}")
            st.metric("Refunds Given", f"£{refunds_given:,.2f}")
    
    # Visualizations
    st.subheader("Key Metrics Visualization")
    
    # Simple bar chart for revenue breakdown
    import pandas as pd
    import plotly.express as px
    
    # Revenue breakdown
    revenue_data = {
        'Category': ['Gross Revenue', 'After Discounts', 'After Refunds', 'Seasonality Adjusted'],
        'Amount': [
            revenue_generated, 
            revenue_generated - discounts_given,
            revenue_generated - discounts_given - refunds_given,
            seasonality_adjusted_revenue
        ]
    }
    
    df_revenue = pd.DataFrame(revenue_data)
    fig_revenue = px.bar(df_revenue, x='Category', y='Amount', title='Revenue Breakdown')
    st.plotly_chart(fig_revenue)
    
    # Profit waterfall
    profit_data = {
        'Stage': ['Revenue', 'COGS', 'Gross Profit', 'Operating Expenses', 'Commissions', 'Marketing', 'Net Profit'],
        'Value': [revenue_generated, -cogs, gross_profit, -operating_expenses, -total_sales_team_commission, -total_marketing_spend, net_profit],
        'Type': ['Revenue', 'Cost', 'Profit', 'Cost', 'Cost', 'Cost', 'Profit']
    }
    
    df_profit = pd.DataFrame(profit_data)
    fig_profit = px.bar(df_profit, x='Stage', y='Value', color='Type', 
                        title='Profit Waterfall', 
                        color_discrete_map={'Revenue': 'green', 'Cost': 'red', 'Profit': 'blue'})
    st.plotly_chart(fig_profit)

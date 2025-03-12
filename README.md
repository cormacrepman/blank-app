# Comprehensive Sales Metrics Simulator

# Get user input for various sales and business metrics
leads_generated = float(input("Enter number of leads generated: "))
lead_conversion_rate = float(input("Enter lead conversion rate (as a percentage, e.g. 20 for 20%): ")) / 100
opportunity_conversion_rate = float(input("Enter opportunity conversion rate (as a percentage, e.g. 30 for 30%): ")) / 100
average_deal_size = float(input("Enter average deal size (revenue per deal): "))
cost_per_lead = float(input("Enter cost per lead: "))
cost_per_meeting = float(input("Enter cost per meeting: "))
meetings_held = int(input("Enter number of meetings held: "))

follow_ups_per_lead = int(input("Enter number of follow-ups per lead: "))
sales_cycle_length = int(input("Enter sales cycle length (days): "))
cogs = float(input("Enter cost of goods sold (COGS): "))
customer_acquisition_cost = float(input("Enter customer acquisition cost (CAC): "))
contract_length = int(input("Enter average contract length (months): "))
avg_customer_lifetime_value = float(input("Enter average customer lifetime value (CLTV): "))
churn_rate = float(input("Enter churn rate (as a percentage, e.g. 10 for 10%): ")) / 100
customer_retention_rate = 1 - churn_rate
operating_expenses = float(input("Enter total operating expenses: "))
sales_team_salary = float(input("Enter total sales team salary: "))
sales_commission_rate = float(input("Enter sales commission rate (as a percentage, e.g. 5 for 5%): ")) / 100
marketing_spend = float(input("Enter total marketing spend: "))
product_dev_cost = float(input("Enter product development cost: "))
discount_rate = float(input("Enter average discount rate (percentage, e.g. 10 for 10%): ")) / 100
refund_rate = float(input("Enter refund rate (as a percentage, e.g. 5 for 5%): ")) / 100
seasonality_adjustment = float(input("Enter seasonality adjustment (percentage change in sales, e.g. 10 for +10%): ")) / 100

# Calculate derived metrics
opportunities = leads_generated * lead_conversion_rate
customers = opportunities * opportunity_conversion_rate
revenue_generated = customers * average_deal_size
profit_margin = (revenue_generated - (cogs + operating_expenses)) / revenue_generated
total_cost_leads = leads_generated * cost_per_lead
total_cost_meetings = meetings_held * cost_per_meeting
# Removed: total_cost_follow_ups = leads_generated * follow_ups_per_lead * cost_per_follow_up
total_sales_team_commission = revenue_generated * sales_commission_rate
total_marketing_spend = marketing_spend + product_dev_cost
discounts_given = revenue_generated * discount_rate
refunds_given = revenue_generated * refund_rate
seasonality_adjusted_revenue = revenue_generated * (1 + seasonality_adjustment)

# Calculate profit and other metrics
gross_profit = revenue_generated - cogs
operating_profit = gross_profit - operating_expenses
net_profit = operating_profit - total_sales_team_commission - total_marketing_spend
# Removed total_cost_follow_ups from the break-even calculation:
break_even_point = total_cost_leads + total_cost_meetings
roi = (net_profit / total_marketing_spend) * 100

# Output results
print("\n--- Comprehensive Sales Metrics Results ---")
print(f"Revenue Generated: £{revenue_generated:,.2f}")
print(f"Gross Profit: £{gross_profit:,.2f}")
print(f"Operating Profit: £{operating_profit:,.2f}")
print(f"Net Profit: £{net_profit:,.2f}")
print(f"Break-even Point: £{break_even_point:,.2f}")
print(f"Return on Investment (ROI) for Marketing: {roi:.2f}%")
print(f"Customer Acquisition Cost (CAC): £{customer_acquisition_cost:,.2f}")
print(f"Customer Lifetime Value (CLTV): £{avg_customer_lifetime_value:,.2f}")
print(f"Churn Rate: {churn_rate * 100}%")
print(f"Retention Rate: {customer_retention_rate * 100}%")
print(f"Seasonality Adjusted Revenue: £{seasonality_adjusted_revenue:,.2f}")
print(f"Discounts Given: £{discounts_given:,.2f}")
print(f"Refunds Given: £{refunds_given:,.2f}")
# Comprehensive Sales Metrics Simulator

# Get user input for various sales and business metrics
leads_generated = float(input("Enter number of leads generated: "))
lead_conversion_rate = float(input("Enter lead conversion rate (as a percentage, e.g. 20 for 20%): ")) / 100
opportunity_conversion_rate = float(input("Enter opportunity conversion rate (as a percentage, e.g. 30 for 30%): ")) / 100
average_deal_size = float(input("Enter average deal size (revenue per deal): "))
cost_per_lead = float(input("Enter cost per lead: "))
cost_per_meeting = float(input("Enter cost per meeting: "))
meetings_held = int(input("Enter number of meetings held: "))

follow_ups_per_lead = int(input("Enter number of follow-ups per lead: "))
sales_cycle_length = int(input("Enter sales cycle length (days): "))
cogs = float(input("Enter cost of goods sold (COGS): "))
customer_acquisition_cost = float(input("Enter customer acquisition cost (CAC): "))
contract_length = int(input("Enter average contract length (months): "))
avg_customer_lifetime_value = float(input("Enter average customer lifetime value (CLTV): "))
churn_rate = float(input("Enter churn rate (as a percentage, e.g. 10 for 10%): ")) / 100
customer_retention_rate = 1 - churn_rate
operating_expenses = float(input("Enter total operating expenses: "))
sales_team_salary = float(input("Enter total sales team salary: "))
sales_commission_rate = float(input("Enter sales commission rate (as a percentage, e.g. 5 for 5%): ")) / 100
marketing_spend = float(input("Enter total marketing spend: "))
product_dev_cost = float(input("Enter product development cost: "))
discount_rate = float(input("Enter average discount rate (percentage, e.g. 10 for 10%): ")) / 100
refund_rate = float(input("Enter refund rate (as a percentage, e.g. 5 for 5%): ")) / 100
seasonality_adjustment = float(input("Enter seasonality adjustment (percentage change in sales, e.g. 10 for +10%): ")) / 100

# Calculate derived metrics
opportunities = leads_generated * lead_conversion_rate
customers = opportunities * opportunity_conversion_rate
revenue_generated = customers * average_deal_size
profit_margin = (revenue_generated - (cogs + operating_expenses)) / revenue_generated
total_cost_leads = leads_generated * cost_per_lead
total_cost_meetings = meetings_held * cost_per_meeting
# Removed: total_cost_follow_ups = leads_generated * follow_ups_per_lead * cost_per_follow_up
total_sales_team_commission = revenue_generated * sales_commission_rate
total_marketing_spend = marketing_spend + product_dev_cost
discounts_given = revenue_generated * discount_rate
refunds_given = revenue_generated * refund_rate
seasonality_adjusted_revenue = revenue_generated * (1 + seasonality_adjustment)

# Calculate profit and other metrics
gross_profit = revenue_generated - cogs
operating_profit = gross_profit - operating_expenses
net_profit = operating_profit - total_sales_team_commission - total_marketing_spend
# Removed total_cost_follow_ups from the break-even calculation:
break_even_point = total_cost_leads + total_cost_meetings
roi = (net_profit / total_marketing_spend) * 100

# Output results
print("\n--- Comprehensive Sales Metrics Results ---")
print(f"Revenue Generated: £{revenue_generated:,.2f}")
print(f"Gross Profit: £{gross_profit:,.2f}")
print(f"Operating Profit: £{operating_profit:,.2f}")
print(f"Net Profit: £{net_profit:,.2f}")
print(f"Break-even Point: £{break_even_point:,.2f}")
print(f"Return on Investment (ROI) for Marketing: {roi:.2f}%")
print(f"Customer Acquisition Cost (CAC): £{customer_acquisition_cost:,.2f}")
print(f"Customer Lifetime Value (CLTV): £{avg_customer_lifetime_value:,.2f}")
print(f"Churn Rate: {churn_rate * 100}%")
print(f"Retention Rate: {customer_retention_rate * 100}%")
print(f"Seasonality Adjusted Revenue: £{seasonality_adjusted_revenue:,.2f}")
print(f"Discounts Given: £{discounts_given:,.2f}")
print(f"Refunds Given: £{refunds_given:,.2f}")
print(f"Total Sales Team Commission: £{total_sales_team_commission:,.2f}")

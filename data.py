import streamlit as st
import pandas as pd
import ast

# Function to read sales data from the uploaded file
def read_sales_data(uploaded_file):
    lines = uploaded_file.read().decode('utf-8').splitlines()
    sales_data = []
    for line_number, line in enumerate(lines, start=1):
        try:
            sales_data.append(ast.literal_eval(line.strip()))
        except Exception as e:
            st.error(f"Error parsing line {line_number}: {line}\n{e}")
    return sales_data

# Function to calculate and display the sales report
def generate_sales_report(sales_data):
    total_items_sold = 0
    total_discounts_given = 0
    total_taxes_collected = 0
    total_sales_amount = 0

    sales_table_data = []

    for sale in sales_data:
        item = sale['item']
        quantity = sale['quantity']
        price_per_unit = sale['price_per_unit']
        discount = sale['discount']
        tax_rate = sale['tax_rate']

        gross_amount = quantity * price_per_unit
        discount_amount = gross_amount * discount
        net_amount = gross_amount - discount_amount
        tax_amount = net_amount * tax_rate
        final_amount = net_amount + tax_amount

        total_items_sold += quantity
        total_discounts_given += discount_amount
        total_taxes_collected += tax_amount
        total_sales_amount += final_amount

        sales_table_data.append({
            "Item": item,
            "Quantity Sold": quantity,
            "Gross Amount (₹)": gross_amount,
            "Discount Amount (₹)": discount_amount,
            "Net Amount (₹)": net_amount,
            "Tax Amount (₹)": tax_amount,
            "Final Amount (₹)": final_amount
        })

    sales_df = pd.DataFrame(sales_table_data)
    sales_df.index = sales_df.index + 1  # Set the index to start from 1
    
    st.write("### Sales Report")
    st.table(sales_df)

    # Prepare summary data
    summary_data = {
        "Summary": ["Total Number of Items Sold", "Total Discounts Given (₹)", "Total Taxes Collected (₹)", "Total Sales Amount (₹)"],
        "Value": [total_items_sold, f"{total_discounts_given:.2f}", f"{total_taxes_collected:.2f}", f"{total_sales_amount:.2f}"]
    }

    summary_df = pd.DataFrame(summary_data)
    summary_df.index = summary_df.index + 1  # Set the index to start from 1
    
    st.write("### Summary")
    st.table(summary_df)

# Streamlit app
st.title("Sales Data Analysis")

uploaded_file = st.file_uploader("Choose a file (sales_data.txt)", type=["txt"])

if uploaded_file is not None:
    sales_data = read_sales_data(uploaded_file)
    if sales_data:
        generate_sales_report(sales_data)
else:
    st.write("Please upload a file to analyze.")
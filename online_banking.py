#!/usr/bin/env python3

# Financial Data Analysis
# This notebook performs financial data analysis on a CSV file, including data processing, monthly summaries, and visualization.
# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib.table import Table
from tabulate import tabulate
import os

# Set up basic plot style
plt.style.use('default')  # Use the default style instead of 'seaborn'
sns.set_theme(style="whitegrid")  # This applies Seaborn's whitegrid theme
import pandas as pd

# Read the CSV file
data = pd.read_csv("private/import/import.csv", sep=";", encoding='utf-8')

# Print the column names to confirm
print("Columns in the CSV file:")
print(data.columns.tolist())

# Rename columns to English
column_mapping = {
    "Bezeichnung Auftragskonto": "Account_Name",
    "IBAN Auftragskonto": "IBAN_Account",
    "BIC Auftragskonto": "BIC_Account",
    "Bankname Auftragskonto": "Bank_Name_Account",
    "Buchungstag": "Booking_Date",
    "Valutadatum": "Value_Date",
    "Name Zahlungsbeteiligter": "Name_Payer",
    "IBAN Zahlungsbeteiligter": "IBAN_Payer",
    "BIC (SWIFT-Code) Zahlungsbeteiligter": "BIC_Payer",
    "Buchungstext": "Booking_Text",
    "Verwendungszweck": "Purpose",
    "Betrag": "Amount",
    "Waehrung": "Currency",
    "Saldo nach Buchung": "Balance_After_Booking",
    "Bemerkung": "Remark",
    "Kategorie": "Category",
    "Steuerrelevant": "Tax_Relevant",
    "Glaeubiger ID": "Creditor_ID",
    "Mandatsreferenz": "Mandate_Reference"
}

# Rename the columns
data = data.rename(columns=column_mapping)

# Convert date columns
date_columns = ['Booking_Date', 'Value_Date']
for col in date_columns:
    data[col] = pd.to_datetime(data[col], format='%d.%m.%Y', errors='coerce')

# Convert Amount and Balance_After_Booking to numeric
for col in ['Amount', 'Balance_After_Booking']:
    data[col] = data[col].str.replace(',', '.').astype(float)

# Display the first few rows of the data
print("\nFirst few rows of the processed data:")
print(data.head())

# Display info about the dataframe
print("\nDataframe Info:")
data.info()
# Create monthly tables
monthly_tables = {}
months = data['Booking_Date'].dt.to_period('M').unique()

for i, month in enumerate(months, 1):
    month_data = data[data['Booking_Date'].dt.to_period('M') == month]
    month_table = month_data[['Booking_Date', 'Name_Payer', 'Amount', 'Currency']]
    monthly_tables[f'Month{i}'] = month_table
    monthly_tables[f'Month{i}'].attrs['month'] = month.strftime('%m.%Y')

# Display the first few rows of the first monthly table
print(list(monthly_tables.values())[0].head())
# Calculate monthly summary
monthly_summary = []

for month_table in monthly_tables.values():
    total_in = month_table['Amount'][month_table['Amount'] > 0].sum()
    total_out = month_table['Amount'][month_table['Amount'] < 0].sum()
    net_money = total_in + total_out
    
    monthly_summary.append({
        'Month': month_table.attrs['month'],
        'Total_In': total_in,
        'Total_Out': total_out,
        'Net_Money': net_money
    })

monthly_summary_df = pd.DataFrame(monthly_summary)

# Display the monthly summary
print(monthly_summary_df)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# Create a graph of the account balance over time
plt.figure(figsize=(12, 6))
plt.plot(data['Booking_Date'], data['Balance_After_Booking'])
plt.title('Account Balance Over Time')
plt.xlabel('Date')
plt.ylabel('Balance')
plt.xticks(rotation=45)

# Set the x-axis to show months
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

# Add vertical lines for each month
for month in pd.date_range(start=data['Booking_Date'].min(), end=data['Booking_Date'].max(), freq='MS'):
    plt.axvline(month, color='gray', linestyle='--', alpha=0.5)

plt.tight_layout()

# Save the balance graph as an image file
plt.savefig('private/images/balance_graph_all.png', dpi=300)

# Display the plot
plt.show()
# Convert 'Booking_Date' to datetime if it's not already
data['Booking_Date'] = pd.to_datetime(data['Booking_Date'])

# Get all available months
available_months = data['Booking_Date'].dt.to_period('M').unique()
available_months = sorted(available_months, reverse=True)  # Sort in reverse order

# Print available months
print("Available months:")
for i, month in enumerate(available_months, 1):
    print(f"{i}. {month}")

# Prompt user for month selection
while True:
    try:
        selection = int(input("\nEnter the number of the month you want to analyze: "))
        if 1 <= selection <= len(available_months):
            selected_month = available_months[selection - 1]
            break
        else:
            print("Invalid selection. Please enter a number from the list.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Filter data for selected month
selected_data = data[data['Booking_Date'].dt.to_period('M') == selected_month]

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 14), gridspec_kw={'height_ratios': [2, 1]})

# Plot balance graph
ax1.plot(selected_data['Booking_Date'], selected_data['Balance_After_Booking'], marker='o')
ax1.set_title(f'Account Balance - {selected_month}', fontsize=14)
ax1.set_xlabel('Date', fontsize=10)
ax1.set_ylabel('Balance', fontsize=10)
ax1.tick_params(axis='both', which='major', labelsize=8)  # Reduce tick label size

# Set x-axis to show days
ax1.xaxis.set_major_locator(mdates.DayLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

# Add vertical lines for each day
for day in selected_data['Booking_Date'].unique():
    ax1.axvline(day, color='gray', linestyle='--', alpha=0.5)

# Add grid to the balance graph
ax1.grid(True, linestyle=':', alpha=0.7)

# List top 10 largest negative transactions
negative_transactions = selected_data[selected_data['Amount'] < 0].sort_values('Amount')
top_10_negative = negative_transactions.head(10)

def format_currency(amount):
    return f"€{amount:.2f}"

# Create a table for the top 10 negative transactions
table_data = []
for index, row in top_10_negative.iterrows():
    date = row['Booking_Date'].strftime('%Y-%m-%d')
    amount = f"{row['Amount']:.2f}"
    name = row['Name_Payer'][:42]  # Increase to 20 characters
    purpose = row['Purpose'][:42]  # Increase to 25 characters
    table_data.append([date, amount, name, purpose])

# Create the table
table = Table(ax2, bbox=[0, 0, 1, 1])
table.auto_set_font_size(False)
table.set_fontsize(9)  # Slightly reduce font size

# Define column widths (adjust these values as needed)
col_widths = [0.10, 0.08, 0.35, 0.35]  # Date, Amount, Name, Purpose

# Add table to the plot
n_rows = len(table_data) + 1
for i in range(n_rows):
    for j, width in enumerate(col_widths):
        if i == 0:
            cell_text = ['Date', 'Amount', 'Name', 'Purpose'][j]
            cell_color = '#f0f0f0'
            font_weight = 'bold'
        else:
            cell_text = table_data[i-1][j]
            cell_color = 'white'
            font_weight = 'normal'
        table.add_cell(i, j, width=width, height=1/n_rows, text=cell_text, 
                       loc='center', facecolor=cell_color)
        table._cells[(i, j)]._text.set_fontweight(font_weight)

ax2.add_table(table)
ax2.set_title('Top 10 Largest Negative Transactions', fontsize=12)
ax2.axis('off')

# Adjust layout
plt.tight_layout()

# Save the graph as an image file
plt.savefig(f'private/images/{selected_month}_graph.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()

# Print statistics for the selected month
print(f"\n{selected_month} Statistics:")
print(f"{'Number of transactions:':<25} {len(selected_data)}")
print(f"{'Starting balance:':<25} {format_currency(selected_data['Balance_After_Booking'].iloc[-1])}")
print(f"{'Ending balance:':<25} {format_currency(selected_data['Balance_After_Booking'].iloc[0])}")
print(f"{'Net change:':<25} {format_currency(selected_data['Balance_After_Booking'].iloc[0] - selected_data['Balance_After_Booking'].iloc[-1])}")

# Prepare data for top 10 largest negative transactions
top_10_data = []
for index, row in top_10_negative.iterrows():
    top_10_data.append([
        row['Booking_Date'].strftime('%Y-%m-%d'),
        format_currency(row['Amount']),
        row['Name_Payer'],
        row['Purpose'][:70] + '...' if len(row['Purpose']) > 70 else row['Purpose']
    ])

# Print top 10 largest negative transactions
print("\nTop 10 Largest Negative Transactions:")
print(tabulate(top_10_data, headers=['Date', 'Amount', 'Name', 'Purpose'], 
               tablefmt='pretty', colalign=('center', 'right', 'left', 'left')))
# Ensure the images directory exists
if not os.path.exists('private/images'):
    os.makedirs('private/images')

# Convert 'Booking_Date' to datetime if it's not already
data['Booking_Date'] = pd.to_datetime(data['Booking_Date'])

# Get all available months
available_months = data['Booking_Date'].dt.to_period('M').unique()
available_months = sorted(available_months, reverse=True)  # Sort in reverse order

# Create a graph for each month
for month in available_months:
    # Filter data for the current month
    monthly_data = data[data['Booking_Date'].dt.to_period('M') == month]
    
    # Create the graph
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]})
    
    ax1.plot(monthly_data['Booking_Date'], monthly_data['Balance_After_Booking'], marker='o')
    ax1.set_title(f'Account Balance - {month}')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Balance')
    
    # Set x-axis to show days
    ax1.xaxis.set_major_locator(mdates.DayLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # Add vertical lines for each day
    for day in monthly_data['Booking_Date'].unique():
        ax1.axvline(day, color='gray', linestyle='--', alpha=0.5)
    
    # Adjust layout and display grid
    ax1.grid(True, linestyle=':', alpha=0.7)
    
    # Get top 10 largest negative transactions
    top_negative = monthly_data[monthly_data['Amount'] < 0].nsmallest(10, 'Amount')
    table_data = [
        (row['Booking_Date'].strftime('%Y-%m-%d'), 
         f"{row['Amount']:.2f}", 
         row['Name_Payer'][:65] + '...' if len(row['Name_Payer']) > 65 else row['Name_Payer'], 
         row['Purpose'][:65] + '...' if len(row['Purpose']) > 65 else row['Purpose'])
        for _, row in top_negative.iterrows()
    ]
    
    # Create the table
    table = Table(ax2, bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(9)  # Default font size
    
    # Define column widths (adjust these values as needed)
    col_widths = [0.10, 0.08, 0.35, 0.35]  # Date, Amount, Name, Purpose
    
    # Add table to the plot
    n_rows = len(table_data) + 1
    for i in range(n_rows):
        for j, width in enumerate(col_widths):
            if i == 0:
                cell_text = ['Date', 'Amount', 'Name', 'Purpose'][j]
                cell_color = '#f0f0f0'
                font_weight = 'bold'
                font_size = 9
            else:
                cell_text = table_data[i-1][j]
                cell_color = 'white'
                font_weight = 'normal'
                font_size = 8 if j == 3 else 9  # Smaller font for Purpose column
            
            cell = table.add_cell(i, j, width=width, height=1/n_rows, text=cell_text, 
                                  loc='center', facecolor=cell_color)
            cell.set_text_props(fontweight=font_weight, fontsize=font_size)
    
    ax2.add_table(table)
    ax2.set_title('Top 10 Largest Negative Transactions', fontsize=12)
    ax2.axis('off')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the graph as an image file
    plt.savefig(f'private/images/{month}_graph.png', dpi=300, bbox_inches='tight')
    
    # Close the figure to free up memory
    plt.close()
    
    # Print statistics for the month
    print(f"\n{month} Statistics:")
    print(f"Number of transactions: {len(monthly_data)}")
    print(f"Starting balance: {monthly_data['Balance_After_Booking'].iloc[-1]:.2f}")
    print(f"Ending balance: {monthly_data['Balance_After_Booking'].iloc[0]:.2f}")
    print(f"Net change: {monthly_data['Balance_After_Booking'].iloc[0] - monthly_data['Balance_After_Booking'].iloc[-1]:.2f}")

print("\nAll monthly graphs with tables have been generated and saved in the 'private/images' folder.")
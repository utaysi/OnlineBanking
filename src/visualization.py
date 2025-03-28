import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib.table import Table
from tabulate import tabulate
import os
import pandas as pd

# Set the style
plt.style.use('seaborn-v0_8-dark')

# Set default colors
facecolor = 'black'
axescolor = '#333333'
labelcolor = 'white'

def format_currency(amount):
    """Formats the amount as currency."""
    return f"€{amount:.2f}"

def generate_all_time_graph(data):
    """Generates a graph of the account balance over time."""
    fig, ax = plt.subplots(figsize=(12, 6), facecolor=facecolor)
    ax.plot(data['Booking_Date'], data['Balance_After_Booking'], color='skyblue')
    ax.set_title('Account Balance Over Time', color=labelcolor)
    ax.set_xlabel('Date', color=labelcolor)
    ax.set_ylabel('Balance', color=labelcolor)
    ax.tick_params(axis='x', rotation=45, color=labelcolor, labelcolor=labelcolor)
    ax.tick_params(axis='y', color=labelcolor, labelcolor=labelcolor)
    ax.set_facecolor(axescolor)
    ax.spines['bottom'].set_color(labelcolor)
    ax.spines['top'].set_color(labelcolor)
    ax.spines['left'].set_color(labelcolor)
    ax.spines['right'].set_color(labelcolor)

    # Set the x-axis to show months
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    # Add vertical lines for each month
    for month in pd.date_range(start=data['Booking_Date'].min(), end=data['Booking_Date'].max(), freq='MS'):
        ax.axvline(month, color='gray', linestyle='--', alpha=0.5)

    fig.tight_layout()

    # Save the balance graph as an image file
    plt.savefig('private/images/balance_graph_all.png', dpi=300, facecolor=fig.get_facecolor())

    # Save the balance graph as an image file

def generate_monthly_graph(data, selected_month):
    """Generates a graph of the account balance and top spending for a specific month."""
    # Filter data for selected month
    selected_data = data[data['Booking_Date'].dt.to_period('M') == selected_month]

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 14), gridspec_kw={'height_ratios': [2, 1]}, facecolor=facecolor)
    ax1.set_facecolor(axescolor)
    ax2.set_facecolor(axescolor)

    # Calculate horizontal offset
    # Plot balance graph
    ax1.plot(selected_data['Virtual_Booking_Date'], selected_data['Balance_After_Booking'], marker='o', color='skyblue')
    ax1.set_title(f'Account Balance - {selected_month}', fontsize=14, color=labelcolor)
    ax1.set_xlabel('Date', fontsize=10, color=labelcolor)
    ax1.set_ylabel('Balance', fontsize=10, color=labelcolor)
    ax1.tick_params(axis='both', which='major', labelsize=8, color=labelcolor, labelcolor=labelcolor)  # Reduce tick label size

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
                cell_color = axescolor
                font_weight = 'bold'
            else:
                cell_text = table_data[i-1][j]
                cell_color = axescolor
                font_weight = 'normal'
            table.add_cell(i, j, width=width, height=1/n_rows, text=cell_text,
                           loc='center', facecolor=cell_color)
            table._cells[(i, j)]._text.set_fontweight(font_weight)
            table._cells[(i, j)]._text.set_color(labelcolor)

    ax2.add_table(table)
    ax2.set_title('Top 10 Largest Negative Transactions', fontsize=12, color=labelcolor)
    ax2.axis('off')

    # Adjust layout
    plt.tight_layout()

    # Save the graph as an image file
    plt.savefig(f'private/images/monthly_graphs/{selected_month}_graph.png', dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())

    # Save the monthly graph as an image file
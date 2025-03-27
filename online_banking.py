#!/usr/bin/env python3

import matplotlib.pyplot as plt
import seaborn as sns
# Financial Data Analysis
# This notebook performs financial data analysis on a CSV file, including data processing, monthly summaries, and visualization.
# Import required libraries
import pandas as pd

# Set up basic plot style
plt.style.use('default')  # Use the default style instead of 'seaborn'
sns.set_theme(style="whitegrid")  # This applies Seaborn's whitegrid theme

from src.data_processing import load_and_preprocess_data, calculate_monthly_summary
from src.visualization import generate_all_time_graph, generate_monthly_graph

# Load and preprocess the data
data = load_and_preprocess_data()

if data is None:
    exit()

# Display the first few rows of the data
print("\nFirst few rows of the processed data:")
print(data.head())

# Display info about the dataframe
print("\nDataframe Info:")
data.info()

# Calculate monthly summary
monthly_summary_df = calculate_monthly_summary(data)

# Display the monthly summary
print(monthly_summary_df)

# Generate all time graph
generate_all_time_graph(data)

# Convert 'Booking_Date' to datetime if it's not already
data['Booking_Date'] = pd.to_datetime(data['Booking_Date'])

# Get all available months
available_months = data['Booking_Date'].dt.to_period('M').unique()
available_months = sorted(available_months, reverse=True)  # Sort in reverse order

# Print available months
print("Available months:")
for i, month in enumerate(available_months, 1):
    print(f"{i}. {month}")

# Create a folder to store the monthly graphs
import os
if not os.path.exists("private/images/monthly_graphs"):
    os.makedirs("private/images/monthly_graphs")

# Iterate through all available months and generate monthly graphs
for i, selected_month in enumerate(available_months):
    # Filter data for selected month
    selected_data = data[data['Booking_Date'].dt.to_period('M') == selected_month]

    # Generate monthly graph
    generate_monthly_graph(data, selected_month)
    percentage = (i + 1) / len(available_months) * 100
    print(f"\rProgress: {percentage:.2f}%", end="")
print()  # Add a newline at the end
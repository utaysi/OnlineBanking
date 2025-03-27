# Optimization Plan for Online Banking Script

## Overview

This document outlines the plan for optimizing the `online_banking.ipynb` script. The goal is to improve the script's structure, maintainability, scalability, and efficiency.

## Current Script Functionality

The script currently performs the following tasks:

*   Imports a bank CSV file.
*   Structures each transaction in a continuous, structured way.
*   Creates monthly and all-time graphs.
*   Shows top spendings per month.

## Proposed Optimizations

The following architectural optimizations are proposed:

1.  **Modularize the code:**
    *   Create functions for:
        *   `load_and_preprocess_data(file_path)`: Loads the CSV file, renames columns, converts data types, and handles missing values.
        *   `calculate_monthly_summary(data)`: Calculates the total income, expenses, and net change for each month.
        *   `generate_all_time_graph(data)`: Generates a graph of the account balance over time.
        *   `generate_monthly_graph(data, month)`: Generates a graph of the account balance and top spending for a specific month.
        *   `display_monthly_statistics(data, month)`: Displays statistics for a specific month, including the number of transactions, starting balance, ending balance, and net change.
    *   Consider using a `TransactionAnalyzer` class to encapsulate the data and functions.
2.  **Improve data processing:**
    *   Use `pd.to_datetime` and `pd.to_numeric` for vectorized data type conversions.
    *   Implement error handling for invalid data values using `try-except` blocks.
3.  **Refactor graphing logic:**
    *   Use Seaborn for creating visually appealing graphs.
    *   Create a generic graphing function that can be used for both all-time and monthly graphs.
4.  **Enhance user interaction:**
    *   Implement a file selection dialog using `tkinter` to allow the user to select the input CSV file.
    *   Use the default "private/images" directory for the output graphs.
5.  **Improve code maintainability:**
    *   Remove duplicate import statements.
    *   Use relative file paths instead of hardcoded paths.
    *   Add comments and docstrings to explain the code.

## Architecture Diagram

```mermaid
graph LR
    A[User Input: CSV File Path (File Selection Dialog)] --> B(Data Loading and Preprocessing)
    B --> C{Data Validation}
    C -- Valid --> D(Data Storage: Pandas DataFrame)
    C -- Invalid --> E[Error Handling]
    D --> F(Monthly Summary Calculation)
    D --> G(All-Time Graph Generation (Seaborn))
    D --> H(Monthly Graph Generation (Seaborn))
    F --> I(Display Monthly Summary)
    G --> J(Save/Display All-Time Graph)
    H --> K(Save/Display Monthly Graphs)
    E --> A
    I --> A
    J --> A
    K --> A
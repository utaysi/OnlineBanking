# Updated Optimization Plan for Online Banking Script

## Overview

This document outlines the plan for optimizing the `online_banking.py` script. The goal is to improve the script's structure, maintainability, scalability, and efficiency.

## Current Script Functionality

The script currently performs the following tasks:

*   Imports a bank CSV file.
*   Structures each transaction in a continuous, structured way.
*   Creates monthly and all-time graphs.
*   Shows top spendings per month.

## Proposed Optimizations

The following architectural optimizations are proposed:

**1. Project Structure:**

*   Create a new directory structure to organize the code:

    ```
    online_banking/
    ├── data/
    │   └── import.csv (Keep in original location)
    ├── src/
    │   ├── data_processing.py
    │   ├── visualization.py
    │   ├── utils.py
    ├── online_banking.py (Keep same file name)
    ├── private/
    │   └── images/
    ├── optimization_plan.md
    └── README.md
    ```

**2. Modularization:**

*   **`online_banking.py`:**
    *   This will be the main entry point of the script.
    *   It will handle user interaction, calling the data processing and visualization modules.
*   **`src/data_processing.py`:**
    *   This module will contain functions for loading and preprocessing data:
        *   `load_data(file_path)`: Loads the CSV file using `pd.read_csv`.
        *   `preprocess_data(data)`: Renames columns, converts data types, and handles missing values.
*   **`src/visualization.py`:**
    *   This module will contain functions for generating graphs and tables:
        *   `generate_all_time_graph(data)`: Generates a graph of the account balance over time using Seaborn.
        *   `generate_monthly_graph(data, month)`: Generates a graph of the account balance and top spending for a specific month using Seaborn.
*   **`src/utils.py`:**
    *   This module will contain utility functions:
        *   `format_currency(amount)`: Formats the amount as currency.
        *   `get_top_transactions(data, n=10)`: Returns the top N largest negative transactions.

**3. Data Processing Improvements:**

*   Use `pd.to_datetime` and `pd.to_numeric` for vectorized data type conversions.
*   Implement error handling for invalid data values using `try-except` blocks.
*   Use a configuration file (`config.json`) to store column mappings and other settings.

**4. Graphing Logic Refactoring:**

*   Use Seaborn for creating visually appealing graphs.
*   Create a generic graphing function that can be used for both all-time and monthly graphs.
*   Save graphs to the `private/images` directory.

**5. User Interaction Enhancements:**

*   Implement a file selection dialog using `tkinter` to allow the user to select the input CSV file.
*   Use the default "private/images" directory for the output graphs.

**6. Code Maintainability Improvements:**

*   Remove duplicate import statements.
*   Use relative file paths instead of hardcoded paths.
*   Add comments and docstrings to explain the code.
*   Use a consistent coding style (e.g., PEP 8).

**7. Implementation Steps:**

1.  Create the directory structure.
2.  Move the existing code into the appropriate modules.
3.  Implement the data processing improvements.
4.  Refactor the graphing logic.
5.  Enhance user interaction.
6.  Improve code maintainability.
7.  Test the script thoroughly.

## Architecture Diagram

```mermaid
graph LR
    A[User Input: CSV File Path (File Selection Dialog)] --> B(Data Loading (data_processing.load_data))
    B --> C(Data Preprocessing (data_processing.preprocess_data))
    C --> D{Data Validation}
    D -- Valid --> E(Data Storage: Pandas DataFrame)
    D -- Invalid --> F[Error Handling]
    E --> G(Monthly Summary Calculation (data_processing.calculate_monthly_summary))
    E --> H(All-Time Graph Generation (visualization.generate_all_time_graph))
    E --> I(Monthly Graph Generation (visualization.generate_monthly_graph))
    G --> J(Display Monthly Summary)
    H --> K(Save/Display All-Time Graph)
    I --> L(Save/Display Monthly Graphs)
    F --> A
    J --> A
    K --> A
    L --> A
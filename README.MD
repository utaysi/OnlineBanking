# Financial Data Analysis Project

This project performs financial data analysis on CSV files, including data processing, monthly summaries, and visualization.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview

This Python script-based project is designed to analyze financial transaction data from CSV files. It provides various functionalities such as data processing, monthly summaries, and visualization of account balances and transactions. The codebase is modularized into separate components for data processing, visualization, and utilities.

## Features

- Data import and preprocessing from CSV files
- Monthly transaction summaries
- Account balance visualization over time
- Monthly detailed analysis with graphs and tables
- Top 10 largest negative transactions for each month
- Automated graph generation for all available months
- Chronological transaction ordering within days (oldest to newest)
- Modular and maintainable code architecture

## Screenshots

### Monthly Analysis Example
![Monthly Analysis](demo-images/demo-monthly.png)

Monthly analysis view, including the account balance graph and the top 10 largest negative transactions for a specific month.

### Overall Account Balance
![Overall Account Balance](demo-images/demo-overall.png)

Account balance over time view, providing a comprehensive summary of financial trends across multiple months.

## Requirements

- Python 3.x
- pandas
- matplotlib
- seaborn
- tabulate
- tqdm

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/financial-data-analysis.git
   cd financial-data-analysis
   ```

2. Install the required packages:
   ```
   pip install pandas matplotlib seaborn tabulate tqdm
   ```

## Usage

1. Place your CSV file in the `private/import/` directory and name it `import.csv`.

2. Run the main script:
   ```
   python online_banking.py
   ```

3. The script will automatically:
   - Load and preprocess your financial data
   - Display basic information about the data
   - Calculate monthly summaries
   - Generate an overall account balance graph
   - Generate detailed monthly graphs for each available month
   - Save all generated graphs to the `private/images/` directory

4. The monthly graphs will be saved in the `private/images/monthly_graphs/` directory with filenames like `YYYY-MM_graph.png`.

## File Structure

```
financial-data-analysis/
│
├── online_banking.py                # Main script file
├── README.md                        # This file
├── src/                             # Source code directory
│   ├── data_processing.py           # Data loading and processing
│   ├── visualization.py             # Data visualization
│   └── utils.py                     # Utility functions
├── plans/                           # Project planning documents
│   ├── transaction_ordering_plan.md
│   └── transaction_ordering_results.md
├── private/                         # Private data (not tracked by git)
│   ├── import/
│   │   └── import.csv               # Your financial data file
│   └── images/
│       ├── balance_graph_all.png    # Overall balance graph
│       └── monthly_graphs/          # Monthly detailed graphs
│           └── YYYY-MM_graph.png
├── demo-images/                     # Demo images for README
│   ├── demo-monthly.png
│   └── demo-overall.png
└── .gitignore
```

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
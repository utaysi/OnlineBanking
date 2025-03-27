import pandas as pd
import numpy as np

def load_and_preprocess_data():
    """
    Loads and preprocesses the financial data from the default CSV file.

    Returns:
        pandas.DataFrame: The preprocessed financial data.
    """
    file_path = "private/import/import.csv"

    # Read the CSV file
    try:
        data = pd.read_csv(file_path, sep=";", encoding='utf-8')
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

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
        try:
            data[col] = data[col].str.replace(',', '.').astype(float)
        except ValueError:
            print(f"Could not convert column {col} to numeric. Please check the data.")
            raise

    # Calculate virtual timestamps with random offset
    data['Transaction_Order'] = data.groupby('Booking_Date').cumcount()
    data['Transactions_Per_Day'] = data.groupby('Booking_Date')['Booking_Date'].transform('count')
    data['Virtual_Timestamp'] = 1 - (data['Transaction_Order'] / data['Transactions_Per_Day'])
    data['Virtual_Timestamp'] = data['Virtual_Timestamp'].clip(0, 1)  # Ensure the timestamp stays within 0 and 1
    data['Virtual_Booking_Date'] = data['Booking_Date'] + pd.to_timedelta(data['Virtual_Timestamp'], unit='D')

    return data
def calculate_monthly_summary(data):
    """
    Calculates the monthly summary of the financial data.

    Args:
        data (pandas.DataFrame): The preprocessed financial data.

    Returns:
        pandas.DataFrame: The monthly summary of the financial data.
    """
    # Create monthly tables
    monthly_tables = {}
    months = data['Booking_Date'].dt.to_period('M').unique()

    for i, month in enumerate(months, 1):
        month_data = data[data['Booking_Date'].dt.to_period('M') == month]
        month_table = month_data[['Booking_Date', 'Name_Payer', 'Amount', 'Currency']]
        monthly_tables[f'Month{i}'] = month_table
        monthly_tables[f'Month{i}'].attrs['month'] = month.strftime('%m.%Y')

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

    return monthly_summary_df
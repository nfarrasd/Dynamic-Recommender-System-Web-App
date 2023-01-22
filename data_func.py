import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

import string
import random


# Read Sheet File
def get_data(names : str):
    # Connect to Sheet
    scope_app = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive', 
                 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive'] 
    cred = ServiceAccountCredentials.from_json_keyfile_name('recommender-system-375210-4fb076db18bf.json', scope_app) 
    client = gspread.authorize(cred)

    # Fetch the Data
    sheet = client.open(f'{names}').sheet1
    df = pd.DataFrame(sheet.get_all_values())

    # Data Cleaning
    df.columns = df.iloc[0]
    df = df[df.columns[1:]]
    df = df.iloc[1:].reset_index(drop = True)
    df = df.dropna()

    if names != 'stocks_data':
        for col in df.columns:
            df[col] = df[col].astype(float).astype(int)

    else:
        for col in df.columns:
            if col not in ['StockCode', 'Description']:
                df[col] = df[col].astype(float).astype(int)

    return df


# Update Database Users Data
def update_users_stocks(id : str,
                        name : str):
    # Connect to Sheet
    scope_app = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive', 
                 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive'] 
    cred = ServiceAccountCredentials.from_json_keyfile_name('recommender-system-375210-4fb076db18bf.json', scope_app) 
    client = gspread.authorize(cred)

    if name == 'user':
        # Fetch the Data
        customer = client.open('customers_data').sheet1
        customer_data = get_data('customers_data') # 3

        if id not in customer_data['CustomerID'].values:
            # Insert row to the Customer Data
            max_idx3 = max(customer_data.index) + 1
            encoded_user = max_idx3
            row3 = [max_idx3, id, encoded_user]
            customer.insert_row(row3)

    elif name == 'stock':
        # Fetch the Data
        stock = client.open('stocks_data').sheet1
        stock_data = get_data('stocks_data') # 4

        if id not in stock_data['StockCode'].values:
            # Insert row to the Stock Data
            max_idx4 = max(stock_data.index) + 1
            encoded_stock = max_idx4
            row4 = [max_idx4, id, encoded_stock, 'pass']
            stock.insert_row(row4)

    pass


# Update Database Transactions Data
def update_transactions(users_id : str,
                        stocks_id : str,
                        n_count : int):
    # Connect to Sheet
    scope_app = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive', 
                 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive'] 
    cred = ServiceAccountCredentials.from_json_keyfile_name('recommender-system-375210-4fb076db18bf.json', scope_app) 
    client = gspread.authorize(cred)

    # Fetch the Data
    purchase = client.open('purchase_data').sheet1
    binary = client.open('binary_data').sheet1

    purchase_data = get_data('purchase_data') # 1
    binary_data = get_data('binary_data') # 2
    customer_data = get_data('customers_data') # 3
    stock_data = get_data('stocks_data') # 4

    # Check existing values
    if users_id in customer_data['CustomerID'].values:
        encoded_user = customer_data.loc[customer_data['CustomerID'] == users_id]['Encoder'].values[0]
        if stocks_id in stock_data['StockCode'].values:
            encoded_stock = stock_data.loc[stock_data['StockCode'] == stocks_id]['Encoder'].values[0]

            # Update cell in the Purchase Data
            temp1 = purchase_data.loc[(purchase_data['CustomerID'] == encoded_user) &
                                      (purchase_data['StockCode'] == encoded_stock)]
            idx1 = temp1.index[0]
            val1 = temp1.iloc[idx1]['value']
            purchase.update_cell(1, 4, val1 + n_count)

            # Update cell in the Binary Data
            temp2 = binary_data.loc[(binary_data['CustomerID'] == encoded_user) &
                                    (binary_data['StockCode'] == encoded_stock)]
            idx2 = temp2.index[0]
            val2 = temp2.iloc[idx2]['value']
            binary.update_cell(1, 4, 1)

    pass

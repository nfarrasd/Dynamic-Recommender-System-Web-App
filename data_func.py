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
            df[col] = df[col].astype(int)

    else:
        for col in df.columns:
            if col not in ['StockCode', 'Description']:
                df[col] = df[col].astype(int)

    return df


# Update Database Data
def update_data(users_id : str,
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
    customer = client.open('customers_data').sheet1
    stock = client.open('stocks_data').sheet1

    purchase_data = get_data('purchase_data') # 1
    binary_data = get_data('binary_data') # 2
    customer_data = get_data('customers_data') # 3
    stock_data = get_data('stocks_data') # 4

    # Check existing values
    if users_id in customer_data['CustomerID'].values:
        encoded_user = customer_data.loc[customer_data['CustomerID'] == users_id]['Encoder'].values[0]
        if stocks_id in stock_data['StockCode'].values:
            # Update cell in the Purchase Data
            encoded_stock = stock_data.loc[stock_data['StockCode'] == stocks_id]['Encoder'].values[0]
            temp1 = purchase_data.loc[(purchase_data['CustomerID'] == encoded_user) &
                                      (purchase_data['StockCode'] == encoded_stock)]
            idx1 = temp1.index[0]
            val1 = temp1.iloc[idx1]['value']
            purchase.update_cell(1, 4 , val1 + n_count)

        else:
            # Insert row to the Stock Data
            max_idx4 = max(stock_data.index) + 1
            encoded_stock = max_idx4
            row4 = [max_idx4, stocks_id, encoded_stock, 'pass']
            stock.insert_row(row4)

            # Insert row to the Purchase Data
            max_idx1 = max(purchase_data.index) + 1
            row1 = [max_idx1, encoded_user, encoded_stock, n_count]
            purchase.insert_row(row1)

            # Insert row to the Binary Data
            max_idx2 = max(binary_data.index) + 1
            row2 = [max_idx2, encoded_user, encoded_stock, 1]
            binary.insert_row(row2)

    else:
        # Insert row to the Customer Data
        max_idx3 = max(customer_data.index) + 1
        encoded_user = max_idx3
        row3 = [max_idx3, users_id, encoded_user]
        customer.insert_row(row3)

        if stocks_id in stock_data['StockCode'].values:
            encoded_stock = stock_data.loc[stock_data['StockCode'] == stocks_id]['Encoder'].values[0]

        else:
            letters = string.ascii_uppercase
            stock_desc = ''.join(random.choice(letters) for i in range(10))

            # Insert row to the Stock Data
            max_idx4 = max(stock_data.index) + 1
            encoded_stock = max_idx4
            row4 = [max_idx4, stocks_id, encoded_stock, stock_desc]
            stock.insert_row(row4)

        # Insert row to the Purchase Data
        max_idx1 = max(purchase_data.index) + 1
        row1 = [max_idx1, encoded_user, encoded_stock, n_count]
        purchase.insert_row(row1)

        # Insert row to the Binary Data
        max_idx2 = max(binary_data.index) + 1
        row2 = [max_idx2, encoded_user, encoded_stock, 1]
        binary.insert_row(row2)

    pass
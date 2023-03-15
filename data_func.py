import gspread
import pymongo
import pandas as pd

from oauth2client.service_account import ServiceAccountCredentials


# Read Sheet File
def get_data(names : str, source : str, query = {}):
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
    
    # Migration to MongoDB
    # Connect to MongoDB
    # client = pymongo.MongoClient('mongodb://localhost:27017/')

    # # Fetch the Data
    # db = client['recsys']
    # collection = db[names]
    # cursor = collection.find(query)

    # # Expand the cursor and construct the DataFrame
    # df =  pd.DataFrame(list(cursor))

    # # Delete the _id
    # try:
    #     del df['_id']

    # except:
    #     pass

    # return df


# Update Database Users Data
def update_users_stocks(id : str,
                        name : str,
                        description = None):
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
            customer.append_row(row3)

    elif name == 'stock':
        # Fetch the Data
        stock = client.open('stocks_data').sheet1
        stock_data = get_data('stocks_data') # 4

        if id not in stock_data['StockCode'].values:
            # Insert row to the Stock Data
            max_idx4 = max(stock_data.index) + 1
            encoded_stock = max_idx4
            row4 = [max_idx4, id, encoded_stock, description]
            stock.append_row(row4)

    pass


# Update Database Transactions Data
def update_transactions(users_id : str,
                        stocks_id : str,
                        n_count : str):
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
    if (users_id in customer_data['CustomerID'].values) & (stocks_id in stock_data['StockCode'].values):
        encoded_user = customer_data.loc[customer_data['CustomerID'] == users_id]['Encoder'].values[0]
        encoded_stock = stock_data.loc[stock_data['StockCode'] == stocks_id]['Encoder'].values[0]

        temp1 = purchase_data.loc[(purchase_data['CustomerID'] == encoded_user) &
                                  (purchase_data['StockID'] == encoded_stock)]

        if len(temp1) == 0:
            # Insert row to the Purchase Data
            max_idx1 = max(purchase_data.index) + 1
            row1 = [max_idx1, int(encoded_user), int(encoded_stock), n_count]
            purchase.append_row(row1)

            # Insert row to the Binary Data
            max_idx2 = max(binary_data.index) + 1
            row2 = [max_idx2, int(encoded_user), int(encoded_stock), 1]
            binary.append_row(row2)
            
        else:
            # Update cell in the Purchase Data
            idx1 = temp1.index[0]
            val1 = temp1.reset_index(drop = True).iloc[0]['value']
            purchase.update_cell(idx1 + 2, 4, int(val1) + int(n_count))

            # Update cell in the Binary Data
            temp2 = binary_data.loc[(binary_data['CustomerID'] == encoded_user) &
                                    (binary_data['StockID'] == encoded_stock)]
            idx2 = temp2.index[0]
            binary.update_cell(idx2 + 2, 4, '1')

    pass

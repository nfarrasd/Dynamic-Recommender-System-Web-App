import gspread
import pandas as pd
import turicreate as tc

from oauth2client.service_account import ServiceAccountCredentials

from data_func import get_data, update_users_stocks, update_transactions


# Recommended Result
def recom_result(customer_ID : str):
    customer_data = get_data('customers_data')
    binary_data = get_data('binary_data')
    old_customers = get_data('old_customers')
    new_customers = get_data('new_customers')

    if customer_ID in customer_data['CustomerID'].values:
        encoded_user = customer_data.loc[customer_data['CustomerID'] == customer_ID]['Encoder'].values[0]
        # Old purchasing customer
        if encoded_user in binary_data['CustomerID'].values:
            user_df = old_customers.loc[old_customers['CustomerID'] == encoded_user].reset_index(drop = True)

        # New customer
        else:
            user_df = new_customers.loc[new_customers['CustomerID'] == encoded_user].reset_index(drop = True)

        # Map Encoded Data
        def mapping(name : int):

            stock_data = get_data('stocks_data')
            stock = stock_data.loc[stock_data['Encoder'] == name]['StockCode'].values[0]

            return stock

        recommendations = ''
        for i in range(len(user_df)):
            if recommendations == '':
                recommendations = mapping(int(user_df.iloc[i]['StockID']))
                
            else:
                recommendations = recommendations + ' | ' + mapping(int(user_df.iloc[i]['StockID']))

        return recommendations

    else:
        return 'Customer ID does not exists.'


# Recommender System Model
def train_model(users_id = 'CustomerID', 
                items_id = 'StockID',
                targets = 'value',
                n_rec = 10):
                
    # Connect to Sheet
    scope_app = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive', 
                 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive'] 
    cred = ServiceAccountCredentials.from_json_keyfile_name('recommender-system-375210-4fb076db18bf.json', scope_app) 
    client = gspread.authorize(cred)

    # Fetch the Data
    old_customers = client.open('old_customers').sheet1
    new_customers = client.open('new_customers').sheet1

    customer_data = get_data('customers_data')
    purchase_data = get_data('purchase_data')
    binary_data = get_data('binary_data')

    users_to_recommend = list(set(customer_data['Encoder']))    

    # Purchase Counts with Pearson Similarity
    # Old customers
    model_1 = tc.item_similarity_recommender.create(tc.SFrame(purchase_data), 
                                                    user_id = users_id, 
                                                    item_id = items_id, 
                                                    target = targets, 
                                                    similarity_type = 'pearson')
            
    recom_1 = model_1.recommend(users = users_to_recommend, k = n_rec)

    # Popularity Model with Binary Input
    # New customers
    model_2 = tc.item_similarity_recommender.create(tc.SFrame(binary_data), 
                                                    user_id = users_id, 
                                                    item_id = items_id, 
                                                    target = targets)
            
    recom_2 = model_2.recommend(users = users_to_recommend, k = n_rec)

    def insert_list(lst):
        for i in range(len(lst)):
            lst[i].insert(0, i)

        return lst

    df_rec_1 = recom_1.to_dataframe()
    temp = df_rec_1.columns.values.tolist()
    temp.insert(0, '')
    old_customers.clear()
    old_customers.update([temp] + insert_list(df_rec_1.values.tolist()))

    df_rec_2 = recom_2.to_dataframe()
    temp = df_rec_2.columns.values.tolist()
    temp.insert(0, '')
    new_customers.clear()
    new_customers.update([temp] + insert_list(df_rec_2.values.tolist()))

    pass

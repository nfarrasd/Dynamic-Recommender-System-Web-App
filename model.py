import turicreate as tc

from data_func import get_data, update_data


# Recommender System Model
def final_model(customer_ID, 
                users_id = 'CustomerID', 
                items_id = 'StockID',
                targets = 'value',
                n_rec = 10):

    purchase_data = get_data('purchase_data')
    binary_data = get_data('binary_data')

    if customer_ID in purchase_data['CustomerID'].values:
        # Purchase Counts with Pearson Similarity
        model = tc.item_similarity_recommender.create(tc.SFrame(purchase_data), 
                                                    user_id = users_id, 
                                                    item_id = items_id, 
                                                    target = targets, 
                                                    similarity_type = 'pearson')
        
        recom = model.recommend(users = customer_ID, k = n_rec)

    else:
        # Popularity Model with Binary Input
        model = tc.item_similarity_recommender.create(tc.SFrame(binary_data), 
                                                  user_id = users_id, 
                                                  item_id = items_id, 
                                                  target = targets)
        
        recom = model.recommend(users = customer_ID, k = n_rec)

    df_rec = recom.to_dataframe()

    rec_list = list(df_rec.loc[df_rec['CustomerID'] == customer_ID]['StockID'])

    return mapping(rec_list, 'stock')


# Map Encoded Data
def mapping(lst : list, 
            name : str):

    customer_data = get_data('customers_data')
    stock_data = get_data('stocks_data')

    mapped = []
    if name == 'stock':
        for item in lst:
            stock = stock_data.loc[stock_data['Encoder'] == item]['StockCode']
            mapped.append(stock)
    
    else:
        for item in lst:
            customer = customer_data.loc[customer_data['Encoder'] == item]['CustomerID']
            mapped.append(customer)  

    return mapped
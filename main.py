from flask import Flask, jsonify, request, render_template

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from model import final_model, mapping
from data_func import get_data, update_users_stocks, update_transactions


# Connect to Sheet
scope_app = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive', 
             'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive'] 
cred = ServiceAccountCredentials.from_json_keyfile_name('recommender-system-375210-4fb076db18bf.json', scope_app) 
client = gspread.authorize(cred)

# Flask App
app = Flask(__name__, template_folder = 'template')


# Routing
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/updateUsers', methods = ['POST'])
def updateUsers():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):    
        req = request.get_json()
        users_id = req['CustomerID']

        update_users_stocks(id = users_id, 
                            name = 'user')
        return jsonify(req)

    else:
        return 'Invalid.'


@app.route('/updateStocks', methods = ['POST'])
def updateStocks():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        req = request.get_json()
        stocks_id = req['StockCode']
        stocks_description = req['Description']

        update_users_stocks(id = stocks_id, 
                            name = 'stock', 
                            description = stocks_description)
        return jsonify(req)

    else:
        return 'Invalid.'


@app.route('/updateTransactions', methods = ['POST'])
def updateTransactions():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        req = request.get_json()
        users_id = req['CustomerID']
        stocks_id = req['StockCode']
        n_count = req['value']

        update_transactions(users_id = users_id, 
                            stocks_id = stocks_id, 
                            n_count = n_count)
        return jsonify(req)

    else:
        return 'Invalid.'


@app.route('/predict', methods = ['POST'])
def predict():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        req = request.get_json()
        customer_ID = req['CustomerID']

        prediction = final_model(customer_ID, 
                                users_id = 'CustomerID', 
                                items_id = 'StockID',
                                targets = 'value',
                                n_rec = 10)

        return render_template('index.html', 
                                prediction_text = prediction)

    else:
        return 'Invalid.'


if __name__ == '__main__':
    app.debug = True
    app.run()

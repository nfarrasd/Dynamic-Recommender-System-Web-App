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
    req = request.get_json()
    users_id = req['CustomerID']

    update_users_stocks(users_id, 'user')
    return jsonify(req)


@app.route('/updateStocks', methods = ['POST'])
def updateStocks():
    req = request.get_json()
    stocks_id = req['StockCode']

    update_users_stocks(stocks_id, 'stock')
    return jsonify(req)


@app.route('/updateTransactions', methods = ['POST'])
def updateTransactions():
    req = request.get_json()
    users_id = req['CustomerID']
    stocks_id = req['StockCode']
    n_count = req['value']

    update_transactions(users_id, stocks_id, n_count)
    return jsonify(req)


@app.route('/predict', methods = ['POST'])
def predict():
    req = request.get_json()
    customer_ID = req['CustomerID']

    prediction = final_model(customer_ID, 
                            users_id = 'CustomerID', 
                            items_id = 'StockID',
                            targets = 'value',
                            n_rec = 10)

    output = ' | '.join(prediction)
    return render_template('index.html', prediction_text = f'Recommended Items Code: {output}')


if __name__ == '__main__':
    app.debug = True
    app.run()

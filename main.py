from flask import Flask, jsonify, request

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from model import get_data, final_model, mapping


# Connect to Sheet
scope_app = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive', 
             'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive'] 
cred = ServiceAccountCredentials.from_json_keyfile_name('recommender-system-375210-4fb076db18bf.json', scope_app) 
client = gspread.authorize(cred)

# Flask App
app = Flask(__name__)


# Routing

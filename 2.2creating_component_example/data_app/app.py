from flask import Flask, jsonify
import requests
import sys
import os
from flask import redirect

current_dir = os.path.dirname(os.path.abspath(__file__))

# Calculate the path to the directory you want to import from
parent_dir = os.path.join(current_dir, '../')
sys.path.append(parent_dir)

from data_service import clean_data

CLEANED_DATA = {}

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>This is the data cleaning service!</p>"

@app.route("/get_cleaned_data")
def get_cleaned_data():
    csv_file = '../MSFT.US.csv'
    x_train_flat, x_test_flat, y_train_flat, y_test_flat, dates_train_str, dates_test_str = clean_data(csv_file)
    CLEANED_DATA.update({
        'x_train_flat': x_train_flat,
        'x_test_flat': x_test_flat,
        'y_train_flat': y_train_flat,
        'y_test_flat': y_test_flat,
        'dates_train_str': dates_train_str,
        'dates_test_str': dates_test_str
    })
    return {
        'message': 'Data cleaned successfully!',
        'x_train': x_train_flat,
        'x_test': x_test_flat,
        'y_train': y_train_flat,
        'y_test': y_test_flat,
        'dates_train': dates_train_str,
        'dates_test': dates_test_str
    }

@app.route("/train_model")
def train_model_redirect():
    if CLEANED_DATA:
        headers = {'Content-Type': 'application/json'}
        data = {'cleaned_data': CLEANED_DATA}  # Assuming CLEANED_DATA is serializable to JSON
        response = requests.post('http://127.0.0.1:5001/train_model', json=data, headers=headers)
        return response.text
    else:
        return {
            'message': 'Data is not cleaned yet. Please clean the data first!'
        }


if __name__ == '__main__':
    app.run(port=5000)
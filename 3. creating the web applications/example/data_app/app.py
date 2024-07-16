from flask import Flask
import requests
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '../')
sys.path.append(parent_dir)
from data_service import clean_data

app = Flask(__name__)

@app.route("/")
def welcome_message():
    return "<p>This is the data cleaning service!</p>"

@app.route("/get_cleaned_data")
def get_cleaned_data():
    csv_file = './MSFT.US.csv'
    x_train_flat, x_test_flat, y_train_flat, y_test_flat, dates_train_str, dates_test_str = clean_data(csv_file)

    return {
        'message': 'Data cleaned successfully!',
        'x_train': x_train_flat,
        'x_test': x_test_flat,
        'y_train': y_train_flat,
        'y_test': y_test_flat,
        'dates_train': dates_train_str,
        'dates_test': dates_test_str
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
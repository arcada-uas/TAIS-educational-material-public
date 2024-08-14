from flask import Flask, request
from training_service import train_model
import sys
import pickle
import base64
import requests
sys.path.append('../')


app = Flask(__name__)


@app.route("/")
def welcome_message():
    return "<p>This is the training service!</p>"


@app.route("/train_model")
def train_model_cf():

    response = requests.get('http://localhost:5000/get_cleaned_data')
    data = response.json()
    if data:
        x_train_flat = data['x_train']
        y_train_flat = data['y_train']

        model = train_model(x_train_flat, y_train_flat)

        if not hasattr(model, 'predict'):
            return {'error': "The trained model does not have a 'predict' method."}

        try:
            model_base64 = base64.b64encode(pickle.dumps(model)).decode('utf-8')
        except Exception as e:
            return {'error': f"Error serializing model: {str(e)}"}

        return {'model': model_base64, 'x_test' : data['x_test'], 'y_test' : data['y_test'], 'dates_test' : data['dates_test']}
    else:
        return "No data provided", 400



if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=5001)
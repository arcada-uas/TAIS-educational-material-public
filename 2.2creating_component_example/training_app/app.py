from flask import Flask, request, jsonify
from training_service import train_model
import sys
import os
import pickle
import base64
import requests
sys.path.append('../')

variables = {}
y_test = None
dates_test = None
x_test = None

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>This is the training service!</p>"


@app.route("/train_model", methods=['POST', 'GET'])
def train_model_cf():
    if request.method == 'POST':
        data = request.json.get('cleaned_data')
        if data:
            x_train_flat = data['x_train_flat']
            print("x_train_flat:" + str(x_train_flat))
            y_train_flat = data['y_train_flat']
            #print("y_train_flat:" + str(y_train_flat))
            variables["y_test"] = data['y_test_flat']
            #print("y_test_flat:" + str(data['y_test_flat']))
            variables["dates_test"] = data['dates_test_str']
            print("dates_test_str:" + str(data['dates_test_str']))
            variables["x_test"] = data['x_test_flat']
            print("training lengths of data:")
            print("x len: " + str(len(x_train_flat)))
            print("y len: " + str(len(y_train_flat)))
            print("dates len: " + str(len(data['dates_test_str'])))



            model = train_model(x_train_flat, y_train_flat)

            print("model: " + str(model))


            if not hasattr(model, 'predict'):
                return {'error': "The trained model does not have a 'predict' method."}

            try:
                model_base64 = base64.b64encode(pickle.dumps(model)).decode('utf-8')
                variables["model"] = model_base64
            except Exception as e:
                return {'error': f"Error serializing model: {str(e)}"}

            return {'message': 'Model trained successfully!'}
        else:
            return "No data provided", 400
    else:
        return "<p>This is the training service, where the training happens!</p>"

        
@app.route("/test_model")
def redirect_test_model():
    if variables.get("model") is not None:
        headers = {'Content-Type': 'application/json'}
        data = {
            'model': (variables["model"]),
            'x_test': variables["x_test"],
            'y_test': variables["y_test"],
            'dates_test': variables["dates_test"]
        }
        response = requests.post('http://localhost:5002/test_model', json=data, headers=headers)
        return response.text
    else:
        return "<p>Model not found.</p>"



if __name__ == '__main__':
    app.run(port=5001)
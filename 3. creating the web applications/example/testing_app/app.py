
import pickle
import base64
from flask import Flask, request, send_file, jsonify
from test_service import test_model
import matplotlib
import requests
matplotlib.use('Agg') 


app = Flask(__name__)

@app.route("/")
def welcome_message():
    return "<p>This is the testing service!</p>"

def save_plot_image(plot_binary, filename):
    with open(filename, 'wb') as f:
        f.write(plot_binary)


@app.route("/test_model")
def test_model_cf():
    response = requests.get('http://localhost:5001/train_model')
    data = response.json()
    
    try:
        model_data = data.get('model')
    except Exception as e:
        return {'error': f"Error loading model data: {str(e)}"}

    try:
        model_binary = base64.b64decode(model_data)
        model = pickle.loads(model_binary)
    except Exception as e:
        return {'error': f"Error loading model: {str(e)}"}
    
    if not hasattr(model, 'predict'):
        return {'error': "The loaded model does not have a 'predict' method."}

    
    try:
        x_test = data.get('x_test')
        y_test = data.get('y_test')
        dates_test = data.get('dates_test')
    except Exception as e:
        return {'error': f"Error loading test data: {str(e)}"}

    try:
        rmse, plot_binary = test_model(model, x_test, y_test, dates_test)
        print("tested model successfully!")
    except Exception as e:
        return jsonify({'error': f"Error testing model: {str(e)}"}), 500



    response = {
        'rmse': rmse,
    }
    plot_filename = 'plot.png'
    save_plot_image(plot_binary, plot_filename)

    return response 


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
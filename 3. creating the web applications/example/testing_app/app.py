import os
import pickle
import base64
from flask import Flask, request, send_file, jsonify, render_template_string
from test_service import test_model
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>This is the testing service!</p>"


@app.route("/test_model", methods=['POST'])
def test_model_cf():
    # Assuming the model and data are sent as base64 encoded binary data in the request
    model_data = request.json.get('model')
    x_test = request.json.get('x_test')
    #print("x_test:" + str(x_test))
    y_test = request.json.get('y_test')
    #print("y_test:" + str(y_test))
    dates_test = request.json.get('dates_test')
    print("dates_test:" + str(dates_test))
    print("testing lengths of data:")
    print("x len: " + str(len(x_test)))
    print("y len: " + str(len(y_test)))
    print("dates len: " + str(len(dates_test)))


    
    # Decode and deserialize the model
    try:
        model_binary = base64.b64decode(model_data)
        model = pickle.loads(model_binary)
        print("model: " + str(model))
    except Exception as e:
        return {'error': f"Error loading model: {str(e)}"}

    # Ensure model is correctly deserialized
    if not hasattr(model, 'predict'):
        return {'error': "The loaded model does not have a 'predict' method."}



    print(type(model))

    # Call the test_model function
    
    try:
        rmse, plot_filename = test_model(model, x_test, y_test, dates_test)
        print("tested model successfully!")
    except Exception as e:
        return jsonify({'error': f"Error testing model: {str(e)}"}), 500

    print("RMSE: ", rmse)
    print("Plot filename: ", plot_filename)
    plot_url = f'/get_plot/{plot_filename}'

    response = {
        'rmse': rmse,
        'plot_url': plot_url
    }

    html_content = f"""
        <html>
        <head><title>Test Results</title></head>
        <body>
            <h1>Test Results</h1>
            <p>RMSE: {rmse}</p>
            <img src="{plot_url}" alt="Plot">
        </body>
        </html>
    """
    return response 
@app.route("/get_plot/<plot_filename>")
def get_plot(plot_filename):
    return send_file(f'./{plot_filename}', mimetype='image/png')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
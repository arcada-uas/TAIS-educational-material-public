# app.py

from flask import Flask, render_template, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Load the RMSE value from file
    rmse_value = 'No RMSE value available'
    if os.path.isfile('rmse_value.txt'):
        with open('rmse_value.txt', 'r') as file:
            rmse_value = file.read().strip()
    
    return render_template('index.html', rmse_value=rmse_value)

@app.route('/plot')
def plot():
    # Debugging code
    print("Current working directory:", os.getcwd())
    print("Files in the directory:", os.listdir('/app'))

    # Path to the plot
    plot_path = '/model_plot.png'

    # Ensure the file exists
    if not os.path.isfile(plot_path):
        return "File not found", 404
    return send_file(plot_path, mimetype='image/png')

def run_flask():
    app.run(host='0.0.0.0', port=8065)

from flask import Flask, request, jsonify, render_template
import grpc
import data_pb2_grpc
import data_pb2
import train_pb2_grpc
import train_pb2
import test_pb2_grpc
import test_pb2
import base64
import pandas as pd
import io

app = Flask(__name__)

# Function to check if a file is a CSV
def is_csv_file(filename):
    return filename.lower().endswith('.csv')

# Function to validate the CSV format
def validate_csv(file):
    try:
        data = pd.read_csv(file)
        required_columns = ['Date', 'Close']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            return f"Missing columns: {', '.join(missing_columns)}"
        
        # Check if there is enough data
        if data.shape[0] < 2:
            return "Not enough data for training. The CSV file must contain at least 2 rows."

        return None
    except pd.errors.EmptyDataError:
        return "The CSV file is empty."
    except Exception as e:
        return f"An error occurred during validation: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clean_data', methods=['POST'])
def clean_data():
    if 'csv_file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['csv_file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not is_csv_file(file.filename):
        return jsonify({'error': 'Invalid file format. Only CSV files are allowed.'}), 400

    # Validate the CSV file format
    validation_error = validate_csv(file)
    if validation_error:
        return jsonify({'error': validation_error}), 400

    try:
        # Read file content for gRPC request
        file.seek(0)  # Reset file pointer to start
        csv_content = file.read()
        
        # Use gRPC to clean the data
        with grpc.insecure_channel('localhost:8080') as channel:
            stub = data_pb2_grpc.DataServiceStub(channel)
            request_data = data_pb2.DataRequest(csv_content=csv_content)
            response = stub.CleanData(request_data)
            
            # Prepare cleaned data for response
            cleaned_data = {
                'x_train': list(response.x_train),
                'x_test': list(response.x_test),
                'y_train': list(response.y_train),
                'y_test': list(response.y_test),
                'dates_train': list(response.dates_train),
                'dates_test': list(response.dates_test)
            }
            
            return jsonify(cleaned_data)
    except grpc.RpcError as e:
        return jsonify({'error': f'RPC failed: {e.code()} - {e.details()}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/train_model', methods=['POST'])
def train_model():
    data = request.get_json()
    x_train = data.get('x_train')
    y_train = data.get('y_train')
    
    if x_train is None or y_train is None:
        return jsonify({'error': 'Invalid input data for model training'}), 400
    
    with grpc.insecure_channel('localhost:8081') as channel:
        stub = train_pb2_grpc.TrainingServiceStub(channel)
        try:
            response = stub.TrainModel(train_pb2.TrainRequest(x_train=x_train, y_train=y_train))
            if response.model:
                model_base64 = base64.b64encode(response.model).decode('utf-8')
                return jsonify({'message': 'Model trained successfully!', 'model': model_base64})
            else:
                return jsonify({'error': 'Model not trained'}), 500
        except grpc.RpcError as e:
            return jsonify({'error': f'RPC failed: {e.code()} - {e.details()}'}), 500

@app.route('/test_model', methods=['POST'])
def test_model():
    data = request.get_json()
    model_base64 = data.get('model')
    x_test = data.get('x_test')
    y_test = data.get('y_test')
    dates_test = data.get('dates_test')
    
    if model_base64 is None or x_test is None or y_test is None or dates_test is None:
        return jsonify({'error': 'Invalid input data for model testing'}), 400
    
    model_binary = base64.b64decode(model_base64)
    
    with grpc.insecure_channel('localhost:8082') as channel:
        stub = test_pb2_grpc.TestingServiceStub(channel)
        try:
            response = stub.TestModel(test_pb2.TestRequest(
                model=model_binary,
                x_test=x_test,
                y_test=y_test,
                dates_test=dates_test
            ))
            if response.rmse is not None:
                plot_base64 = base64.b64encode(response.plot).decode('utf-8')
                return jsonify({
                    'rmse': response.rmse,
                    'plot': plot_base64
                })
            else:
                return jsonify({'error': 'Model not tested'}), 500
        except grpc.RpcError as e:
            return jsonify({'error': f'RPC failed: {e.code()} - {e.details()}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify, render_template
import grpc
import data_pb2_grpc
import data_pb2
import train_pb2_grpc
import train_pb2
import test_pb2_grpc
import test_pb2
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clean_data', methods=['POST'])
def clean_data():
    csv_file_path = request.form['csv_file_path']
    
    with grpc.insecure_channel('localhost:8080') as channel:
        print("insecure channel")
        stub = data_pb2_grpc.DataServiceStub(channel)
        try:
            print("trying to open file")
            with open(csv_file_path, 'rb') as f:
                csv_content = f.read()
            request_data = data_pb2.DataRequest(csv_content=csv_content)
            response = stub.CleanData(request_data)
            print(response)
            print("returning data")
            return jsonify({
                'x_train': list(response.x_train),
                'x_test': list(response.x_test),
                'y_train': list(response.y_train),
                'y_test': list(response.y_test),
                'dates_train': list(response.dates_train),
                'dates_test': list(response.dates_test)
            })
        except grpc.RpcError as e:
            return jsonify({'error': f'RPC failed: {e.code()} - {e.details()}'}), 500

@app.route('/train_model', methods=['POST'])
def train_model():
    data = request.get_json()
    x_train = data['x_train']
    y_train = data['y_train']
    
    with grpc.insecure_channel('localhost:8081') as channel:
        stub = train_pb2_grpc.TrainingServiceStub(channel)
        try:
            response = stub.TrainModel(train_pb2.TrainRequest(x_train=x_train, y_train=y_train))
            if response.model:
                # Encode the model binary data to Base64
                model_base64 = base64.b64encode(response.model).decode('utf-8')
                return jsonify({'model': model_base64})
            else:
                return jsonify({'error': 'Model not trained'}), 500
        except grpc.RpcError as e:
            return jsonify({'error': f'RPC failed: {e.code()} - {e.details()}'}), 500

@app.route('/test_model', methods=['POST'])
def test_model():
    data = request.get_json()
    model_base64 = data['model']
    # Decode the model Base64 data to binary
    model_binary = base64.b64decode(model_base64)
    x_test = data['x_test']
    y_test = data['y_test']
    dates_test = data['dates_test']
    
    with grpc.insecure_channel('localhost:8082') as channel:
        stub = test_pb2_grpc.TestingServiceStub(channel)
        try:
            response = stub.TestModel(test_pb2.TestRequest(model=model_binary, x_test=x_test, y_test=y_test, dates_test=dates_test))
            if response.rmse is not None:
                # Encode the plot binary data to Base64
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

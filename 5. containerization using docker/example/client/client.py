import grpc
import data_pb2_grpc
import data_pb2
import train_pb2_grpc
import train_pb2
import test_pb2_grpc
import test_pb2
import base64
import json
import io

def save_plot_image(plot_binary, filename):
    with open(filename, 'wb') as f:
        f.write(plot_binary)

def main():
    csv_file_path = 'MSFT.US.csv'  # Use the provided CSV file path

    # Clean data
    with grpc.insecure_channel('localhost:8080') as channel:
        stub = data_pb2_grpc.DataServiceStub(channel)
        try:
            with open(csv_file_path, 'rb') as f:
                csv_content = f.read()
            request_data = data_pb2.DataRequest(csv_content=csv_content)
            response = stub.CleanData(request_data)
            cleaned_data = {
                'x_train': list(response.x_train),
                'x_test': list(response.x_test),
                'y_train': list(response.y_train),
                'y_test': list(response.y_test),
                'dates_train': list(response.dates_train),
                'dates_test': list(response.dates_test)
            }
            print("Data cleaned successfully.")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")
            return

    # Train model
    with grpc.insecure_channel('localhost:8081') as channel:
        stub = train_pb2_grpc.TrainingServiceStub(channel)
        try:
            response = stub.TrainModel(train_pb2.TrainRequest(
                x_train=cleaned_data['x_train'],
                y_train=cleaned_data['y_train']
            ))
            if response.model:
                model_base64 = base64.b64encode(response.model).decode('utf-8')
                print("Model trained successfully.")
            else:
                print("Model not trained.")
                return
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")
            return

    # Test model
    with grpc.insecure_channel('localhost:8082') as channel:
        stub = test_pb2_grpc.TestingServiceStub(channel)
        try:
            response = stub.TestModel(test_pb2.TestRequest(
                model=base64.b64decode(model_base64),
                x_test=cleaned_data['x_test'],
                y_test=cleaned_data['y_test'],
                dates_test=cleaned_data['dates_test']
            ))
            if response.rmse:
                print(f"RMSE: {response.rmse}")
                if response.plot:
                    plot_filename = 'plot.png'
                    save_plot_image(response.plot, plot_filename)
                    print(f"Plot saved as {plot_filename}.")
            else:
                print("Model not tested.")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")
            return

if __name__ == '__main__':
    main()

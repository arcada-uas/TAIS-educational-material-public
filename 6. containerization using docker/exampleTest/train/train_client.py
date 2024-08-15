import grpc
import model_pb2
import model_pb2_grpc
import pickle
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def run():
    # Load the cleaned data
    with open('cleaned_data.pkl', 'rb') as f:
        cleaned_data = pickle.load(f)

    # Create a channel and a stub (client)
    channel = grpc.insecure_channel('localhost:8063')
    stub = model_pb2_grpc.TrainingServiceStub(channel)

    # Create a TrainRequest message
    train_request = model_pb2.CleanedData(
        x_train=cleaned_data.x_test,  # Assuming x_test is used as x_train for training
        y_train=cleaned_data.y_test,  # Assuming y_test is used as y_train for training
        x_test=cleaned_data.x_test,
        y_test=cleaned_data.y_test,
        dates_train=cleaned_data.dates_train,
        dates_test=cleaned_data.dates_test
    )

    # Make the call
    try:
        logging.info("Sending training request to the server...")
        response = stub.TrainModel(train_request)
        logging.info("Received response from the server.")
        logging.info(f"Model: {response.model}")
    except grpc.RpcError as e:
        logging.error(f"gRPC error: {e.code()} - {e.details()}")

if __name__ == '__main__':
    run()
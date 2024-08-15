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
    # Load the TrainResponse
    with open('train_response.pkl', 'rb') as f:
        train_response = pickle.load(f)

    # Create a channel and a stub (client)
    channel = grpc.insecure_channel('localhost:8061')  # Change to the appropriate port
    stub = model_pb2_grpc.TestingServiceStub(channel)

    # Create a TestRequest message using the loaded TrainResponse
    test_request = model_pb2.TrainResponse(
        model=train_response.model,
        x_train=train_response.x_train,
        y_train=train_response.y_train,
        x_test=train_response.x_test,
        y_test=train_response.y_test,
        dates_train=train_response.dates_train,
        dates_test=train_response.dates_test
    )

    # Make the call
    try:
        logging.info("Sending test request to the server...")
        response = stub.TestModel(test_request)
        logging.info("Received response from the server.")
        #logging.info(f"Test Results: {response.results}")
        return model_pb2.TestResult(
            rmse=response.rmse,
            plot=response.plot
        )
    except grpc.RpcError as e:
        logging.error(f"gRPC error: {e.code()} - {e.details()}")
        return model_pb2.TestResult()

if __name__ == '__main__':
    run()
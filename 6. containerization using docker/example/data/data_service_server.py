from concurrent import futures
import grpc
import model_pb2_grpc
import model_pb2
from data_service import clean_data
import io
import os
from app import run_app
import threading
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler()  # Output to the console
    ]
)

class DataServiceServicer(model_pb2_grpc.DataServiceServicer):
    def __init__(self):
        self.dataset_filepath = 'uploaded_file.csv'

    def CleanData(self, request, context):
        logging.info("Cleaning data...")
        try:

            if not os.path.isfile(self.dataset_filepath):
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Dataset file not found")
                return model_pb2.CleanedData()
            
            # Clean data
            x_train, x_test, y_train, y_test, dates_train, dates_test = clean_data(self.dataset_filepath)

            if len(x_train) != len(y_train):
                raise ValueError("x_train and y_train have different lengths")
            
            response = model_pb2.CleanedData(
                x_train=x_train,
                y_train=y_train,
                x_test=x_test,
                y_test=y_test,
                dates_train=dates_train,
                dates_test=dates_test
            )
            
            # Return cleaned data along with the result of training
            logging.info("Data cleaned successfully.")
            return response
        
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return model_pb2.CleanedData()

def start_flask_app():
    run_app()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_DataServiceServicer_to_server(DataServiceServicer(), server)
    port = 8061
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()
    logging.info("Data service server started on port 8061.")
    threading.Thread(target=start_flask_app).start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

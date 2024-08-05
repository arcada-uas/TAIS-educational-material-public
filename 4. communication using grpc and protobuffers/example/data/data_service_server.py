from concurrent import futures
import grpc
import data_pb2_grpc
import data_pb2
import train_pb2_grpc
import train_pb2
from data_service import clean_data
import io

class DataServiceServicer(data_pb2_grpc.DataServiceServicer):
    def __init__(self):
        # Initialize gRPC channel and stub for TrainingService
        self.training_channel = grpc.insecure_channel('localhost:8081')  # Replace with actual address
        self.training_stub = train_pb2_grpc.TrainingServiceStub(self.training_channel)

    def CleanData(self, request, context):
        try:
            # Read CSV content from the request
            csv_content = request.csv_content
            csv_file = io.BytesIO(csv_content)
            
            # Clean data
            x_train, x_test, y_train, y_test, dates_train, dates_test = clean_data(csv_file)

            if len(x_train) != len(y_train):
                raise ValueError("x_train and y_train have different lengths")
            
            response = data_pb2.CleanedData(
                x_train=x_train,
                y_train=y_train,
                x_test=x_test,
                y_test=y_test,
                dates_train=dates_train,
                dates_test=dates_test
            )
            
            # Call TrainingService directly
            train_response = self.training_stub.TrainModel(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, dates_train=dates_train, dates_test=dates_test)
            
            # Return cleaned data along with the result of training
            return response
        
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return data_pb2.DataResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_pb2_grpc.add_DataServiceServicer_to_server(DataServiceServicer(), server)
    server.add_insecure_port('[::]:8080')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

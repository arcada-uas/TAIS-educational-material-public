import grpc
import train_pb2_grpc
import train_pb2
from training_service import train_model
import logging
from concurrent import futures
import test_pb2_grpc

class TrainingServiceServicer(train_pb2_grpc.TrainingServiceServicer):
    def __init__(self):
        self.testing_channel = grpc.insecure_channel('localhost:8082')
        self.testing_stub = test_pb2_grpc.TestingServiceStub(self.testing_channel)

    def TrainModel(self, request, context):
        try:
            # Train model
            x_train = request.x_train
            y_train = request.y_train
            
            model_binary = train_model(x_train, y_train)
            logging.info("Model trained successfully")

            test_request = train_pb2.TrainResponse(
                model=model_binary,
                x_train=x_train,
                y_train=y_train,
                x_test=request.x_test,
                y_test=request.y_test,
                dates_train=request.dates_train,
                dates_test=request.dates_test
            )
            
            #self.testing_stub.TestModel(test_request)

            return train_pb2.TrainResponse(
                model=model_binary,
                x_train=x_train,
                y_train=y_train,
                x_test=request.x_test,
                y_test=request.y_test,
                dates_train=request.dates_train,
                dates_test=request.dates_test
            )
        
        except Exception as e:
            logging.exception("Error training model")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return train_pb2.TrainResponse()
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    train_pb2_grpc.add_TrainingServiceServicer_to_server(TrainingServiceServicer(), server)
    server.add_insecure_port('[::]:8081')
    server.start()
    print("Training service server started on port 8081.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

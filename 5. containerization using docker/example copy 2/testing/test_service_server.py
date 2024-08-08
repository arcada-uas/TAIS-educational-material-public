import grpc
import model_pb2_grpc
import model_pb2
from concurrent import futures
import pickle
import test_service
from threading import Thread
from app import run_flask 

class TestingServiceServicer(model_pb2_grpc.TestingServiceServicer):
    def TestModel(self, request, context):
        try:
            # Get the model from the binary string
            model_binary = request.model
            model = pickle.loads(model_binary)
            
            # Run the model testing function
            rmse, plot_image_binary = test_service.test_model(model, request.x_test, request.y_test, request.dates_test)
            
            print("Model tested successfully")
            
            # Return both RMSE and plot image binary in the response
            return model_pb2.TestResult(
                rmse=rmse,
                plot=plot_image_binary
            )
        
        except Exception as e:
            print("Error testing model")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return model_pb2.TestResult() 

def run_app():
    run_flask()

def serve():
    flask_thread = Thread(target=run_app)
    flask_thread.start()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_TestingServiceServicer_to_server(TestingServiceServicer(), server)
    server.add_insecure_port('0.0.0.0:8061')
    server.start()
    print("Testing service server started on port 8061.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

import grpc
import test_pb2_grpc
import test_pb2
from test_service import test_model
from concurrent import futures
import pickle
import base64

class TestingServiceServicer(test_pb2_grpc.TestingServiceServicer):
    def TestModel(self, request, context):
        try:
            # Get the model from the binary string
            model_binary = request.model
            model = pickle.loads(model_binary)
            
            # Run the model testing function
            rmse, plot_image_binary = test_model(model, request.x_test, request.y_test, request.dates_test)
            
            print("Model tested successfully")
            
            # Return both RMSE and plot image binary in the response
            return test_pb2.TestResponse(
                rmse=rmse,
                plot=plot_image_binary
            )
        
        except Exception as e:
            print("Error testing model")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return test_pb2.TestResponse()
        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_TestingServiceServicer_to_server(TestingServiceServicer(), server)
    server.add_insecure_port('[::]:8082')
    server.start()
    print("Testing service server started on port 8082.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

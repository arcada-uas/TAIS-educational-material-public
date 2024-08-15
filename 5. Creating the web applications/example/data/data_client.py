import grpc
import model_pb2_grpc
import model_pb2


def run():
    with grpc.insecure_channel('localhost:8061') as channel:
        stub = model_pb2_grpc.DataServiceStub(channel)
        
        try:
            # Read CSV file content as bytes
            # Create request with CSV content
            empty_message = model_pb2.Empty()
            
            # Call the CleanData method
            response = stub.CleanData(empty_message)

            if response.x_train and response.x_test and response.y_train and response.y_test and response.dates_train and response.dates_test:
                print("x_trian:", response.x_train)
                print("x_test:", response.x_test)
                print("y_train:", response.y_train)
                print("y_test:", response.y_test)
                print("Dates Train:", response.dates_train)
                print("Dates Test:", response.dates_test)
            else:
                print("No data returned or some fields are empty.")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")


if __name__ == '__main__':
    run()

# data_service_server.py

from concurrent import futures
import grpc
import data_pb2_grpc
import data_pb2
import pandas as pd
from data_service import clean_data
import os
import io
import logging

class DataServiceServicer(data_pb2_grpc.DataServiceServicer):
    def CleanData(self, request, context):
        try:
            # Read CSV content from the request
            csv_content = request.csv_content
            csv_file = io.BytesIO(csv_content)
            
            print("Received CSV data, cleaning...")
            # Clean data
            x_train, x_test, y_train, y_test, dates_train, dates_test = clean_data(csv_file)
            print("Data cleaned successfully")

            print(x_train, x_test, y_train, y_test, dates_train, dates_test)

            print("Returning data to client")
            return data_pb2.DataResponse(
                x_train=x_train,
                x_test=x_test,
                y_train=y_train,
                y_test=y_test,
                dates_train=dates_train,
                dates_test=dates_test
            )
        except Exception as e:
            logging.exception("Error cleaning data")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return data_pb2.DataResponse()


def serve():
    print("in serve function")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_pb2_grpc.add_DataServiceServicer_to_server(DataServiceServicer(), server)
    server.add_insecure_port('[::]:8080')
    server.start()
    print("Data service server started on port 8080.", flush=True)
    server.wait_for_termination()



if __name__ == '__main__':
    print("in main", flush=True)
    serve()

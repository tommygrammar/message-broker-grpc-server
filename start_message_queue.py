import grpc
import queue_pb2
import queue_pb2_grpc
import time

def start_queue(queue_name):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = queue_pb2_grpc.QueueServiceStub(channel)
        response = stub.StartQueue(queue_pb2.StartQueueRequest(queue_name=queue_name))
        print(f'StartQueue response: {response.status}')

if __name__ == '__main__':
    while True:
        queue_name = "Chainsaw Man"
        start_queue(queue_name)
        print('Queue started. Waiting for next command...')
        time.sleep(10)  

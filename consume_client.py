import grpc
import queue_pb2
import queue_pb2_grpc

def deserialize_message(message_bytes):
    # Deserialize the message bytes to string
    return message_bytes.decode("utf-8")

def consume_queue(queue_name):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = queue_pb2_grpc.QueueServiceStub(channel)
        request = queue_pb2.ConsumeQueueRequest(queue_name=queue_name)

        try:
            for response in stub.ConsumeQueue(request):
                if response.message:
                    message = deserialize_message(response.message)  
                    print(f'Received message: {message}')
                else:
                    print('No message received.')
        except grpc.RpcError as e:
            print(f'An error occurred: {e.details()}')

if __name__ == '__main__':
    queue_name = "Chainsaw Man"
    consume_queue(queue_name)

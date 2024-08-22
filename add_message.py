import grpc
import queue_pb2
import queue_pb2_grpc

def serialize_message(message):
    # Serialize the message to bytes
    return message.encode("utf-8")  

def add_message(queue_name, payload):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = queue_pb2_grpc.QueueServiceStub(channel)
        serialized_message = serialize_message(payload)
        response = stub.AddMessage(queue_pb2.AddMessageRequest(
            queue_name=queue_name,
            message=serialized_message
        ))
        print(f'Status: {response.status}')

if __name__ == '__main__':
    queue_name = "Chainsaw Man"

    while True:
        payload = input('Enter the message payload (or type "exit" to quit): ')
        if payload.lower() == 'exit':
            print('Exiting...')
            break
        add_message(queue_name, payload)

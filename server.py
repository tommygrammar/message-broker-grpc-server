from concurrent import futures
import grpc
import queue_pb2, queue_pb2_grpc
import time

# In-memory dictionary to store queues
queues = {}

class QueueService(queue_pb2_grpc.QueueServiceServicer):

    def StartQueue(self, request, context):
        queue_name = request.queue_name
        if queue_name not in queues:
            queues[queue_name] = []
            return queue_pb2.StartQueueResponse(status=f"Queue '{queue_name}' started.")
        else:
            return queue_pb2.StartQueueResponse(status=f"Queue '{queue_name}' already exists.")

    def AddMessage(self, request, context):
        queue_name = request.queue_name
        message_bytes = request.message
        # Deserialize the message
        message = message_bytes.decode("utf-8")  

        if queue_name in queues:
            queues[queue_name].append(message_bytes)  # Append as bytes
            return queue_pb2.AddMessageResponse(status="Message added to the queue.")
        else:
            return queue_pb2.AddMessageResponse(status=f"Queue '{queue_name}' does not exist.")

    def ConsumeQueue(self, request, context):
        queue_name = request.queue_name
        if queue_name in queues:
            while True:
                if queues[queue_name]:
                    message_bytes = queues[queue_name].pop(0)
                    yield queue_pb2.ConsumeQueueResponse(message=message_bytes)
                else:
                    time.sleep(1)  # Wait before checking again
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Queue '{queue_name}' not found.")
            return

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    queue_pb2_grpc.add_QueueServiceServicer_to_server(QueueService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

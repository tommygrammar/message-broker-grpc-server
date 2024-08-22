was working on a kind of message broker which I could use on my arhitecture and i found this idea to be so good..

Still developing it but it should work alright. The goal is it working for micro services architecture

run server.py to start the gRPC server

then in start_message_queue.py, go choose the name of the queue, I have sent it to default as "Chainsaw Man"

add_message basically sends messages to the queue of your choice

consume_client receives the messages from the queue of your choice and displays them

and the proto file is important, understand it

will be adding more features but do feel free to contribute to it

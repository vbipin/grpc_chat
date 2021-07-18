#Chat Server
#code copied and modified from : https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_server.py
from concurrent import futures

import grpc

import chat_pb2
import chat_pb2_grpc

from chat_pb2 import Status, User, Packet


class Chat(chat_pb2_grpc.ChatServicer):

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)
    
    def add_user(self, request, context):
        """Adds a new user to the server
        """
        return Status(packets=92)


    def del_user(self, request, context):
        """Deletes a user
        """
        return Status(packets=0)

    def get_status(self, request, context):
        """Get status
        """
        return Status(packets=0)

    def send_msg(self, request, context):
        """Sends a message to the server
        """
        return Status(packets=0)

    def get_msg(self, request, context):
        """Read one msg from the server
        """
        return Packet(name='1')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(Chat(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()


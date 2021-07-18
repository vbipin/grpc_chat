from __future__ import print_function

import grpc

import chat_pb2
import chat_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chat_pb2_grpc.ChatStub(channel)
        response = stub.add_user(chat_pb2.User(name='you'))
    print("Greeter client received: ", response.packets)


if __name__ == '__main__':
    run()
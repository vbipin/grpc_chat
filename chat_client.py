from __future__ import print_function

import grpc

import chat_pb2
import chat_pb2_grpc

from chat_pb2 import Status, User, Packet

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chat_pb2_grpc.ChatStub(channel)
        response = stub.add_user(User(name='you'))
        print("received status: ", response.packets)
        
        response = stub.send_msg(Packet(name='you'))
        print("received status: ", response.packets)
        
        response = stub.get_msg(User(name='you'))
        print("received msg: ", response)
        
        response = stub.del_user(User(name='you'))
        print("received status: ", response.packets)
        

if __name__ == '__main__':
    run()
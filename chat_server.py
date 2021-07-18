#Chat Server
#code copied and modified from : https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_server.py
from concurrent import futures

import grpc

import chat_pb2
import chat_pb2_grpc

from chat_pb2 import Status, User, Packet


class Chat(chat_pb2_grpc.ChatServicer):
    
    def add_user(self, request, context):
        """Adds a new user to the server
        """
        username =  request.name
        store_add_user( username )
        return Status(packets=num_pending_messages(username))


    def del_user(self, request, context):
        """Deletes a user
        """
        username =  request.name
        store_del_user( username )
        return Status(packets=0)

    def get_status(self, request, context):
        """Get status
        """
        username =  request.name
        return Status(packets=num_pending_messages(username))

    def send_msg(self, request, context):
        """Sends a message to the server
        """
        username =  request.name
        msg = request
        store_put_msg( msg )
        return Status(packets=num_pending_messages(username))

    def get_msg(self, request, context):
        """Read one msg from the server
        """
        username =  request.name
        msg = store_get_msg( username )
        #return Packet(name='1')
        return msg #this is of type Packet


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(Chat(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
    
    
####### APP specific code
##############################################################################
#We need a message store to keep all the messages
#We also need a user store to keep track of the logged in users. 
#It will also store the index of the next expected message

MAX_MSGS = 1024
msg_store = []
users = { }  #uid : next msg ptr

def store_add_user(username) :
    users[username] = 0 #last msg index read
    
def store_del_user(username):
    if username in users:
        del users[username]
        store_cleanup()
        
def num_pending_messages(username):
    if len(msg_store) == 0 :
        return 0
    #else we count from current index to end of msg_store
    return len(msg_store) - users[username]  #this will give the pending messages
           
def store_put_msg( msg ):
    msg_store.append(msg)
    
    
def store_cleanup():
    #we find the min user pointer and purge up to that
    if not users : #we can purge all
        #msg_store = []
        return 
    
    min_index = min(users.values())
    if min_index == 0 : #nothing to do
        return
    
    #adjust the indexs
    for _ in range(min_index):
        msg_store.pop(0) #just remove from the back
        
    for username in users :
        users[username] -= min_index
        
        
def store_get_msg( username ) :
    """returns none if cannot get msg"""
    store_cleanup()
    index_to_read = users[username]
    if index_to_read >= len(msg_store) :
        return None
    msg = msg_store[ index_to_read ]
    users[username] += 1
    return msg

##############################################################################


if __name__ == '__main__':
    serve()


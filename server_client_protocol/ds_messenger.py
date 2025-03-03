import socket
from server_client_protocol.ds_protocol import *

class DirectMessage:
    def __init__(self, recipient, message, timestamp):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp

class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None   
        self.username = username
        self.dsuserver = dsuserver
        self.password = password
        self.port = '3001'
		
    def send(self, message:str, recipient:str) -> bool:
        # must return true if message successfully sent, false if send failed.
        try: 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, self.port))
                send_file = client.makefile('w')
                recv_file = client.makefile('r')
            
                join_msg = format_join_msg(self.username, self.password)
                send_file.write(join_msg + '\r\n')
                send_file.flush()
                
                resp = recv_file.readline()
                response = extract_json(resp)
                if response.type != "ok":
                    print("Error:", response.message)
                    return False
                
                self.token = response.token

                if message:
                    print(f'Sending message: {message}; Sending to {recipient}')
                    direct_msg = format_direct_msg(self.token, message, recipient)
                    send_file.write(direct_msg + '\r\n')
                    send_file.flush()
    
                    resp = recv_file.readline()
                    response = extract_json(resp)
                    if response.type != "ok":
                        print("Error:", response.message)
                        return False
                    else:
                        print('Message sent Sucessfully!')
        except Exception as e:
            print(f'An Unexpected Error Occcured: {e}')


    def retrieve_messages(self, message_type: str) -> list:
        # must return a list of DirectMessage objects containing all new messages
        try: 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, self.port))
                send_file = client.makefile('w')
                recv_file = client.makefile('r')
            
                join_msg = format_join_msg(self.username, self.password)
                send_file.write(join_msg + '\r\n')
                send_file.flush()
                
                resp = recv_file.readline()
                response = extract_json(resp)
                if response.type != "ok":
                    print("Error:", response.message)
                    return []
                
                self.token = response.token

                request_msg = format_msg_request(self.token, message_type)
                print(f'Finding New Messages for {self.username}')

                send_file.write(request_msg +'\r\n')
                send_file.flush()

                resp = recv_file.readline()

                messages = extract_direct_message(resp)
                
                if messages:
                    directmessages = []
                    for msg in messages:
                        ds = DirectMessage(recipient=msg['from'], message = msg['message'], timestamp= msg['timestamp'])
                        directmessages.append(ds)
                    
                    return directmessages
                else: 
                    return []

        except Exception as e:
            print(f'An Unexpected Error occured: {e}')

 
    def retrieve_all(self) -> list:
        # must return a list of DirectMessage objects containing all messages
        return self.retrieve_messages('all')
    
    def retrieve_new(self) -> list:
        # must return a list of DirectMessage objects containing all new messages
        return self.retrieve_messages('new')




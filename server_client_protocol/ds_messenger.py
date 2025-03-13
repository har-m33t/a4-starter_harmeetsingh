import socket
import json
import datetime

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server_client_protocol.ds_protocol import *

class DirectMessage:
    def __init__(self, sender, message, timestamp, from_user):
        self.sender = sender
        self.message = message
        self.timestamp = timestamp
        self._from_user = from_user

class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None   
        self.username = username
        self.dsuserver = dsuserver
        self.password = password
        self.port = 3001
        
    def send(self, message: str, recipient: str) -> bool:
        """ Sends a direct message to a recipient. Returns True if successful, False otherwise. """
        try: 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, self.port))
                send_file = client.makefile('w')
                recv_file = client.makefile('r')
            
                # Authenticate user
                join_msg = format_join_msg(self.username, self.password)
                send_file.write(join_msg + '\r\n')
                send_file.flush()
                
                resp = recv_file.readline().strip()
                response = extract_json(resp)
                if response.type != "ok":
                    print("Error:", response.message)
                    return False
                
                self.token = response.token

                # Send direct message
                if message:
                    timestamp = str(datetime.datetime.now().timestamp())  # Generate timestamp
                    print(f'Sending message: "{message}" to {recipient}')
                    
                    direct_msg = format_direct_msg(token = self.token, direct_msg=message, recipient=recipient, timestamp=timestamp)

                    send_file.write(direct_msg + '\r\n')

                    send_file.flush()

                    resp = recv_file.readline().strip()

                    response = extract_json(resp)

                    if response.type != "ok":
                        print("Error:", response.message)
                        return False
                    else:
                        print("Message sent successfully!")
                        return True
                        
        except Exception as e:
            print(f'An unexpected error occurred: {e}')
            return False
        

    def retrieve_messages(self, message_type: str) -> list:
        """ Retrieves messages of the specified type ('new' or 'all'). """
        try: 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, self.port))
                send_file = client.makefile('w')
                recv_file = client.makefile('r')
            
                # Authenticate user
                join_msg = format_join_msg(self.username, self.password)
                send_file.write(join_msg + '\r\n')
                send_file.flush()
                
                resp = recv_file.readline().strip()
                response = extract_json(resp)
                
                
                if response.type != "ok":
                    print("Error:", response.message)
                    return []
            
                self.token = response.token

                # Request messages
                request_msg = format_msg_request(self.token, message_type)
                
                print(f'Retrieving {message_type} messages for {self.username}')
                send_file.write(request_msg + '\r\n')
                send_file.flush()

                resp = recv_file.readline().strip()
                messages = extract_direct_message(resp)
                
                direct_messages = []
                for msg in messages:
                    if 'recipient' in msg.keys():
                        direct_messages.append(DirectMessage(msg['recipient'], msg['message'], msg['timestamp'], True))
                    elif 'from' in msg.keys():
                        direct_messages.append(DirectMessage(msg['from'], msg['message'], msg['timestamp'], False))
                
                return direct_messages

        except Exception as e:
            print(f'An unexpected error occurred: {e}')
            return []

    def retrieve_all(self) -> list:
        """ Retrieves all messages. """
        return self.retrieve_messages('all')
    
    def retrieve_new(self) -> list:
        """ Retrieves only new messages. """
        return self.retrieve_messages('new')

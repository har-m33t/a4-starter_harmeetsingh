"""
ds_messenger.py

This module provides functionality for sending and retrieving direct messages
using a socket connection to a Distributed Social Universe (DSU) server.

"""
import socket
import datetime
from ds_protocol import extract_direct_message, format_join_msg
from ds_protocol import extract_json, format_direct_msg, format_msg_request


class UnexpectedError(Exception):
    '''
    Catch any Unexpected Errors within the program
    '''


class DirectMessage:
    """
    Represents a direct message with s
    ender, message content, timestamp, and origin information.
    """

    def __init__(self,
                 sender: str,
                 message: str,
                 timestamp: str,
                 from_user: bool
                 ):
        """
        Initialize a DirectMessage object.

        Args:
            sender (str): The sender of the message.
            message (str): The content of the message.
            timestamp (str): The timestamp of the message.
            from_user (bool):
                Whether the message is from the user (True)
                or to the user (False).
        """
        self.sender = sender
        self.message = message
        self.timestamp = timestamp
        self.from_user = from_user

    def print_user_info(self):
        """
        Print Out Direct Message Info
        """
        print('Sender:', self.sender)
        print('Message:', self.message)
        print('Timestamp:', self.timestamp)
        print('From user?:', self.from_user)
        return True

    def dictionary_user_info(self):
        """
        Convert Direct Message into a Dictionary format
        """
        return {
            'sender': self.sender,
            'message': self.message,
            'timestamp': self.timestamp,
            'from_user': self.from_user
        }


class DirectMessenger:
    """
    Handles sending and retrieving direct messages
    using a socket connection to a DSU server.
    """

    def __init__(self,
                 dsuserver: str = None,
                 username: str = None,
                 password: str = None
                 ):
        """
        Initialize a DirectMessenger object.

        Args:
            dsuserver (str): The DSU server address.
            username (str): The username for authentication.
            password (str): The password for authentication.
        """
        self.token = None
        self.username = username
        self.dsuserver = dsuserver
        self.password = password
        self.port = 3001

    def send(self, message: str, recipient: str) -> bool:
        """
        Sends a direct message to a recipient.

        Args:
            message (str): The message content to send.
            recipient (str): The recipient's username.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, self.port))
                send_file = client.makefile('w', encoding='utf-8')
                recv_file = client.makefile('r', encoding='utf-8')

                # Authenticate user
                join_msg = format_join_msg(self.username, self.password)
                send_file.write(join_msg + '\r\n')
                send_file.flush()

                resp = recv_file.readline().strip()
                response = extract_json(resp)

                if response.type != "ok":
                    print("Authentication Error:", response.message)
                    return False

                self.token = response.token

                timestamp = str(
                    datetime.datetime.now().timestamp()
                    )
                print(f'Sending message: "{message}" to {recipient}')

                direct_msg = format_direct_msg(
                    token=self.token,
                    direct_msg=message,
                    recipient=recipient,
                    timestamp=timestamp
                )
                send_file.write(direct_msg + '\r\n')
                send_file.flush()

                resp = recv_file.readline().strip()
                response = extract_json(resp)

                if response.type != "ok":
                    print("Message Sending Error:", response.message)
                    return False

                print("Message sent successfully!")
                return True

        except socket.error as e:
            print(f"Socket error: {e}")

        return False

    def retrieve_messages(self, message_type: str) -> list:
        """
        Retrieves messages of the specified type ('new' or 'all').

        Args:
            message_type (str):
                The type of messages to retrieve ('new' or 'all').

        Returns:
            list: A list of DirectMessage objects.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, self.port))
                send_file = client.makefile('w', encoding='utf-8')
                recv_file = client.makefile('r', encoding='utf-8')

                # Authenticate user
                join_msg = format_join_msg(self.username, self.password)
                send_file.write(join_msg + '\r\n')
                send_file.flush()

                resp = recv_file.readline().strip()
                response = extract_json(resp)

                if response.type != "ok":
                    print("Authentication Error:", response.message)
                    return []

                self.token = response.token

                # Request messages
                request_msg = format_msg_request(self.token, message_type)
                print(f'Retrieving {message_type} messages')
                print(f'for {self.username}')
                send_file.write(request_msg + '\r\n')
                send_file.flush()

                resp = recv_file.readline().strip()
                messages = extract_direct_message(resp)

                direct_messages = []
                for msg in messages:
                    if 'recipient' in msg:
                        dm = DirectMessage(
                            msg['recipient'],
                            msg['message'],
                            msg['timestamp'],
                            True
                            )
                        direct_messages.append(dm)
                    elif 'from' in msg:
                        dm = DirectMessage(
                            msg['from'],
                            msg['message'],
                            msg['timestamp'],
                            False
                            )
                        direct_messages.append(dm)

                return direct_messages

        except socket.error as e:
            print(f"Socket error: {e}")

        return []

    def retrieve_all(self) -> list:
        """
        Retrieves all messages.

        Returns:
            list: A list of all DirectMessage objects.
        """
        return self.retrieve_messages('all')

    def retrieve_new(self) -> list:
        """
        Retrieves only new messages.

        Returns:
            list: A list of new DirectMessage objects.
        """
        return self.retrieve_messages('new')

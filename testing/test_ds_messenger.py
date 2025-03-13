import pytest
import json
import socket

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server_client_protocol.ds_protocol import *
from server_client_protocol.ds_messenger import DirectMessenger, DirectMessage

class ServerNotRunningError(Exception):
    pass

def is_server_running(host = 'localhost', port = 3001, timeout=2) -> bool:
    """Checks if a server is running at the given host and port."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            print('Server Running')
            return True
    except (socket.timeout, ConnectionRefusedError):
        raise ServerNotRunningError('Server must be running to execute tests')

def test_DirectMessage_instance():
    msg = DirectMessage('sender', 'message', 'time_stamp', True)
    assert msg.sender == 'sender'
    assert msg.message == 'message'
    assert msg.timestamp == 'time_stamp'
    assert msg._from_user == True

def test_DirectMessenger_instance():
    direct_msgr = DirectMessenger('localhost', 'test1', 'test1')
    assert direct_msgr.token == None   
    assert direct_msgr.username == 'test1'
    assert direct_msgr.dsuserver == 'localhost'
    assert direct_msgr.password == 'test1'
    assert direct_msgr.port == 3001

def test_DirectMessenger_send():
    
    is_server_running()

    direct_msgr = DirectMessenger('localhost', 'test1', 'test1')
    result = direct_msgr.send('TESTING', 'test2')
    assert result is True

    invalid_direct_msgr = DirectMessenger('localhost', 'test1', 'test2')
    result = invalid_direct_msgr.send('TESTING', 'test2')
    assert result is False

    direct_msgr = DirectMessenger('localhost', 'test1', 'test1')
    result = direct_msgr.send('TESTING', '_test2')
    assert result is False

    invalid_server = DirectMessenger('local_host', 'test1', 'test1')
    result = invalid_server.send('TESTING', 'test2')
    assert result is False

def test_DirectMessenger_retrieve_messages():
    
    is_server_running()
    direct_msgr = DirectMessenger('localhost', 'test1', 'test1')
    all_messages = direct_msgr.retrieve_messages('all')
    assert isinstance(all_messages, list)
    if all_messages:
        assert isinstance(all_messages[0], DirectMessage)

    direct_msgr = DirectMessenger('localhost', 'test1', 'test1')
    new_messages = direct_msgr.retrieve_messages('new')
    assert isinstance(new_messages, list)
    if new_messages:
        assert isinstance(new_messages[0], DirectMessage)
    

def test_DirectMessenger_retrieve_all():
    
    direct_msgr = DirectMessenger('localhost', 'test1', 'test1')
    all_messages = direct_msgr.retrieve_all()
    assert isinstance(all_messages, list)
    if all_messages:
        assert isinstance(all_messages[0], DirectMessage)

def test_DirectMessenger_retrieve_new():
    
    direct_msgr = DirectMessenger('localhost', 'test1', 'test1')
    new_messages = direct_msgr.retrieve_new()
    assert isinstance(new_messages, list)
    if new_messages:
        assert isinstance(new_messages[0], DirectMessage)

def test_DirectMessenger_retrieve_messages_invalid_profile():
    
    direct_msgr = DirectMessenger('localhost', '_test1', 'test1')
    messages = direct_msgr.retrieve_messages('all')
    assert messages == []

def test_DirectMessenger_retrieve_messages_invalid_password():

    direct_msgr = DirectMessenger('localhost', 'test1', '_test1')
    messages = direct_msgr.retrieve_messages('all')
    assert messages == []

def test_DirectMessenger_retrieve_messages_invalid_server():

    direct_msgr = DirectMessenger('local_host', 'test1', 'test1')
    messages = direct_msgr.retrieve_messages('all')
    assert messages == []
        
'''
pytest testing/test_ds_messenger.py

coverage run -m pytest

coverage report -m
'''
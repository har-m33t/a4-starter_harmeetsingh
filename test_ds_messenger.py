"""
test_ds_messenger.py

This module contains unit tests
for the DirectMessenger and DirectMessage classes
in the ds_messenger module.

"""

import socket
from ds_messenger import DirectMessenger, DirectMessage


class ServerNotRunningError(Exception):
    """
    Custom exception raised when the server is not running.
    """


def is_server_running(host='localhost', port=3001, timeout=2) -> bool:
    """
    Checks if a server is running at the given host and port.

    Args:
        host (str): The server hostname. Defaults to 'localhost'.
        port (int): The server port. Defaults to 3001.
        timeout (int): The connection timeout in seconds. Defaults to 2.

    Returns:
        bool: True if the server is running, False otherwise.

    Raises:
        ServerNotRunningError: If the server is not running.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            print('Server Running')
            return True
    except (socket.timeout, ConnectionRefusedError) as exc:
        raise ServerNotRunningError(
            'Server must be running to execute tests'
            ) from exc


def test_direct_message_instance():
    """
    Test the DirectMessage class
    to ensure it initializes and behaves correctly.
    """
    msg = DirectMessage('sender', 'message', 'time_stamp', True)
    assert msg.sender == 'sender'
    assert msg.message == 'message'
    assert msg.timestamp == 'time_stamp'
    assert msg.from_user is True

    assert msg.print_user_info() is True
    assert msg.dictionary_user_info() == {
        'sender': 'sender',
        'message': 'message',
        'timestamp': 'time_stamp',
        'from_user': True,
    }


def test_direct_messenger_instance():
    """
    Test the DirectMessenger class to ensure it initializes correctly.
    """
    direct_msgr = DirectMessenger('localhost', 'test1', 'test1')
    assert direct_msgr.token is None
    assert direct_msgr.username == 'test1'
    assert direct_msgr.dsuserver == 'localhost'
    assert direct_msgr.password == 'test1'
    assert direct_msgr.port == 3001


def test_direct_messenger_send():
    """
    Test the DirectMessenger send method to ensure it sends messages correctly.
    """
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

    invalid_msg = DirectMessenger('local_host', 'test1', 'test1')
    result = invalid_msg.send(None, 'test2')
    assert result is False


def test_direct_messenger_retrieve_messages():
    """
    Test the DirectMessenger retrieve_messages method
    to ensure it retrieves messages correctly.
    """
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


def test_direct_messenger_retrieve_all():
    """
    Test the DirectMessenger retrieve_all method
    to ensure it retrieves all messages correctly.
    """
    direct_msgr = DirectMessenger('localhost', 'test1', 'test1')
    all_messages = direct_msgr.retrieve_all()
    assert isinstance(all_messages, list)
    if all_messages:
        assert isinstance(all_messages[0], DirectMessage)


def test_direct_messenger_retrieve_new():
    """
    Test the DirectMessenger retrieve_new method
    to ensure it retrieves new messages correctly.
    """
    direct_msgr = DirectMessenger('localhost', 'test1', 'test1')
    new_messages = direct_msgr.retrieve_new()
    assert isinstance(new_messages, list)
    if new_messages:
        assert isinstance(new_messages[0], DirectMessage)


def test_direct_messenger_retrieve_messages_invalid_profile():
    """
    Test the DirectMessenger retrieve_messages method with an invalid profile.
    """
    direct_msgr = DirectMessenger('localhost', '_test1', 'test1')
    messages = direct_msgr.retrieve_messages('all')
    assert not messages


def test_direct_messenger_retrieve_messages_invalid_password():
    """
    Test the DirectMessenger retrieve_messages method with an invalid password.
    """
    direct_msgr = DirectMessenger('localhost', 'test1', '_test1')
    messages = direct_msgr.retrieve_messages('all')
    assert not messages


def test_direct_messenger_retrieve_messages_invalid_server():
    """
    Test the DirectMessenger retrieve_messages method with an invalid server.
    """
    direct_msgr = DirectMessenger('local_host', 'test1', 'test1')
    messages = direct_msgr.retrieve_messages('all')
    assert not messages

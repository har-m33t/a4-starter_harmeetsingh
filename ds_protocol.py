"""
ds_protocol.py

This module provides functions to format and extract JSON messages for
communication with a Distributed Social Universe (DSU) server.

Author: Harmeet Singh
Email: harmees2
Student ID: 27012171
"""

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from JSON messages.
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


def extract_json(json_msg: str) -> DataTuple:
    """
    Takes a JSON string and converts it to a DataTuple object containing
    the type, message, and token extracted from the JSON message.

    Args:
        json_msg (str): A string representing the JSON message to be parsed.

    Returns:
        DataTuple: A namedtuple containing the parsed values
        (type, message, token).
                  Returns None if JSON cannot be decoded.
    """
    try:
        json_obj = json.loads(json_msg)
        response_type = json_obj['response']['type']
        message = json_obj['response']['message']
        if response_type == 'ok':
            try:
                token = json_obj['response']['token']
            except KeyError:
                token = None
        else:
            token = None
        return DataTuple(response_type, message, token)

    except json.JSONDecodeError:
        print("JSON cannot be decoded.")
        return None


def format_join_msg(username: str, password: str) -> str:
    """
    Creates a formatted JSON string
    to join a session with provided credentials.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        str: A JSON string representing the join request.
    """
    return json.dumps({
        "join": {
            "username": username,
            "password": password,
            "token": ""
        }
    })


def format_direct_msg(
        token: str, direct_msg: str, recipient: str, timestamp: str = ''
        ) -> str:
    """
    Creates a formatted JSON string to send a direct message with the provided
    token, message, recipient, and timestamp.

    Args:
        token (str): The authentication token.
        direct_msg (str):
          The content of the message.
        recipient (str):
          The recipient of the message.
        timestamp (str, optional):
          The timestamp of the message. Defaults to ''.

    Returns:
        str: A JSON string representing the direct message request.
    """
    return json.dumps({
        "token": token,
        "directmessage": {
            "entry": direct_msg,
            "recipient": recipient,
            "timestamp": timestamp
        }
    })


def extract_direct_message(json_msg: str) -> list:
    """
    Takes a JSON string and extracts direct messages from it.

    Args:
        json_msg (str):
          A string representing the JSON message to be parsed.

    Returns:
        list: A list of messages.
        Returns an empty list if JSON cannot be decoded
        or is invalid.
    """
    try:
        json_obj = json.loads(json_msg)
        response_type = json_obj['response']['type']
        messages = json_obj['response'].get('messages', [])
        if response_type == 'ok' and messages:
            return messages
        return []

    except json.JSONDecodeError:
        print("JSON cannot be decoded.")
        return []
    except KeyError as key_error:
        print(f"ERROR: Missing key in JSON - {key_error}")
        return []


def format_msg_request(token: str, message_type: str) -> str:
    """
    Creates a formatted JSON string to request messages of a specific type.

    Args:
        token (str): The authentication token.
        message_type (str): The type of messages to request ('new' or 'all').

    Returns:
        str: A JSON string representing the message request.
    """
    return json.dumps({
        "token": token,
        "directmessage": message_type
    })

"""
test_ds_protocol.py

This module contains unit tests for the ds_protocol module.

coverage run -m pytest

coverage report -m

"""

import json
from ds_protocol import extract_json, format_join_msg
from ds_protocol import format_direct_msg, extract_direct_message
from ds_protocol import format_msg_request


def test_extract_json():
    """
    Test the extract_json function to ensure it correctly parses JSON messages.
    """
    json_msg = json.dumps(
        {"response":
         {"type": "ok", "message": "Success", "token": "12345"}}
        )
    result = extract_json(json_msg)
    assert result.type == "ok"
    assert result.message == "Success"
    assert result.token == "12345"

    json_msg = json.dumps(
        {"response":
         {"type": "error", "message": "Failure"}
         })
    result = extract_json(json_msg)
    assert result.type == "error"
    assert result.message == "Failure"
    assert result.token is None

    json_msg = '{"response": "type": "ok", "message":'
    result = extract_json(json_msg)
    assert result is None

    json_msg = json.dumps(
        {"response":
         {"type": "ok", "message": "Success"}
         })
    result = extract_json(json_msg)
    assert result.token is None
    assert result.type == "ok"
    assert result.message == "Success"


def test_format_join_msg():
    """
    Test the format_join_msg function to
    ensure it correctly formats join messages.
    """
    result = format_join_msg("user", "pass")
    expected = {"join": {"username": "user", "password": "pass", "token": ""}}
    assert json.loads(result) == expected


def test_format_direct_msg():
    """
    Test the format_direct_msg function
    to ensure it correctly formats direct messages.
    """
    result = format_direct_msg("token123", "Hello", "user2", "2025-03-02")
    expected = {
        "token": "token123",
        "directmessage":
        {"entry": "Hello", "recipient": "user2", "timestamp": "2025-03-02"}
    }
    assert json.loads(result) == expected


def test_extract_direct_message():
    """
    Test the extract_direct_message function
    to ensure it correctly extracts direct messages.
    """
    json_msg = json.dumps({
        "response": {
            "type": "ok",
            "messages": [
                {"from": "user1", "entry": "Hello", "timestamp": "2025-03-02"},
                {"from": "user2", "entry": "Hi", "timestamp": "2025-03-03"}
            ]
        }
    })
    result = extract_direct_message(json_msg)
    assert len(result) == 2
    assert result[0]["from"] == "user1"
    assert result[1]["entry"] == "Hi"

    json_msg = json.dumps({
        "response": {
            "type": "error",
            "messages": []
        }
    })
    result = extract_direct_message(json_msg)
    assert not result

    json_msg = json.dumps({
        "response": {
            "type": "error"
        }
    })
    result = extract_direct_message(json_msg)
    assert not result

    json_msg = '"response": {"type": "ok","messages":'
    result = extract_direct_message(json_msg)
    assert not result

    json_msg = json.dumps({
        "response": {
            "messages": [
                {"from": "user1", "entry": "Hello", "timestamp": "2025-03-02"},
                {"from": "user2", "entry": "Hi", "timestamp": "2025-03-03"}
            ]
        }
    })
    result = extract_direct_message(json_msg)
    assert not result


def test_format_msg_request():
    """
    Test the format_msg_request function to
    ensure it correctly formats message requests.
    """
    result = format_msg_request("token123", "new")
    expected = {"token": "token123", "directmessage": "new"}
    assert json.loads(result) == expected

import pytest
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server_client_protocol.ds_protocol import *

# Test extract_json
def test_extract_json():
    json_msg = json.dumps({"response": {"type": "ok", "message": "Success", "token": "12345"}})
    result = extract_json(json_msg)
    assert result.type == "ok"
    assert result.message == "Success"
    assert result.token == "12345"
    
    json_msg = json.dumps({"response": {"type": "error", "message": "Failure"}})
    result = extract_json(json_msg)
    assert result.type == "error"
    assert result.message == "Failure"
    assert result.token is None

    json_msg = '{"response": "type": "ok", "message": "Success", "token": ""}}' # FAULTY JSON MSG
    result = extract_json(json_msg)
    assert result is None

    json_msg = json.dumps({"response": {"type": "ok", "message": "Success"}})
    result = extract_json(json_msg)
    assert result.token is None
    assert result.type == "ok"
    assert result.message == "Success"

# Test format_join_msg
def test_format_join_msg():
    result = format_join_msg("user", "pass")
    expected = {"join": {"username": "user", "password": "pass", "token": ""}}
    assert json.loads(result) == expected

# Test format_post_msg
def test_format_post_msg():
    result = format_post_msg("token123", "Hello world", "2025-03-02")
    expected = {"token": "token123", "post": {"entry": "Hello world", "timestamp": "2025-03-02"}}
    assert json.loads(result) == expected

# Test format_bio_msg
def test_format_bio_msg():
    result = format_bio_msg("token123", "New bio", "2025-03-02")
    expected = {"token": "token123", "bio": {"entry": "New bio", "timestamp": "2025-03-02"}}
    assert json.loads(result) == expected

# Test format_direct_msg
def test_format_direct_msg():
    result = format_direct_msg("token123", "Hello", "user2", "2025-03-02")
    expected = {"token": "token123", "directmessage": {"entry": "Hello", "recipient": "user2", "timestamp": "2025-03-02"}}
    assert json.loads(result) == expected

# Test extract_direct_message
def test_extract_direct_message():
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
    assert result == []

    json_msg = json.dumps({
        "response": {
            "type": "error"
            }
    })
    result = extract_direct_message(json_msg)
    assert result == []
    
    json_msg = '"response": {"type": "ok","messages": ["from": "user1", "entry": "Hello", "timestamp": "2025-03-02"},{"from": "user2", "entry": "Hi", "timestamp": "2025-03-03"}]}'
    result = extract_direct_message(json_msg)
    assert result == []
    



# Test format_msg_request
def test_format_msg_request():
    result = format_msg_request("token123", "new")
    expected = {"token": "token123", "directmessage": "new"}
    assert json.loads(result) == expected

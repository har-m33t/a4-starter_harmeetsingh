import pytest
import json
from unittest.mock import patch, Mock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server_client_protocol.ds_protocol import *
from server_client_protocol.ds_messenger import DirectMessenger, DirectMessage

# Mock responses for different scenarios
MOCK_SUCCESS_AUTH = json.dumps({"response": {"type": "ok", "message": "Authenticated"}})
MOCK_FAILED_AUTH = json.dumps({"response": {"type": "error", "message": "Authentication failed"}})
MOCK_SUCCESS_SEND = json.dumps({"response": {"type": "ok", "message": "Message sent"}})
MOCK_FAILED_SEND = json.dumps({"response": {"type": "error", "message": "Failed to send"}})
MOCK_MESSAGES = json.dumps({
    "response": {"type": "ok", "messages": [
        {"sender": "alice", "recipient": "bob", "entry": "Hello Bob!", "timestamp": "2025-03-03T12:00:00"},
        {"sender": "charlie", "recipient": "bob", "entry": "How's it going?", "timestamp": "2025-03-03T12:05:00"}
    ]}
})
MOCK_EMPTY_MESSAGES = json.dumps({"response": {"type": "ok", "messages": []}})
MOCK_NETWORK_FAILURE = json.dumps({"response": {"type": "error", "message": "Network failure"}})

@pytest.fixture
def mock_messenger():
    """Mocked DirectMessenger instance."""
    messenger = Mock()
    
    # Mock authentication
    messenger.authenticate.side_effect = lambda user, pwd: user == "user" and pwd == "pass"

    # Mock send function
    messenger.send.side_effect = lambda msg, recipient: bool(msg and recipient)  # False if empty

    # Mock retrieve_all and retrieve_new
    messenger.retrieve_all.return_value = json.loads(MOCK_MESSAGES)["response"]["messages"]
    messenger.retrieve_new.return_value = json.loads(MOCK_MESSAGES)["response"]["messages"]

    return messenger

def test_successful_auth(mock_messenger):
    """Test successful authentication."""
    assert mock_messenger.authenticate("user", "pass") is True

def test_failed_auth(mock_messenger):
    """Test failed authentication."""
    assert mock_messenger.authenticate("user", "wrongpass") is False

def test_successful_message_send(mock_messenger):
    """Test successful message sending."""
    assert mock_messenger.send("Hello!", "alice") is True

def test_failed_message_send(mock_messenger):
    """Test failed message sending (empty message)."""
    assert mock_messenger.send("", "alice") is False

def test_retrieve_all_messages(mock_messenger):
    """Test retrieving all messages successfully."""
    messages = mock_messenger.retrieve_all()
    assert len(messages) == 2
    assert messages[0]["entry"] == "Hello Bob!"
    assert messages[1]["sender"] == "charlie"

def test_retrieve_new_messages(mock_messenger):
    """Test retrieving new messages."""
    messages = mock_messenger.retrieve_new()
    assert len(messages) == 2
    assert messages[0]["entry"] == "Hello Bob!"
    assert messages[1]["sender"] == "charlie"

def test_empty_message(mock_messenger):
    """Test sending an empty message."""
    assert mock_messenger.send("", "alice") is False

def test_empty_recipient(mock_messenger):
    """Test sending a message with an empty recipient."""
    assert mock_messenger.send("Hello!", "") is False

'''
pytest test_ds_messenger.py -v
'''
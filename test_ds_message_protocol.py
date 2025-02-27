import unittest
import json
from collections import namedtuple
from ds_protocol import format_direct_msg, extract_direct_message

DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])

class TestDirectMessageFucntions(unittest.TestCase):

    def test_format_direct_msg_valid(self): 
        token = "abc123"
        direct_msg = "Hello!"
        recipient = "user42"
        timestamp = "2025-02-27T12:34:56Z"
        excpected = {
            "token": token, 
            "direct_message": {
                'entry': direct_msg, 
                "recipient": recipient,
                "timestamp": timestamp
            }
        }

        self.assertEqual(json.loads(format_direct_msg(token, direct_msg, recipient, timestamp)), excpected)
    
    def test_format_direct_msg_without_timestamp(self):
        token = "abc123"
        direct_msg = "Hello!"
        recipient = "user42"
        excpected = {
            "token": token, 
            "direct_message": {
                'entry': direct_msg, 
                "recipient": recipient,
                "timestamp": ""
            }
        }
        
        self.assertEqual(json.loads(format_direct_msg(token, direct_msg, recipient)), excpected)

    
    def test_extract_direct_message_valid(self):
        
        json_msg = json.dumps({
            "response": {
                "type": "ok", 
                "token": "secureToken", 
                "messages": [
                    {'from': 'userA', 'content': 'hey'},
                    {'from': 'userB', 'content': 'hello'}
                ]
            }
        })

        expected = {
            'userA': DataTuple("ok", {'from': 'userA', 'content': 'hey'}, "secureToken"), 
            'userB': DataTuple("ok", {"from": 'userB', 'content': 'hello'}, 'secureToken')
        }

        self.assertEqual(extract_direct_message(json_msg), expected)

    def test_extract_direct_message_invalid_message(self):
        
        invalid_json = "{response: {type: 'ok', messages: ["
        
        with self.assertRaises(json.JSONDecodeError):
            extract_direct_message(invalid_json)
            
    def test_extract_direct_message_missing_fields(self):
        json_msg = json.dumps({
            "response": {
                "type": "ok", 
                "messages": []
            }
        })

        expected = {}

        self.assertEqual(extract_direct_message(json_msg), expected)
    
    def test_extract_direct_messsage_error_type(self):
        json_msg = json.dumps({
            "response": {
                "type": "error",
                "messages": [
                    {'from': 'userA', 'content': 'Something went Wrong'}
                ]
            }
        })

        expected = {}

        self.assertEqual(extract_direct_message(json_msg), expected)    

if __name__ == "__main__":
    unittest.main()
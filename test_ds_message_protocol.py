import unittest
import json
from collections import namedtuple
from ds_protocol import format_direct_msg, extract_direct_message

DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])

class TestDirectMessageFucntions(unittest.TestCase):

    def test_format_direct_msg_valid(self): 
        raise NotImplementedError
    
    def test_format_direct_msg_without_timestamp(self):
        raise NotImplementedError
    
    def test_extract_direct_message_valid(self):
        raise NotImplementedError
    
    def test_extract_direct_message_invalid_message(self):
        raise NotImplementedError
    
    def test_extract_direct_message_missing_fields(self):
        raise NotImplementedError
    
    def test_extract_direct_messsage_error_type(self):
        raise NotImplementedError
    

if __name__ == "__main__":
    unittest.main()
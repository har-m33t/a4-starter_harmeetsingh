# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Harmeet Singh
# harmees2
# 27012171

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['type','message', 'token'])

def extract_json(json_msg:str) -> DataTuple[str, str, str]:
  '''
  Takes a JSON string and converts it to a DataTuple object containing
  the type, message, and token extracted from the JSON message.
  
  Args:
    json_msg (str): A string representing the JSON message to be parsed.

  Returns:
    DataTuple: A namedtuple containing the parsed values (type, message, token).
  '''
  try:
    json_obj = json.loads(json_msg)
    type = json_obj['response']['type']
    message = json_obj['response']['message']
    if type == 'ok':
      token = json_obj['response']['token']
    else:
      token = None
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(type, message, token)

def format_join_msg(username: str, password: str) -> str:
    '''
    Creates a formatted JSON string to join a session with provided credentials.
    
    Args:
      username (str): The username of the user.
      password (str): The password of the user.
    
    Returns:
      str: A JSON string representing the join request.
    '''
    return json.dumps({
        "join": {
            "username": username,
            "password": password,
            "token": ""
        }
    })

def format_post_msg(token: str, entry: str, timestamp: str ='') -> str:
  '''
  Creates a formatted JSON string to post an entry with the provided token, entry, and timestamp.
  
  Args:
    token (str): The authentication token.
    entry (str): The content of the post.
    timestamp (str, optional): The timestamp of the post. Defaults to ''.

  Returns:
    str: A JSON string representing the post request.
  '''
  return json.dumps(
    {
      "token": token, 
      "post": {'entry': entry, "timestamp": timestamp}
    }
  )

def format_bio_msg(token: str, bio: str, timestamp: str ='') -> str:
  '''
  Creates a formatted JSON string to post a bio with the provided token, bio, and timestamp.
  
  Args:
    token (str): The authentication token.
    bio (str): The content of the bio.
    timestamp (str, optional): The timestamp of the bio update. Defaults to ''.

  Returns:
    str: A JSON string representing the bio request.
  '''
  return json.dumps(
    {
      "token": token, 
      "bio": {'entry': bio, "timestamp": timestamp}
    }
  )

def format_direct_msg(token: str, direct_msg: str, recipient: str, timestamp: str ='') -> str:
  '''
  Creates a formatted JSON string to post a bio with the provided token, message, recipient and timestamp.
  
  Args:
    token (str): The authentication token.
    direct_msg (str): The content of the bio.
    recipient (str): To whom which will recieve the message
    timestamp (str, optional): The timestamp of the bio update. Defaults to ''.

  Returns:
    str: A JSON string representing the direct message request.
  '''
  return json.dumps(
    {
      'token': token, 
      'direct_message': {
        'entry': direct_msg,
        'recipient': recipient, 
        'timestamp': timestamp 
        }
    }
  )

def extract_direct_message(json_msg: str) -> dict:
    '''
    Takes a JSON string and converts it to a DataTuple object containing
    the type, message, and token extracted from the JSON message. It stores it in a message dictionary, where the key is the person who sent it.

    Args:
        json_msg (str): A string representing the JSON message to be parsed.

    Returns:
        DataTuple: A namedtuple containing the parsed values (type, message, token).
    '''
    
    try:
        json_obj = json.loads(json_msg)
        type = json_obj['response']['type']
        messages = json_obj['response']['messages']
        if type == 'ok':
            token = json_obj['response']['token']
            msg_dict = {}
            for message in messages:
                msg_dict[message["from"]] = DataTuple(type, message, token)
        else:
            token = None
    
        return msg_dict
     
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
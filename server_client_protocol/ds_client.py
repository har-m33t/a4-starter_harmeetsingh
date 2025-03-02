# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME
# EMAIL
# STUDENT ID

import socket
from server_client_protocol.ds_protocol import *

def send(server: str, port: int, username: str, password: str, message: str, bio: str = None) -> bool:
    """
    Establishes a connection to a server, authenticates the user, and sends a message and/or bio update.

    This function uses a TCP socket to connect to a server, authenticate the user using the provided 
    credentials, and send either a message, a bio update, or both. The function ensures proper 
    communication with the server by sending formatted requests and processing server responses.

    Parameters:
        server (str): The hostname or IP address of the server to connect to.
        port (int): The port number of the server.
        username (str): The username for authentication.
        password (str): The password for authentication.
        message (str): The message to be posted.
        bio (str, optional): The bio to be updated. Defaults to None.

    Returns:
        bool: True if the message and/or bio is successfully posted, False otherwise.

    Process:
        1. Establishes a connection to the specified server and port using a TCP socket.
        2. Sends a formatted authentication request using the username and password.
        3. Waits for a server response to verify authentication success.
        4. If authentication is successful, sends a message post request (if provided).
        5. Waits for a response from the server to confirm the message post.
        6. If a bio update is provided, sends a formatted request to update the bio.
        7. Waits for a response from the server to confirm the bio update.
        8. Closes the connection and returns True if all operations are successful.
        9. Returns False if any step fails due to authentication errors, message failures, or exceptions.

    Exceptions:
        - ValueError: Raised when an invalid value is encountered (currently logged as 'yoooo').
        - Exception: Catches unexpected errors and prints the error message.

    Example Usage:
        success = send("example.com", 12345, "user123", "securepassword", "Hello, world!", "Software Engineer")
        if success:
            print("Post and/or bio update successful!")
        else:
            print("Failed to send post or update bio.")
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((server, port))
            send_file = client.makefile('w')
            recv_file = client.makefile('r')

            # Step 1: Join the server
            join_msg = format_join_msg(username, password)
            send_file.write(join_msg + '\r\n')
            send_file.flush()

            # Step 2: Receive response
            resp = recv_file.readline()
            response = extract_json(resp)
            if response.type != "ok":
                print("Error:", response.message)
                return False

            token = response.token

            # Step 3: Send post or bio
            if message:
                print(f'Publishing: {message}')
                post_msg = format_post_msg(token, message)
                send_file.write(post_msg + '\r\n')
                send_file.flush()
                
                resp = recv_file.readline()
                response = extract_json(resp)
                if response.type != "ok":
                    print("Error:", response.message)
                    return False
                else:
                    print('Post published Sucessfully!')

            if bio:
                print(f'Publishing: {bio}')
                bio_msg = format_bio_msg(token, bio)
                send_file.write(bio_msg + '\r\n')
                send_file.flush()
                
                resp = recv_file.readline()
                response = extract_json(resp)
                if response.type != "ok":
                    print("Error:", response.message)
                    return False
                else:
                    print('Bio Published Succesfully!')

            return True
    
    except Exception as e:
        print("An error occurred:", str(e))
        return False
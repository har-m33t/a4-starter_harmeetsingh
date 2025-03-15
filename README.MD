# Assignment 4: Direct Messaging System with GUI

## Overview
This project implements a direct messaging system that allows users to send and receive messages via the DSP platform. The system features a graphical user interface (GUI) built using Tkinter and incorporates networking, local storage, and automated message retrieval.

## Features
- **Direct Messaging**: Users can send and receive messages in real-time.
- **User Authentication**: Secure login to the DSP platform.
- **Message Storage**: Locally saves messages and contacts for offline viewing.
- **GUI Interface**: Interactive Tkinter-based interface with user-friendly navigation.
- **Automated Message Retrieval**: New messages are fetched periodically.


### Running the Program
1. Ensure the server is running on port `3001`.
2. Execute the program using:
```sh
python3 a4.py
```
The GUI should load automatically.

## File Structure
```
|-- a4.py                   # Main application file and GUI implementation using Tkinter
|-- ds_protocol.py          # Handles message formatting and communication
|-- ds_messenger.py         # Manages direct message operations
|-- profile_class.py        # Handles user profile and local message storage
|-- test_ds_protocol.py     # Unit tests for protocol functionality
|-- test_ds_messenger.py    # Unit tests for direct messaging
```

## Usage
### Sending a Message
1. Select a user from the contacts list.
2. Type a message in the input box.
3. Click the 'Send' button.

### Receiving Messages
- New messages automatically appear in the chat window.
- Use the 'Retrieve New' button to manually fetch new messages.

### Offline Mode
- Previously received messages are stored locally and displayed upon startup.
- Sending a message while offline will fail gracefully.

## Testing
To run the unit tests:
```sh
pytest
```
Run coverage analysis:
```sh
coverage run -m pytest
coverage report -m
```

## Development Practices
- **Version Control**: Regular commits using Git.
- **Coding Standards**: Follows PEP8 guidelines.
- **Error Handling**: Gracefully manages connection errors.

## Authors
Developed by Harmeet Singh.

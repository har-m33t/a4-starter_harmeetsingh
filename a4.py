# a3.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# HARMEET SINGH
# HARMEES2@UCI.EDU
# 27012171

# Import Necessary Libraries 
from pathlib import Path
import shlex

# Import Necessary Modules
from Profile import Profile, Post
from ds_client import send
from ui import *
from admin import admin_main


def read_input()-> list:
    """
    Reads and parses user input, handling quotation marks appropriately.

    This function captures user input as a raw string and attempts to tokenize it using `shlex.split`. 
    It determines whether to use POSIX-compatible parsing based on the presence of single (') or double (") 
    quotes in the input. If improper quotation wrapping is detected, an error message is displayed.

    Returns:
        list: A list of parsed input tokens if successful.
        None: If a ValueError occurs due to improper quotation wrapping.

    Exceptions:
        - ValueError: Caught when an input string has improperly wrapped quotations, triggering an error message.

    Example Usage:
        >>> read_input()
        user input: "Hello world" test
        Output: ['Hello world', 'test']
    """
    raw_input = input()
    try: 
        if "'" in raw_input or '"' in raw_input:
            return shlex.split(raw_input, posix= True)
        
        return shlex.split(raw_input, posix=False)
    except ValueError:
        print('ERROR: IMPROPER QUOTATION WRAPPING')
        return None


def split_input(command_line: str) -> list:
    """
    Splits a command line string into individual tokens, handling quotations properly.

    This function parses a given command line string and splits it into a list of tokens. If the string contains 
    single (') or double (") quotes, it uses POSIX-compatible parsing; otherwise, it uses the default parsing method.

    Parameters:
        command_line (str): The command line string to be parsed.

    Returns:
        list: A list of parsed tokens if successful.
        None: If a ValueError occurs due to improper quotation wrapping.

    Exceptions:
        - ValueError: Caught when the input string contains improperly wrapped quotations, triggering an error message.

    Example Usage:
        >>> split_input('echo "Hello world" test')
        Output: ['echo', 'Hello world', 'test']
    """
    try: 
        if '"' in command_line or "'" in command_line:
            return shlex.split(command_line, posix= True)
        
        return shlex.split(command_line, posix=False) 
    except ValueError:
        print('ERROR: IMPROPER QUOTATION WRAPPING')
        return None


def validate_file_command(args: list, expected_args: int, check_suffix: bool = True) -> bool:
    """
    Validates common requirements for file commands (Delete, Read).

    This function checks the validity of a file command by performing the following:
    - Verifying that the correct number of arguments is provided.
    - Ensuring the specified file exists.
    - Optionally, checking that the file has a ".dsu" suffix.

    Parameters:
        args (list): The list of arguments passed to the command.
        expected_args (int): The expected number of arguments for the command.
        check_suffix (bool, optional): A flag indicating whether to check for a ".dsu" file suffix. Defaults to True.

    Returns:
        bool: True if all validation checks pass, False otherwise.

    Exceptions:
        - Prints error messages if any validation fails (incorrect number of arguments, file not found, or invalid suffix).

    Example Usage:
        >>> validate_file_command(['delete', 'file.dsu'], 2)
        Output: True  # If the file exists and has the correct suffix.

        >>> validate_file_command(['delete', 'file.txt'], 2)
        Output: ERROR: FILE MUST END WITH .dsu  # If the file doesn't have a .dsu suffix.
    """

    if len(args) != expected_args:
        print(f"ERROR: IMPROPER COMMAND LENGTH ")
        return False
    
    path = Path(args[1])

    if not path.exists():
        print("ERROR: FILE DOES NOT EXIST")
        return False
    if check_suffix and path.suffix != ".dsu":
        print("ERROR: FILE MUST END WITH .dsu")
        return False
    return True


def validate_create(args: list) -> bool:
    """
    Validates requirements for creating a file.

    This function checks if the given arguments for creating a file satisfy the following:
    - The correct number of arguments is provided.
    - The third argument is '-n'.
    - The directory in which the file will be created exists.
    - The file does not already exist.

    Parameters:
        args (list): The list of arguments passed to the command.

    Returns:
        bool: True if all validation checks pass, False otherwise.

    Exceptions:
        - Prints error messages if any validation fails (incorrect argument count, missing '-n', invalid directory, or existing file).

    Example Usage:
        >>> validate_create(['create', 'path/to/directory', '-n', 'newfile.dsu'])
        Output: True  # If the arguments are valid and the directory exists.

        >>> validate_create(['create', 'path/to/directory', '-x', 'newfile.dsu'])
        Output: ERROR MISSING ARGUEMENT -n  # If the third argument is not '-n'.
    """

    if len(args) != 4:
        print(f"ERROR IMPROPER COMMAND LENGTH")
        return False
    if args[2] != "-n":
        print("ERROR MISSING ARGUEMENT -n")
        return False
    path = Path(args[1])
    if not path.is_dir():
        print("ERROR FILEPATH DOES NOT EXIST ")
        return False

    return True


def validate_edit(args: list, profile: Profile=None) -> bool:
    """
    Validates the requirements for editing a profile.

    This function checks if the given arguments for editing a profile meet the following criteria:
    - The first argument is a valid edit command.
    - The correct number of arguments is provided.
    - If deleting a post, it verifies that the post ID is an integer within the valid range.

    Parameters:
        args (list): The list of arguments passed to the edit command.
        profile (Profile, optional): An optional Profile object used to validate the post ID for deletion. Defaults to None.

    Returns:
        bool: True if all validation checks pass, False otherwise.

    Exceptions:
        - Prints error messages if any validation fails (invalid command, incorrect argument count, or invalid post ID).

    Example Usage:
        >>> validate_edit(['-usr', 'newUsername'], profile)
        Output: True  # If the arguments are valid and the profile exists.

        >>> validate_edit(['-delpost', 'invalidID'], profile)
        Output: ERROR: ID MUST BE GREATER THAN 0  # If the post ID is invalid.
    """
    
    valid_options = ['-usr', '-pwd', '-bio', '-addpost','-delpost']

    if args[0] not in valid_options:
        print('ERROR: INVALID EDIT COMMNAND')
        return False
    
    if len(args) != 2:
        print('ERROR IMPROPER COMMAND LENGTH')
        return False 
    
    if args[0] == '-delpost':
        try:
            args[2] = int(args[2])
            assert type(args[2]) is int, "ID MUST BE TYPE INT"
            assert 0 <= args[2], "ID MUST BE GREATER THAN 0"
            assert args[2] < len(profile.get_posts()), 'ID MUST BE IN RANGE'
        except AssertionError as a:
            print(f'ERROR: {a}')
            return False

    return True 


def validate_print(args:list) -> bool:
    """
    Validates the requirements for printing profile information.

    This function checks if the given arguments for printing profile details meet the following:
    - The correct number of arguments is provided.
    - If printing a specific post, it verifies that the post ID is a valid integer.
    - The first argument is one of the allowed options for printing profile details.

    Parameters:
        args (list): The list of arguments passed to the print command.

    Returns:
        bool: True if all validation checks pass, False otherwise.

    Exceptions:
        - Prints error messages if any validation fails (incorrect argument count or invalid ID format).

    Example Usage:
        >>> validate_print(['-posts'], profile)
        Output: True  # If the arguments are valid.

        >>> validate_print(['-post', 'invalidID'], profile)
        Output: ERROR: ID MUST BE A NUMBER  # If the ID is not a valid number.
    """

    if args[0] == '-post':
        if len(args) != 2:
            print('ERROR: IMPROPER ARGUEMENT LENGTH')
            return False
        try: 
            args[1] = int(args[1])
        except ValueError:
            print("ERROR: ID MUST BE A NUMBER")
            return False
    else:
        if len(args) != 1:
            print('ERROR: IMPROPER ARGUEMENT LENGTH')
            return False
    
    valid_options = ['-usr', '-pwd', '-bio', '-posts', '-post', '-all']
    
    if args[0] not in valid_options:
        return False
    
    return True 


def edit_file(args: list, profile: Profile, profile_path: str) -> bool:
    """
    Edits a profile based on the provided command and updates the profile file.

    This function handles various profile edit commands (e.g., updating username, password, bio, adding/removing posts)
    and saves the updated profile to the specified file path.

    Parameters:
        args (list): The list of arguments passed to the edit command, where the first argument specifies the action 
                     (e.g., '-usr', '-pwd', '-bio', '-addpost', '-delpost') and the second argument provides the new value or post ID.
        profile (Profile): The Profile object representing the user profile to be edited.
        profile_path (str): The file path where the profile data should be saved.

    Returns:
        bool: True if the profile was successfully edited and saved, False otherwise.

    Exceptions:
        - Prints error messages if any validation fails (invalid command, missing profile, or empty value).
        - Returns False if the profile or file path is invalid, or if the specified value is empty.

    Example Usage:
        >>> edit_file(['-usr', 'newUsername'], profile, '/path/to/profile')
        Output: True  # If the username is successfully updated.

        >>> edit_file(['-delpost', '1'], profile, '/path/to/profile')
        Output: True  # If the post with ID '1' is successfully deleted.
    """

    if profile is None or profile_path is None:
        print('ERROR: PROFILE/PATH DOES NOT EXIST')
        return False
    
    value = args[1]

    if value.strip() == '':
        print('ERROR: Bio/Post cannot be White Space')
        return False

    if args[0] == '-usr':
        profile.username = value
    elif args[0] == '-pwd':
        profile.password = value
    elif args[0] == '-bio':
        profile.bio = value
    elif args[0] == '-addpost':
        profile.add_post(Post(value))
    elif args[0] == '-delpost':
        profile.del_post(args[1])
    else:
        print('ERROR: INVALID OPTION')

    profile.save_profile(profile_path)

    return True


def print_file(args: list, profile: Profile) -> bool:
    """
    Prints the specified details of a user's profile.

    This function handles various print commands (e.g., printing username, password, bio, posts) and displays
    the requested information from the profile.

    Parameters:
        args (list): The list of arguments passed to the print command, where the first argument specifies 
                     what to print (e.g., '-usr', '-pwd', '-bio', '-posts', '-post', '-all') and, in some cases, 
                     a second argument specifying the post ID.
        profile (Profile): The Profile object representing the user profile whose information is to be printed.

    Returns:
        bool: True if the profile information was successfully printed, False otherwise.

    Exceptions:
        - Prints error messages if any validation fails (invalid command, missing profile, or invalid post ID).
        - Returns False if the profile does not exist or if the ID provided is not a valid post ID.

    Example Usage:
        >>> print_file(['-usr'], profile)
        Output: Username: user123  # Prints the username.

        >>> print_file(['-post', '2'], profile)
        Output: Post 2: This is a post entry.  # Prints the post with ID '2'.
    """
    
    print()

    if not profile:
        print('ERROR: PROFILE DOES NOT EXIST')
    
    if args[0] == '-usr':
        print(f'Username: {profile.username}')
    
    elif args[0] == '-pwd':
        print(f'Password: {profile.password}')
    
    elif args[0] == '-bio':
        print(f'Bio: {profile.bio}')
    
    elif args[0] == '-posts':
        posts = profile.get_posts()
        for i, post in enumerate(posts):
            print(f"Post {i}: {post['entry']}")
    
    elif args[0] == '-post':
        try:
            posts = profile.get_posts()
            ID = int(args[1])
            assert 0 <= ID
            assert ID < len(posts)
        except ValueError:
            print('ERROR: ID IS NOT A NUMBER')
            return False
        except IndexError:
            print("ERROR: NO ID GIVEN ")
            return False
        except AssertionError as a:
            print(f'ERROR: ID NOT IN RANGE')
            return False
        except Exception as e:
            print(f'ERROR: {e}')
            return False
        print(f"Post {ID}: {posts[ID]['entry']}") 
    
    elif args[0] == '-all':
        print('Username:', profile.username)
        print('Password:', profile.password)
        print('Bio:', profile.bio)
        posts = profile.get_posts()
        for i, post in enumerate(posts):
            print(f"Post {i}: {post['entry']}")
    
    print()
    return True


def create_file(args: list) -> tuple[Profile, str]:
    """
    Creates a new profile file and saves it, or opens an existing profile file if the path already exists.

    This function handles creating a new file in the specified directory with a .dsu extension (if not already provided),
    gathers user input for profile details (username, password, bio), and saves the profile. If the file already exists,
    it opens the existing profile instead.

    Parameters:
        args (list): The list of arguments passed to the create command, where:
                     - args[1] specifies the directory for the new profile file.
                     - args[3] specifies the file name (without extension).
    
    Returns:
        tuple: A tuple containing:
            - Profile: The Profile object for the newly created or opened profile.
            - str: The path to the profile file.

    Exceptions:
        - Prints error messages if any validation fails (e.g., file exists, file not found).
        - Prompts the user for input if creating a new profile.

    Example Usage:
        >>> create_file(['C', 'profiles/', 'newfile.dsu'])
        Output: ('/profiles/newfile.dsu')  # Creates a new file or opens an existing one.
    """

    directory = args[1]
    file_name = args[3]

    if not file_name.endswith(".dsu"):
        file_name += ".dsu"

    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)

    file_path = dir_path / file_name

    if file_path.exists():
        print(f"ERROR: FILE PATH EXISTS")
        print('OPENING FILE INSTEAD')
        file_name = args[3]
        if not file_name.endswith(".dsu"):
            file_name += ".dsu"
        file_path = f'{args[1]}/{file_name}'
        args = ['O', file_path]
        profile, profile_path = open_file(args)
        return profile, profile_path
    else:

        username = input('Enter your username: ')
        
        password = input('Enter your password: ')

        dsuserver = input('Enter the server you would like to publish to: ')
        
        if username.strip() != '' and password.strip != '':
            user_profile = Profile(username=username, password=password, dsuserver=dsuserver)
        
        bio = input('Enter your bio (optional): ')
        
        if bio.strip() != '':
            user_profile.bio = bio

        file_path.touch()
        
        print(f"{file_path}")

        user_profile.save_profile(file_path)

        return user_profile, file_path


def open_file(args: list) -> tuple[Profile, str]:
    """
    Opens an existing profile file and loads the associated Profile object.

    This function attempts to open the profile file specified in the argument list, load the profile data from it,
    and return the Profile object along with the file path. If the file does not exist or any other exception occurs,
    it returns None.

    Parameters:
        args (list): A list of arguments where:
                     - args[1] specifies the path to the profile file to be opened.
    
    Returns:
        tuple: A tuple containing:
            - Profile: The Profile object loaded from the file, or None if there was an error.
            - str: The path to the profile file, or None if the file doesn't exist or an error occurred.

    Exceptions:
        - Prints error messages if the file is not found or if any exception occurs while loading the profile.

    Example Usage:
        >>> open_file(['O', '/profiles/existingfile.dsu'])
        File /profiles/existingfile.dsu loaded successfully.
        Output: (Profile object, '/profiles/existingfile.dsu')  # Returns the loaded profile and file path.
    """
    
    try:
        file_path = Path(args[1]) 
        profile = Profile()
        profile.load_profile(file_path) 
        print(f'File {file_path} loaded succesfully.') 
        return profile, file_path
    except FileNotFoundError as f :
        print(f"ERROR: FILE NOT FOUND")
        return None, None
    except Exception as e:
        print(f"ERROR: EXCEPTION CAUGHT {e}")
        return None, None 


def delete_file(args: list) -> bool:
    """
    Deletes the file specified by the argument list.

    This function attempts to delete the file specified in the arguments and prints a success message if the file
    is deleted successfully. If the file doesn't exist or an error occurs, it prints an error message and returns False.

    Parameters:
        args (list): A list of arguments where:
                     - args[1] specifies the path to the file to be deleted.

    Returns:
        bool: True if the file is deleted successfully, False if there was an error (e.g., file not found).

    Exceptions:
        - Prints error messages if the file is not found or if any exception occurs during deletion.

    Example Usage:
        >>> delete_file(['D', '/profiles/existingfile.dsu'])
        /profiles/existingfile.dsu DELETED
        Output: True  # File is deleted successfully.
    """

    try: 
        file_path = Path(args[1])
        file_path.unlink()
        print(f"{file_path} DELETED")
        return True
    except FileNotFoundError as f :
        print(f"ERROR {f}")
        return False
    except Exception as e:
        print(f"ERROR {e}")
        return False


def read_file(args: list) -> bool:
    """
    Reads and prints the content of a file specified by the argument list.

    This function attempts to read the file specified in the arguments and prints its content. If the file does not
    exist or does not have a ".dsu" suffix, an error message is printed. If the file is empty, it prints "EMPTY".

    Parameters:
        args (list): A list of arguments where:
                     - args[1] specifies the path to the file to be read.

    Returns:
        bool: True if the file is read and content is displayed successfully, False if there was an error (e.g., file
              not found, wrong file type, or any other exception).

    Exceptions:
        - Prints error messages if the file does not exist, does not have a ".dsu" suffix, or if any exception occurs
          while reading the file.

    Example Usage:
        >>> read_file(['R', '/profiles/somefile.dsu'])
        File content printed here
        Output: True  # File is read successfully.
    """
    try:
        file_path = Path(args[1])
        
        if not file_path.exists():
            print(f"ERROR: FILE PATH DOES NOT EXIST")
            return False
        if file_path.suffix != ".dsu":
            print(f"ERROR: FILE DOES NOT END WITH DSU")
            return False

        content = file_path.read_text(encoding="utf-8")
        if content.strip() == "":
            print("EMPTY")
        else:
            print(content.strip())  # Print file content
        return True

    except FileNotFoundError as f:
        print(f"ERROR: {f}")
        return False
    except Exception as e :
        print(f"ERROR: {e}")
        return False


def publish_online_after_edit(args: list, profile:Profile) -> bool:
    """
    Publishes the changes made to a profile (post or bio) to an online server after user confirmation.

    This function handles the publishing of posts and bios to an online server based on user input. The user is
    prompted with a yes/no question to confirm whether they'd like to publish the change. If the user confirms, the
    changes are sent to the server specified in the profile's `dsuserver` attribute.

    Parameters:
        args (list): A list of arguments where:
                     - args[1] specifies the type of edit ('-addpost' or '-bio').
                     - args[2] contains the post or bio content to be published.
        profile (Profile): The user's profile object, containing necessary information like username, password,
                           and the server to which the profile will be published.

    Returns:
        bool: Returns True if the message is successfully sent to the server, False otherwise.

    Exceptions:
        - This function assumes that the `send` function (used for publishing to the server) is properly defined.
        - Returns the result of the `send` function call if the message is successfully sent.

    Example Usage:
        >>> publish_online_after_edit(['-addpost', 'This is a new post'], profile)
        Would you like to publish this post online? (y/n) y
        Message published to server.
        Output: True  # The post is successfully sent to the server.
    """
    message = False
    answer = ''
    if args[1] == "-addpost":
        while answer not in ('y', 'n'):
            answer = input('Would you like to publish this post online? (y/n) ')
        if answer == 'y':
            messgae = send(server = profile.dsuserver, port = 3001, username = profile.username, password = profile.password, message = args[2])
    elif args[1] == "-bio":
        while answer not in ('y', 'n'):
            answer = input('Would you like to publish this bio online? (y/n) ')
        if answer == 'y':
            message = send(server = profile.dsuserver, port = 3001, username = profile.username, password = profile.password, bio = args[2], message = None)
    
    return message


def validate_publish_online(args: list, profile: Profile) -> bool:
    """
    Validates the arguments for publishing profile changes (post or bio) to an online server.

    This function checks the correctness of the command, including:
    - Whether the first argument is either '-post' or '-bio'.
    - Whether the second argument for '-post' is a valid integer ID within the range of the user's posts.
    - Ensures that the proper number of arguments are provided.

    Parameters:
        args (list): A list of arguments, where:
                     - args[0] specifies the action ('-post' or '-bio').
                     - args[1] contains the post ID (for '-post') or the bio content (for '-bio').
        profile (Profile): The user's profile object, containing posts and other necessary information for validation.

    Returns:
        bool: Returns True if the command is valid, False otherwise.

    Exceptions:
        - If the arguments are not correctly formatted or do not match the expected pattern, it prints an error message and returns False.

    Example Usage:
        >>> validate_publish_online(['-post', '3'], profile)
        Output: True  # The command is valid for publishing a post.
        
        >>> validate_publish_online(['-bio', 'This is my new bio'], profile)
        Output: True  # The command is valid for publishing a bio.
        
        >>> validate_publish_online(['-post', 'notanumber'], profile)
        Output: False  # The ID should be a number.
    """
    
    try: 
        if args[0] not in ('-post', '-bio'):
            print('ERROR: Please select one of the two options')
            return False
        if args[0] == "-post":
            try: 
                ID = int(args[1])
                assert ID < len(profile.get_posts()), "ID MUST BE WITHING RANGE"
                assert len(args) > 1, "IMPROPER COMMAND LENGTH"
            except ValueError: 
                print('ERROR: ID must be a number')
                return False
            except AssertionError as e:
                print('ERROR: ID must be within range')
                return False
    except IndexError:
        print('ERROR: IMPROPER COMMAND LENGTH')
        return False

    return True


def publish_online(args: list, profile: Profile) -> bool:
    """
    Publishes a user's post or bio to an online server.

    This function sends a message (either a post or bio) from the user's profile to a specified server. The action is determined by the first argument:
    - '-bio': The user's bio will be sent.
    - '-post': The post with the ID specified by the second argument will be sent.

    Parameters:
        args (list): A list of arguments, where:
                     - args[0] specifies the action ('-post' or '-bio').
                     - args[1] (for '-post') specifies the post ID to be published.
        profile (Profile): The user's profile object, containing the necessary information for sending the message (e.g., posts and bio).

    Returns:
        bool: Returns True if the message was successfully sent, False otherwise.

    Example Usage:
        >>> publish_online(['-bio'], profile)
        Output: True  # Bio is successfully published to the server.
        
        >>> publish_online(['-post', '3'], profile)
        Output: True  # Post with ID 3 is successfully published to the server.
        
        >>> publish_online(['-post', 'notanumber'], profile)
        Output: False  # An error occurs because the post ID is invalid.
    """

    message = False
    if args[0] == '-bio':
        message = send(server = profile.dsuserver, port = 3001, username = profile.username, password = profile.password, bio = profile.bio, message = None)
    elif args[0] == '-post':
        ID = int(args[1])
        message = send(server = profile.dsuserver, port = 3001, username = profile.username, password = profile.password, message = profile.get_posts()[ID].entry)
    return message


def main(command_line: str =None, profile: Profile = None, profile_path: str = None) -> tuple[Profile, str]:
    """
    Main loop for processing user commands related to managing a user profile and interacting with a file system.

    The function parses and executes commands based on the input received either from a command line argument or from interactive input. Commands include:
    - 'C': Create a new profile.
    - 'D': Delete a file.
    - 'R': Read a file.
    - 'O': Open an existing profile.
    - 'E': Edit a profile.
    - 'P': Print profile details.
    - 'W': Publish online (bio or post).

    Parameters:
        command_line (str, optional): A string containing the user input to be processed. If not provided, interactive input is requested.
        profile (Profile, optional): The current user profile object. Used for operations that require profile data, such as editing and publishing.
        profile_path (str, optional): The file path where the profile data is saved or loaded from.

    Returns:
        tuple: A tuple containing the updated profile and the profile file path. If no actions are taken (e.g., 'Q' command or errors), it returns (None, None).

    Example Usage:
        >>> main('C -dir /profile_name')
        (Profile, 'profile_path')

        >>> main('O -dir /profile_name')
        (Profile, 'profile_path')

        >>> main('Q')
        None, None

    Command Syntax:
        - 'C': Create a new profile
        - 'D': Delete a file
        - 'R': Read a file
        - 'O': Open a profile
        - 'E': Edit a profile
        - 'P': Print profile details
        - 'W': Publish profile data online
        - 'Q': Quit the application
    """

    if command_line:    
        args = split_input(command_line)
    else: 
        args = read_input()
    
    if args == None:
        return None, None 

    if len(args) == 0:
        print("ERROR: COMMAND LINE IS EMPTY")

    command = args[0].upper()

    if command == "Q":
        return None, None
    elif command == "C":
        if validate_create(args) == True:
            profile, profile_path = create_file(args)
    elif command == "D":
        if validate_file_command(args, expected_args=2):
            delete_file(args)
    
    elif command == "R":
        if validate_file_command(args, expected_args=2):
            read_file(args)

    elif command == "O":
        if validate_file_command(args, expected_args=2):
            profile, profile_path = open_file(args)

    elif command == "E":
        for i in range(1, len(args), 2):
            if validate_edit(args[i:i+2], profile):
                edit_file(args[i:i+2], profile, profile_path)
                publish_online_after_edit(args, profile)
            else:
                break

    elif command == 'P':
        for i in range(1, len(args)):
            if args[i] == '-post':
                if validate_print(args[i:i+2]) and profile:
                    print_file(args[i:i+2], profile)
                else:
                    print('ERROR: INVALID COMMAND FOR PRINT')
                    break
            else:
                if validate_print(args[i:i+1]) and profile:
                    print_file(args[i:i+1], profile)
                else:
                    break
    elif command == 'W':
        for i in range(1, len(args)):
            if args[i] == "-post":
                if validate_publish_online(args[i:i+2], profile) and profile:
                    publish_online(args[i:i+2], profile)
                else:
                    break
            elif args[i] == "-bio":
                if validate_publish_online(args[i:i+1], profile) and profile:
                    publish_online(args[i:i+1], profile)
                else:
                    break
            else:
                continue
    else:
        print("ERROR: INVALID COMMAND GIVEN")
    
    return profile, profile_path


def main_function() -> None:
    """
    Main entry point for running the user profile management system.

    This function provides an interactive loop where users can input commands to create, read, edit, delete, and manage their profiles.
    The loop continues until the user inputs 'Q' to quit. Additionally, the function allows an admin to enter an admin interface with the 'ADMIN' command.

    It interacts with the `print_welcome` function to display a welcome message and the `print_border` function to separate user inputs visually. The `loop` function handles user command input, while `main` processes the commands.

    Flow of Execution:
        1. Displays a welcome message.
        2. Prompts the user for a command.
        3. Processes the command with `main` (handling profile-related tasks).
        4. Exits if 'Q' is input.
        5. Provides an option for an admin to access admin controls if 'ADMIN' is input.

    The user profile and profile path are managed throughout the session, and each command affects the profile state.

    Functions and Features:
        - `print_welcome`: Displays the welcome message.
        - `print_border`: Prints a visual separator for commands.
        - `loop`: Handles the continuous input loop for user commands.
        - `main`: Handles profile-related logic based on the user's commands.
        - 'Q': Quit the program.
        - 'ADMIN': Enter the admin interface for further management.
    
    Example usage:
        >>> main_function()  # Initiates the interactive loop with user commands

    Returns:
        None.
    """

    print_welcome()
    profile = None
    profile_path = None
    while True:
        print_border()

        command_line = loop(profile)
        if command_line == 'Q':
            break
        if command_line == 'ADMIN':
            admin_main()
            break
        else:
            profile, profile_path = main(command_line, profile, profile_path)


if __name__ == '__main__':
    main_function()
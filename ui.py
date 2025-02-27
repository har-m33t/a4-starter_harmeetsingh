# ui.py

# Starter code for assignment 2 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Harmeet
# harmees2
# 27012171

from a4 import main
from admin import admin_main
from Profile import Profile


def print_welcome():
    """
    Displays a welcome message to the user when they start the program.
    
    Example usage:
        >>> print_welcome()
    """
    text = 'Welcome to your Journal'
    print(f'--- | {text:^10} | ---')


def print_menu() -> str:
    """
    Displays the main menu with all available options to the user and prompts for input.
    
    Returns:
        str: The user's selected command.
    
    Example usage:
        >>> command = print_menu()
    """
    text = '~ ~ ~ | MENU | ~ ~ ~'
    print(f'{text:^36}')
    print_border()
    print_options()
    print_border()
    command = get_command()
    return command


def print_options():
    """
    Displays the list of available options for the user to select from the menu.
    
    Example usage:
        >>> print_options()
    """
    print('OPTIONS')
    print('\tC ~ Create a DSU File')
    print('\tO ~ Open an existing DSU File')
    print('\tE ~ Edit an Open DSU File')
    print('\tP ~ Print Contents of an Open DSU File')
    print('\tD ~ Delete an existing DSU File')
    print('\tR ~ Read Contents of a File')
    print('\tW ~ Post your Journal')
    print('\tQ ~ Quit the program')


def get_command() -> str:
    """
    Prompts the user for a command input.
    
    Returns:
        str: The user's input command.
    
    Example usage:
        >>> command = get_command()
    """
    command = input('Please Enter an Option listed above: ')
    return command


def print_border(num=36):
    """
    Prints a border line for better visual organization of the UI.
    
    Args:
        num (int): The length of the border line. Defaults to 36.
    
    Example usage:
        >>> print_border(40)
    """
    border = '-' * num
    print(f'{border}')


def validate_ui_command(command: str) -> bool:
    """
    Validates the user command input to ensure it matches one of the valid options.
    
    Args:
        command (str): The user command to validate.
    
    Returns:
        bool: True if the command is valid, False otherwise.
    
    Example usage:
        >>> is_valid = validate_ui_command('C')
    """
    try:
        if command == 'ADMIN':
            return True
        assert len(command) == 1
        assert command in ('Q', 'C', 'D', 'R', 'O', 'E' ,'P' , 'W', 'ADMIN')
        return True
    except AssertionError:
        print('ERROR: ENTER A VALID COMMAND')
        return False


def print_edit_options():
    """
    Displays a list of available options to edit in the profile (e.g., username, password, bio).
    
    Example usage:
        >>> print_edit_options()
    """
    print('Edit Options: ')
    print('\t-usr ~ Change username')
    print('\t-pwd ~ Change password')
    print('\t-bio ~ Change bio')
    print('\t-addpost [POST] ~ Add post')
    print('\t-delpost [ID] ~ Delete post by ID')
    print_border()


def print_print_options():
    """
    Displays a list of available options to print from the profile (e.g., username, password, posts).
    
    Example usage:
        >>> print_print_options()
    """
    print('Print Options')
    print('\t-usr ~ Prints the username stored in the profile object')
    print('\t-pwd ~ Prints the password stored in the profile object')
    print('\t-bio ~ Prints the bio stored in the profile object')
    print('\t-posts ~ Prints all posts stored in the profile with ID')
    print('\t-post [ID] ~ Prints post identified by ID')
    print('\t-all ~ Prints all content stored in the profile object')
    print_border()


def print_publish_options():
    """
    Displays a list of available options to publish content online from the profile (e.g., bio, post).
    
    Example usage:
        >>> print_publish_options()
    """
    print('Publish online options: ')
    print('\t-bio ~ Posts the bio stored in the profile object')
    print('\t-post [ID] ~ Post identified by ID')


def loop(profile: Profile = None) -> str:
    """
    The main loop that handles user input and processes the commands based on the selected menu option.
    
    Args:
        profile (Profile): The current profile being edited or used. Defaults to None.
    
    Returns:
        str: The command line string to be processed by the main function or other UI logic.
    
    Example usage:
        >>> command_line = loop(profile)
    """
    space = ' '
    while True:
        command = print_menu()
        command = command.upper().strip()
        if validate_ui_command(command):
            if command == 'Q':
                command_line = 'Q'
            elif command == 'C':
                print_border()
                path = input('Enter the directory this file will go into: ')
                name = input('Enter name of file: ')
                command_line = 'C' + space + path + space + '-n' + space + name
                print_border()
            elif command == 'D':
                print_border()
                path = input('Enter the file path for the file to delete: ')
                print_border()
                command_line = 'D' + space + path
            elif command == 'R':
                print_border()
                path = input('Enter the file path for the file to read: ')
                print_border()
                command_line = 'R' + space + path
            elif command == 'O':
                print_border()
                path = input('Enter the file path for the file to Open: ')
                print_border()
                command_line = 'O' + space + path
            elif command == 'E':
                print_border()
                print_edit_options()
                option = input('What would you like to edit in this file: ')
                print_border()
                command_line = 'E' + space + option
            elif command == 'P':
                print_border()
                print_print_options()
                option = input('What would you like to print in this file: ')
                command_line = 'P' + space + option
                print_border()
            elif command == 'W':
                print_border()
                print_publish_options()
                if profile:
                    print('Your posts: ')
                    if profile.get_posts():
                        for i, post in enumerate(profile.get_posts()):
                            print(f'\t{i}: {post.entry}')
                    else:
                        print('NO POSTS')
                    
                    if profile.bio:
                        print(f'Your Bio: {profile.bio}')
                    else:
                        print('Your Bio: EMPTY')
                else:
                    print('ERROR: NO PROFILE OPEN CURRENTLY')
                    return None
                option = input('What would you like to post: ')
                command_line = 'W' + space + option
            elif command == 'ADMIN':
                command_line = command
            return command_line

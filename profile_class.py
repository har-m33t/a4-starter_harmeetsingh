"""
profile_class.py

This module defines the Profile and Post classes,
which are used to manage user profiles
and posts for a Distributed Social Universe (DSU) server.
It includes functionality for
saving and loading profiles, managing posts, and handling exceptions.
"""

import json
import time
from pathlib import Path


class DsuFileError(Exception):
    """
    Custom exception raised when
    there is an error loading or saving Profile objects
    to a file.
    """


class DsuProfileError(Exception):
    """
    Custom exception raised
    when there is an error deserializing a DSU file to a
    Profile object.
    """


class Post(dict):
    """
    The Post class is responsible for
    working with individual user posts.
    It supports a timestamp property and an
    entry property that stores the post message.
    """

    def __init__(self, entry: str = None, timestamp: float = 0):
        """
        Initialize a Post object.

        Args:
            entry (str):
                The content of the post.
            timestamp (float):
                The timestamp of the post. Defaults to the current time.
        """
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry: str) -> None:
        """
        Set the entry content of the post
        and update the timestamp if not already set.

        Args:
            entry (str): The content of the post.
        """
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new one
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self) -> str:
        """
        Get the entry content of the post.

        Returns:
            str: The content of the post.
        """
        return self._entry

    def set_time(self, timestamp: float) -> None:
        """
        Set the timestamp of the post.

        Args:
            timestamp (float): The timestamp to set.
        """
        self._timestamp = timestamp
        dict.__setitem__(self, 'timestamp', timestamp)

    def get_time(self) -> float:
        """
        Get the timestamp of the post.

        Returns:
            float: The timestamp of the post.
        """
        return self._timestamp

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    """
    The Profile class manages user profiles
    for the DSU server.
    It includes properties such as
    username, password, bio, posts, friends, and messages.
    """

    def __init__(self,
                 dsuserver: str = None,
                 username: str = None,
                 password: str = None
                 ):
        """
        Initialize a Profile object.

        Args:
            dsuserver (str): The DSU server address.
            username (str): The username for the profile.
            password (str): The password for the profile.
        """
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.bio = ''  # OPTIONAL
        self._posts = []  # OPTIONAL
        self.friends = []
        self.messages = []

    def add_post(self, post: Post) -> None:
        """
        Add a Post object to the profile's posts list.

        Args:
            post (Post): The Post object to add.
        """
        self._posts.append(post)

    def del_post(self, index: int) -> bool:
        """
        Delete a Post object at the specified index.

        Args:
            index (int): The index of the post to delete.

        Returns:
            bool: True if the post was deleted, False otherwise.
        """
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    def get_posts(self) -> list[Post]:
        """
        Get the list of posts in the profile.

        Returns:
            list[Post]: The list of Post objects.
        """
        return self._posts

    def add_message(self, message: dict) -> None:
        """
        Add a message to the profile's messages list.

        Args:
            message (dict): The message to add.
        """
        self.messages.append(message)

    def add_friend(self, friend_username: str) -> None:
        """
        Add a friend to the profile's friends list.

        Args:
            friend_username (str): The username of the friend to add.
        """
        if friend_username not in self.friends:
            self.friends.append(friend_username)

    def get_messages_for_recipient(self, recipient: str) -> list[dict]:
        """
        Get messages for a specific recipient.

        Args:
            recipient (str): The recipient's username.

        Returns:
            list[dict]: The list of messages for the recipient.
        """
        return [msg for msg in self.messages if msg['recipient'] == recipient]

    def save_profile(self, path: str) -> None:
        """
        Save the profile to a DSU file.

        Args:
            path (str): The path to the DSU file.

        Raises:
            DsuFileError: If there is an error saving the file.
        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'w', encoding='utf-8') as f:
                    json.dump(self.__dict__, f)
            except Exception as ex:
                raise DsuFileError(
                    "Error while attempting to process the DSU file."
                    ) from ex
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        """
        Load a profile from a DSU file.

        Args:
            path (str): The path to the DSU file.

        Raises:
            DsuProfileError: If there is an error loading the file.
            DsuFileError: If the file is invalid.
        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                    self.username = obj['username']
                    self.password = obj['password']
                    self.dsuserver = obj['dsuserver']
                    self.bio = obj['bio']
                    self.friends = obj['friends']
                    self.messages = obj['messages']
                    for post_obj in obj['_posts']:
                        post = Post(post_obj['entry'], post_obj['timestamp'])
                        self._posts.append(post)
            except Exception as ex:
                raise DsuProfileError(ex) from ex
        else:
            raise DsuFileError()

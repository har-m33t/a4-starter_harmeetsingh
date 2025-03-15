"""
This module implements a GUI-based distributed
social messenger application using Tkinter.
It allows users to send and receive messages,
manage contacts, and configure server settings.

Author: Harmeet Singh
Email: harmees2
Student ID: 27012171

"""

import sys
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import time
import socket
import sv_ttk
from ds_messenger import DirectMessenger, DirectMessage
from profile_class import Profile, Path


class Body(tk.Frame):
    """Represents the main body of the GUI, handling contacts and messages."""

    def __init__(self, root, recipient_selected_callback=None):
        """Initialize the Body frame.

        Args:
            root:
                The root Tkinter window.
            recipient_selected_callback:
                Callback function for when a recipient is selected.
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event):
        """
        Handle the selection of a contact in the contact list.
        """
        try:
            print(event)
            selected_item = self.posts_tree.selection()
            if selected_item:
                item_id = selected_item[0]
                contact_name = self.posts_tree.item(item_id, "text")
                if self._select_callback is not None:
                    self._select_callback(contact_name)
        except IndexError:
            pass

    def insert_contact(self, contact: str):
        """Insert a new contact into the contact list.
        Args:
            contact: The name of the contact to add.
        """
        self._contacts.append(contact)
        contact_id = len(self._contacts) - 1
        self._insert_contact_tree(contact_id, contact)

    def _insert_contact_tree(self, contact_id, contact: str):
        """Insert a contact into the Treeview widget.

        Args:
            contact_id: The ID of the contact.
            contact: The name of the contact.
        """
        if len(contact) > 25:
            contact = contact[:24] + "..."
        self.posts_tree.insert('', contact_id, contact_id, text=contact)

    def insert_user_message(self, message: str):
        """Insert a message sent by the user into the message display.

        Args:
            message: The message to insert.
        """
        self.entry_editor.insert(
            tk.END,
            message + '\n',
            'entry-right'
            )

    def insert_contact_message(self, message: str):
        """Insert a message received from a contact into the message display.
        Args:
            message: The message to insert.
        """
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        """Get the text entered in the message editor.

        Returns:
            The text from the message editor.
        """
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        """Set the text in the message editor.

        Args:
            text: The text to set.
        """
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _insert_all_msgs(self, messages: list[DirectMessage], recipient):
        """Insert all messages for a recipient into the message display.

        Args:
            messages: A list of DirectMessage objects.
            recipient: The recipient of the messages.
        """
        for msg in messages:
            if not msg.from_user:
                if msg.sender == recipient:
                    self.insert_contact_message(msg.message)
            elif msg.from_user:
                if msg.sender == recipient:
                    self.insert_user_message(msg.message)

    def reset_message_box(self):
        """Reset the message editor to an empty state."""
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, '')

    def reset_entry_box(self):
        """Reset the entry editor to an empty state."""
        self.entry_editor.delete(1.0, tk.END)
        self.entry_editor.insert(1.0, '')

    def reset_ui(self):
        """Reset the UI to its initial state."""
        self.reset_entry_box()
        self.reset_message_box()
        self.posts_tree.delete(*self.posts_tree.get_children())
        self.insert_contact("studentexw23")

    def _draw(self):
        """Draw the widgets in the Body frame."""
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind(
            "<<TreeviewSelect>>",
            self.node_select
            )
        self.posts_tree.pack(
            fill=tk.BOTH, side=tk.TOP,
            expand=True, padx=5, pady=5
            )

        entry_frame = tk.Frame(
            master=self,
            bg=""
            )
        entry_frame.pack(
            fill=tk.BOTH,
            side=tk.TOP,
            expand=True
            )

        editor_frame = tk.Frame(
            master=entry_frame,
            bg="red"
            )
        editor_frame.pack(
            fill=tk.BOTH,
            side=tk.LEFT,
            expand=True
            )

        scroll_frame = tk.Frame(
            master=entry_frame,
            bg="blue",
            width=10
            )

        scroll_frame.pack(
            fill=tk.BOTH,
            side=tk.LEFT,
            expand=False
            )

        message_frame = tk.Frame(
            master=self,
            bg="yellow"
            )
        message_frame.pack(
            fill=tk.BOTH,
            side=tk.TOP,
            expand=False
            )

        self.message_editor = tk.Text(
            message_frame,
            width=0,
            height=5
            )
        self.message_editor.pack(
            fill=tk.BOTH,
            side=tk.LEFT,
            expand=True,
            padx=0,
            pady=0
            )

        self.entry_editor = tk.Text(
            editor_frame,
            width=0,
            height=5
            )
        self.entry_editor.tag_configure(
            'entry-right',
            justify='right'
            )
        self.entry_editor.tag_configure(
            'entry-left',
            justify='left'
            )
        self.entry_editor.pack(
            fill=tk.BOTH,
            side=tk.LEFT,
            expand=True,
            padx=0,
            pady=0
            )

        entry_editor_scrollbar = tk.Scrollbar(
            master=scroll_frame,
            command=self.entry_editor.yview
            )
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(
            fill=tk.Y,
            side=tk.LEFT,
            expand=False,
            padx=0,
            pady=0
            )


class Footer(tk.Frame):
    """Represents the footer of the GUI, containing the Send button."""

    def __init__(self, root, send_callback=None):
        """Initialize the Footer frame.

        Args:
            root: The root Tkinter window.
            send_callback: Callback function for the Send button.
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        """Handle the Send button click event."""
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        """Draw the widgets in the Footer frame."""
        save_button = tk.Button(
            master=self,
            text="Send",
            width=20
            )
        save_button.bind(
            "<Button-1>",
            lambda event: self.send_click()
            )
        save_button.pack(
            fill=tk.BOTH,
            side=tk.RIGHT,
            padx=5,
            pady=5
            )

        self.footer_label = tk.Label(
            master=self,
            text="Ready."
            )

        self.footer_label.pack(
            fill=tk.BOTH,
            side=tk.LEFT,
            padx=5
            )


class NewContactDialog(tk.simpledialog.Dialog):
    """A dialog for configuring server settings and user credentials."""

    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        """Initialize the NewContactDialog.

        Args:
            root: The root Tkinter window.
            title: The title of the dialog.
            user: The username.
            pwd: The password.
            server: The server address.
        """
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, master):
        """Create the dialog body.

        Args:
            frame: The frame to add widgets to.
        """
        self.server_label = tk.Label(
            master,
            width=30,
            text="DS Server Address"
            )
        self.server_label.pack()
        self.server_entry = tk.Entry(master, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(
            master,
            width=30,
            text="Username"
            )
        self.username_label.pack()
        self.username_entry = tk.Entry(master, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(master, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, width=30)
        self.password_entry.insert(tk.END, self.user)
        self.password_entry.pack()
        self.password_entry['show'] = '*'

    def apply(self):
        """Apply the settings entered in the dialog."""
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    """The main application class for the distributed social messenger."""

    def __init__(self, root):
        """Initialize the MainApp.

        Args:
            root: The root Tkinter window.
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        self.direct_messenger = None
        self.profile = None
        self.filepath = None
        self._draw()
        self.body.insert_contact("studentexw23")

    def is_server_running(
            self, host='localhost', port=3001, timeout=2
            ) -> bool:
        """Check if the server is running.

        Args:
            host: The server host.
            port: The server port.
            timeout: The connection timeout.

        Returns:
            True if the server is running, False otherwise.
        """
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except (socket.timeout, ConnectionRefusedError):
            return False

    def send_message(self):
        """Send a message to the selected recipient."""
        if not self.direct_messenger:
            tk.messagebox.showerror(
                "Error",
                "DirectMessenger instance not initialized."
                )
            return
        if not self.recipient:
            tk.messagebox.showerror(
                "Error",
                "No recipient selected. Please choose a contact."
                )
            return
        if not self.is_server_running():
            tk.messagebox.showerror(
                "Server Error",
                "Unable to connect. Server not running."
                )
            return

        message = self.body.get_text_entry()

        if not message:
            tk.messagebox.showerror(
                "Error",
                "Cannot send an empty message."
                )
            return
        try:
            self.publish(message)
            self.body.insert_user_message(f"{message}")
            self.body.set_text_entry("")

            self.profile.add_message(
                {
                    'recipient': self.recipient,
                    'message': message,
                    'from_user': True,
                    'timestamp': time.time()
                }
            )
            self.profile.save_profile(self.filepath)
        except AttributeError as e:
            tk.messagebox.showerror(
                "Attribute Error",
                f"An internal error occurred: {e}"
                )
        except ConnectionError:
            tk.messagebox.showerror(
                "Connection Error",
                "Failed to send message. Check your network connection."
                )
        except socket.timeout:
            tk.messagebox.showerror(
                "Timeout Error",
                "Message sending timed out. Try again."
                )
        except ValueError as e:
            tk.messagebox.showerror(
                "Data Error",
                f"Invalid message data: {e}"
                )
        except OSError as e:
            tk.messagebox.showerror(
                "File Error",
                f"Failed to save message: {e}"
                )
        except RuntimeError as e:
            tk.messagebox.showerror(
                "Publishing Error",
                f"Failed to publish message: {e}"
                )

    def add_contact(self):
        """Add a new contact."""
        if not self.is_server_running():
            tk.messagebox.showerror(
                "Server Error",
                "Unable to connect. The server is not running."
                )
            return
        contact = simpledialog.askstring(
            'Add Contact',
            "Enter Contact Name:"
            )
        if not contact:
            tk.messagebox.showerror(
                "Contact Error",
                "Contact name cannot be empty."
                )
            return
        if contact == self.username:
            tk.messagebox.showerror(
                "Contact Error",
                "Contact cannot be yourself"
                )
            return

        self.body.insert_contact(contact)
        self.profile.add_friend(contact)
        self.profile.save_profile(self.filepath)

    def retrive_contacts(self):
        """Retrieve and display all contacts."""
        for contact in self.profile.friends:
            self.body.insert_contact(contact)

    def recipient_selected(self, recipient):
        """Handle the selection of a recipient.

        Args:
            recipient: The selected recipient.
        """
        self.recipient = recipient
        self.body.reset_entry_box()
        self.body.reset_message_box()
        try:
            messages = self.profile.get_messages_for_recipient(recipient)
            for msg in messages:
                if msg['from_user']:
                    self.body.insert_user_message(msg['message'])
                else:
                    self.body.insert_contact_message(msg['message'])
        except AttributeError:
            tk.messagebox.showerror(
                'Profile Error',
                'No Profile Currently Open'
                )

    def configure_server(self):
        """Configure the server settings."""
        try:
            ud = NewContactDialog(
                self.root, "Configure Account",
                self.username, self.password, self.server
                )
            self.username = ud.user
            self.password = ud.pwd
            self.server = ud.server

            if not self.username:
                tk.messagebox.showerror(
                    'Configuration Error',
                    'Cannot Leave Username Empty'
                    )
                return
            if not self.password:
                tk.messagebox.showerror(
                    'Configuration Error',
                    'Cannot Leave Password Empty'
                    )
                return
            if not self.server:
                tk.messagebox.showerror(
                    'Configuration Error',
                    'Cannot Leave Server Empty')
                return

            if not self.is_server_running():
                tk.messagebox.showerror(
                    "Server Error",
                    "Unable to connect. The server is not running.")
                return

            self.direct_messenger = DirectMessenger(
                self.server, self.username, self.password
                )
            if self.direct_messenger:
                print('DirectMessenger Initialized')
            print(f"Connected to server: {self.server}")

            print('Creating Profile')
            self.profile = Profile(
                self.server, self.username, self.password
                )

            self.body.reset_ui()

        except TypeError as e:
            tk.messagebox.showerror(
                "Configuration Error",
                f"Invalid parameters for NewContactDialog: {e}")
        except RuntimeError as e:
            tk.messagebox.showerror(
                "Configuration Error",
                f"Failed to initialize NewContactDialog: {e}"
                )
        except AttributeError as e:
            tk.messagebox.showerror(
                "Configuration Error",
                f"Missing values from NewContactDialog: {e}"
                )
        except ConnectionError:
            tk.messagebox.showerror(
                "Server Error",
                "Failed to check if server is running."
                )
        except ValueError as e:
            tk.messagebox.showerror(
                "Configuration Error",
                f"Invalid credentials or server response: {e}"
                )

    def publish(self, message: str):
        """Publish a message to the server.

        Args:
            message: The message to publish.
        """
        try:
            if self.direct_messenger and self.recipient:
                self.direct_messenger.send(message, self.recipient)
            else:
                tk.messagebox.showerror(
                    "Publish Error",
                    "DirectMessenger or recipient is not set."
                    )
        except AttributeError as e:
            tk.messagebox.showerror(
                "Publish Error",
                f"Messaging system not initialized properly: {e}"
                )
        except ValueError as e:
            tk.messagebox.showerror(
                "Publish Error",
                f"Invalid recipient or message format: {e}"
                )
        except ConnectionError:
            tk.messagebox.showerror(
                "Publish Error",
                "Failed to send message: Connection lost."
                )
        except TimeoutError:
            tk.messagebox.showerror(
                "Publish Error",
                "Failed to send message: Server timeout."
                )
        except RuntimeError as e:
            tk.messagebox.showerror(
                "Publish Error",
                f"Unexpected error while sending: {e}"
                )
        except OSError as e:
            tk.messagebox.showerror(
                "Publish Error",
                f"Network/socket error: {e}"
                )

    def check_new(self):
        """Check for new messages from the server."""
        if self.direct_messenger:
            try:
                messages = self.direct_messenger.retrieve_new()
                if not isinstance(messages, list):
                    raise TypeError("Expected a list of messages.")
                for msg in messages:
                    self.body.insert_contact_message(f"{msg.message}")
                    self.profile.add_message(
                        {
                            'recipient': msg.sender,
                            'message': msg.message,
                            'from_user': False,
                            'timestamp': time.time()
                        }
                    )
                    self.profile.save_profile(self.filepath)
            except AttributeError as e:
                tk.messagebox.showerror(
                    "Check Error",
                    f"Messaging system not initialized: {e}"
                    )
            except ConnectionError:
                tk.messagebox.showerror(
                    "Check Error",
                    "Failed to retrieve messages: Connection lost."
                    )
            except TimeoutError:
                tk.messagebox.showerror(
                    "Check Error",
                    "Failed to retrieve messages: Server timeout."
                    )
            except TypeError as e:
                tk.messagebox.showerror(
                    "Check Error",
                    f"Unexpected response format: {e}"
                    )
            except KeyError as e:
                tk.messagebox.showerror(
                    "Check Error",
                    f"Missing expected message data: {e}"
                    )
            except RuntimeError as e:
                tk.messagebox.showerror(
                    "Check Error",
                    f"Error updating UI with new messages: {e}"
                    )
            except OSError as e:
                tk.messagebox.showerror(
                    "Check Error",
                    f"Failed to save messages: {e}"
                    )

        self.root.after(2000, self.check_new)

    def create_file(self):
        """Create a new profile file."""
        filepath = filedialog.asksaveasfilename()
        if not filepath:
            tk.messagebox.showerror(
                "File Creation Error",
                "No file selected. Please choose a valid file name."
                )
            return
        filepath += ".dsu"
        self.filepath = Path(filepath)
        try:
            self.filepath.touch()
        except (PermissionError, OSError) as e:
            tk.messagebox.showerror(
                "File Creation Error",
                f"File system error: {e}"
                )
            return

        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        self.direct_messenger = None

        try:
            self.configure_server()
        except (ConnectionError, ValueError) as e:
            tk.messagebox.showerror(
                "Configuration Error",
                f"Error: {e}"
                )
            return

        try:
            self.profile.save_profile(self.filepath)
        except (FileNotFoundError, OSError) as e:
            tk.messagebox.showerror(
                "File Save Error",
                f"Error: {e}"
                )
            return

    def open_file(self):
        """Open an existing profile file."""
        filepath = filedialog.askopenfilename()
        if not filepath:
            tk.messagebox.showerror(
                "File Opening Error",
                "No file selected."
                )
            return

        if not Path(filepath).exists():
            tk.messagebox.showerror(
                "File Opening Error",
                "Selected file does not exist."
                )
            return

        self.body.reset_ui()
        self.filepath = Path(filepath)

        try:
            self.profile = Profile()
            self.profile.load_profile(self.filepath)
        except (ValueError, KeyError) as e:
            tk.messagebox.showerror(
                "Profile Error",
                f"Error: {e}"
                )
            return

        self.username = self.profile.username
        self.password = self.profile.password
        self.server = self.profile.dsuserver

        try:
            self.direct_messenger = DirectMessenger(
                self.server, self.username, self.password
                )
        except ConnectionError:
            tk.messagebox.showerror(
                "Server Connection Error",
                "Unable to connect to the server."
                )
            return
        except ValueError as e:
            tk.messagebox.showerror(
                "Login Error",
                f"Invalid credentials: {e}"
                )
            return

        try:
            print(self.profile.friends)
            self.retrive_contacts()
        except AttributeError:
            tk.messagebox.showerror(
                "Contacts Error",
                "Error retrieving contacts. Profile data may be corrupted."
                )
            return

    def close_program(self):
        """Close the program."""
        sys.exit()

    def _draw(self):
        """Draw the main application UI."""
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(
            label='New',
            command=self.create_file
            )
        menu_file.add_command(
            label='Open...',
            command=self.open_file
            )
        menu_file.add_command(
            label='Close',
            command=self.close_program
            )

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(
            menu=settings_file,
            label='Settings'
            )
        settings_file.add_command(
            label='Add Contact',
            command=self.add_contact
            )
        settings_file.add_command(
            label='Configure DS Server',
            command=self.configure_server
            )

        self.body = Body(
            self.root,
            recipient_selected_callback=self.recipient_selected
            )
        self.body.pack(
            fill=tk.BOTH,
            side=tk.TOP,
            expand=True)
        self.footer = Footer(
            self.root, send_callback=self.send_message
            )
        self.footer.pack(
            fill=tk.BOTH, side=tk.BOTTOM
            )


if __name__ == "__main__":
    main = tk.Tk()
    main.title("ICS 32 Distributed Social Messenger")
    main.geometry("720x480")
    main.option_add('*tearOff', False)

    style = ttk.Style()
    style.theme_use('clam')

    sv_ttk.set_theme('dark')

    app = MainApp(main)

    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    timer_id = main.after(2000, app.check_new)
    print(timer_id)
    main.mainloop()

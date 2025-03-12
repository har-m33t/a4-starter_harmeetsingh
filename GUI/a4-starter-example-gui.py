import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from typing import Text
import time

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server_client_protocol.ds_messenger import DirectMessenger, DirectMessage

from a4_logic.Profile import Profile, Path

import socket

import sv_ttk

class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        selected_item = self.posts_tree.selection()  # Get selected item(s)
        if selected_item:
            item_id = selected_item[0]  # Get first selected item
            entry = self.posts_tree.item(item_id, "text")  # Get the contact name
            if self._select_callback is not None:
                self._select_callback(entry) 

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str):
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')

    def insert_contact_message(self, message:str):
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)
    
    def _insert_all_msgs(self, messages: list[DirectMessage], recipient):
        for msg in messages:
            if msg._from_user == False:
                if msg.sender == recipient:
                    self.insert_contact_message(msg.message)
            elif msg._from_user == True:
                if msg.sender == recipient:
                    self.insert_user_message(msg.message)
    
    def _reset_message_box(self):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, '')
    
    def _reset_entry_box(self):
        self.entry_editor.delete(1.0, tk.END)
        self.entry_editor.insert(1.0, '')

    def _reset_ui(self):
        self._reset_entry_box()
        self._reset_message_box
        self.posts_tree.delete(*self.posts_tree.get_children())
        self.insert_contact("studentexw23") 

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.bind("<Button-1>", lambda event: self.send_click())

        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        # You need to implement also the region for the user to enter
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols.
        #self.password...

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry.insert(tk.END, self.user)
        self.password_entry.pack()
        self.password_entry['show'] = '*'

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        #self.direct_messenger = ... continue!
        self.direct_messenger = None
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        self.body.insert_contact("studentexw23") # adding one example student.

    
    def is_server_running(self, host = 'localhost', port = 3001, timeout=2) -> bool:
        """Checks if a server is running at the given host and port."""
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except (socket.timeout, ConnectionRefusedError):
            return False
        
    def send_message(self): # WORKS 
        # You must implement this!
        if not self.direct_messenger:
            tk.messagebox.showerror("Error", "DirectMessenger instance is not initialized.")
            return
        if not self.recipient:
            tk.messagebox.showerror("Error", "No recipient selected. Please choose a contact.")
            return
        if not self.is_server_running():
            tk.messagebox.showerror("Server Error", "Unable to connect. The server is not running.")
            return
        message = self.body.get_text_entry()
        if not message:
            tk.messagebox.showerror("Error", "Cannot send an empty message.")
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
        except Exception as e:
            tk.messagebox.showerror("Message Error", f"Failed to send message: {e}")

    def add_contact(self): 
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        if not self.is_server_running():
            tk.messagebox.showerror("Server Error", "Unable to connect. The server is not running.")
            return
        contact = simpledialog.askstring('Add Contact', "Enter Contact Name:")
        if not contact:
            tk.messagebox.showerror("Error", "Contact name cannot be empty.")
            return
        
        self.body.insert_contact(contact)
        self.profile.add_friend(contact)
        self.profile.save_profile(self.filepath)
    
    def retrive_contacts(self):
        for contact in self.profile.friends:
            self.body.insert_contact(contact)

    def recipient_selected(self, recipient):
        self.recipient = recipient
        self.body._reset_entry_box()
        self.body._reset_message_box()
        try: 
            messages = self.profile.get_messages_for_recipient(recipient)
            for msg in messages:
                if msg['from_user']:
                    self.body.insert_user_message(msg['message'])
                else:
                    self.body.insert_contact_message(msg['message'])
        except AttributeError:
            tk.messagebox.showerror('Profile Error', 'No Profile Currently Open')

                
    def configure_server(self):
        '''Create an Account'''
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        if not self.username:
            tk.messagebox.showerror('Configuration Error', 'Cannot Leave Username Empty')
            return
        if not self.password:
            tk.messagebox.showerror('Configuration Error', 'Cannot Leave Password Empty')
            return 
        if not self.server:
            tk.messagebox.showerror('Configuration Error', 'Cannot Leave Server Empty')
            return

        # You must implement this!
        # You must configure and instantiate your
        # DirectMessenger instance after this line.
        if not self.is_server_running():
            tk.messagebox.showerror("Server Error", "Unable to connect. The server is not running.")
            return
        # Initialize DirectMessenger with validated server
        try:
            self.direct_messenger = DirectMessenger(self.server, self.username, self.password)
            if self.direct_messenger:
                print('DirectMessenger Intialized')
            print(f"Connected to server: {self.server}")

            print('Creating Profile')
            self.profile = Profile(dsuserver=self.server, username=self.username, password=self.password)

            self.body._reset_ui()
        except Exception as e:
            tk.messagebox.showerror("Configuration Error", f"Failed to configure server: {e}")    


    def publish(self, message:str):
        # You must implement this!
        try:
            if self.direct_messenger and self.recipient:
                self.direct_messenger.send(message, self.recipient)
        except Exception as e:
            tk.messagebox.showerror("Publish Error", f"Failed to send message {e}")

    def check_new(self):
        # You must implement this!
        if self.direct_messenger:
            try:
                messages = self.direct_messenger.retrieve_new()
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
            except Exception as e:
                tk.messagebox.showerror("Publish Error", f"Failed to send message {e}")
        
        self.root.after(2000, self.check_new) 
    
    def create_file(self):
        try:
            filepath = filedialog.asksaveasfilename() + '.dsu'
            self.filepath = Path(filepath)
            self.filepath.touch()

            self.username = '' # Reset All Values for Server Configuration 
            self.password = ''
            self.server = ''
            self.recipient = ''
            self.direct_messenger = None

            self.configure_server()
            self.profile.save_profile(self.filepath)
        except Exception as e:
            tk.messagebox.showerror('File Creation Error', f'Failed to Create File: {e}')

    
    def open_file(self):
        try:
            filepath = filedialog.askopenfilename()
            if not filepath:
                return 
            
            self.body._reset_ui()

            self.filepath = Path(filepath)
            self.profile = Profile()
            self.profile.load_profile(self.filepath)

            self.username = self.profile.username
            self.password = self.profile.password
            self.server = self.profile.dsuserver

            self.direct_messenger = DirectMessenger(self.server, self.username, self.password)
            
            print(self.profile.friends)
            self.retrive_contacts()
        except Exception as e:
            tk.messagebox.showerror('File Opening Error', f'Failed to Open File: {e}')
    

    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.create_file)
        menu_file.add_command(label='Open...', command = self.open_file)
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    double = False

    if double == False:
        # All Tkinter programs start with a root window. We will name ours 'main'.
        main = tk.Tk()

        # 'title' assigns a text value to the Title Bar area of a window.
        main.title("ICS 32 Distributed Social Messenger")

        # This is just an arbitrary starting point. You can change the value
        # around to see how the starting size of the window changes.
        main.geometry("720x480")

        # adding this option removes some legacy behavior with menus that
        # some modern OSes don't support. If you're curious, feel free to comment
        # out and see how the menu changes.
        main.option_add('*tearOff', False)
        
        style = ttk.Style()
        style.theme_use('clam')

        sv_ttk.set_theme('dark')

        # Initialize the MainApp class, which is the starting point for the
        # widgets used in the program. All of the classes that we use,
        # subclass Tk.Frame, since our root frame is main, we initialize
        # the class with it.
        app = MainApp(main)

        # When update is called, we finalize the states of all widgets that
        # have been configured within the root frame. Here, update ensures that
        # we get an accurate width and height reading based on the types of widgets
        # we have used. minsize prevents the root window from resizing too small.
        # Feel free to comment it out and see how the resizing
        # behavior of the window changes.
        main.update()
        main.minsize(main.winfo_width(), main.winfo_height())
        id = main.after(2000, app.check_new)
        print(id)
        # And finally, start up the event loop for the program (you can find
        # more on this in lectures of week 9 and 10).
        main.mainloop()
    
    else:
        # Create two root windows
        main1 = tk.Tk()
        main2 = tk.Tk()

        # Set window titles
        main1.title("User 1 - ICS 32 Messenger")
        main2.title("User 2 - ICS 32 Messenger")

        # Create instances of MainApp for both users
        app1 = MainApp(main1)
        app2 = MainApp(main2)

        # Run both event loops
        main1.after(2000, app1.check_new)
        main2.after(2000, app2.check_new)

        main1.mainloop()
        main2.mainloop()
    
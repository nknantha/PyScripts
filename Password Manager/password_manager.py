"""
MyPass is a password manager with GUI.

:URL: https://github.com/nknantha/PyScripts/tree/main/Password%20Manager/password_manager.py
:Author: NanthaKumar<https://github.com/nknantha>
:Date: 2021/09/25
"""
import json
import random
import string
from tkinter import *
from tkinter import ttk, messagebox, font


class MyPass:

    TITLE = 'nPassM'
    DATA_FILE = 'data.json'

    WID_PAD_X = 5
    WID_PAD_Y = 5

    ROOT_PAD_X = 30
    ROOT_PAD_Y = 30

    PS_CHARS = string.ascii_letters + string.digits + '#$%^,()*+.:|=?@/[]_`{}\\!;-~'

    def __init__(self):

        # Setup window.
        self._root = Tk()
        self._root.title(self.TITLE)
        self._root.configure(padx=self.ROOT_PAD_X, pady=self.ROOT_PAD_Y)
        self._root.resizable(0, 0)

        # Setup Logo.
        self._image_file = PhotoImage(file='Images/logo.png')
        ttk.Label(master=self._root, image=self._image_file).grid(column=0, row=0,
                                                                  padx=self.WID_PAD_X,
                                                                  pady=self.WID_PAD_Y,
                                                                  columnspan=2)

        # Form Labels.
        new_font = font.Font(root=self._root, size=10)
        ttk.Label(master=self._root, text='Site', font=new_font).grid(column=0, row=1,
                                                                      padx=self.WID_PAD_X,
                                                                      pady=self.WID_PAD_Y, sticky=E)
        ttk.Label(master=self._root, text='Username', font=new_font).grid(column=0, row=2,
                                                                          padx=self.WID_PAD_X,
                                                                          pady=self.WID_PAD_Y, sticky=E)
        ttk.Label(master=self._root, text='Password', font=new_font).grid(column=0, row=3,
                                                                          padx=self.WID_PAD_X,
                                                                          pady=self.WID_PAD_Y, sticky=E)

        # Site Entry Frame.
        self._site_entry_frame = ttk.Frame(self._root)
        self._site_entry_frame.grid(column=1, row=1, padx=self.WID_PAD_X, pady=self.WID_PAD_Y,
                                    columnspan=2, sticky=NSEW)

        # Site Entry.
        self._site_entry = ttk.Entry(master=self._site_entry_frame)
        self._site_entry.pack(expand=True, fill=X, side=LEFT)
        self._site_entry.focus()

        # Search Button.
        self._search_button = ttk.Button(master=self._site_entry_frame, text='Search', command=self.__search)
        self._search_button.pack(side=LEFT)

        # Username Entry.
        self._username_entry = ttk.Entry(master=self._root)
        self._username_entry.grid(column=1, row=2, padx=self.WID_PAD_X, pady=self.WID_PAD_Y,
                                  columnspan=2, sticky=NSEW)

        # Password Button Frame.
        self._password_button_frame = ttk.Frame(master=self._root)
        self._password_button_frame.grid(column=1, row=3, padx=self.WID_PAD_X, pady=self.WID_PAD_Y)

        # Password Entry.
        self._password_entry_variable = StringVar()
        self._password_entry = ttk.Entry(master=self._password_button_frame,
                                         textvariable=self._password_entry_variable)
        self._password_entry.pack(expand=True, fill=X, side=LEFT)

        # Copy Button.
        self._copy_button = ttk.Button(master=self._password_button_frame, text='Copy',
                                       command=self.__copy_to_clipboard)
        self._copy_button.pack(side=LEFT)

        # Generate Button.
        self._generate_button = ttk.Button(master=self._password_button_frame, text='Generate',
                                           command=self.__generate)
        self._generate_button.pack(side=LEFT)

        # Generate Length Spinbox.
        self._length_spinbox_variable = IntVar()
        self._length_spinbox_variable.set(8)
        self._generate_length_spinbox = ttk.Spinbox(master=self._password_button_frame,
                                                    textvariable=self._length_spinbox_variable,
                                                    from_=8, to=40, increment=1, width=3, state='readonly')
        self._generate_length_spinbox.pack(side=LEFT)

        # Button Frame.
        self._button_frame = ttk.Frame(master=self._root)
        self._button_frame.grid(column=1, row=4, padx=self.WID_PAD_X, pady=self.WID_PAD_Y,
                                columnspan=2, sticky=NSEW)

        # Add Button.
        self._add_button = ttk.Button(master=self._button_frame, text='Add',
                                      default='active', command=self.__add_entry)
        self._add_button.pack(expand=True, fill=X, side=LEFT)

        # Clear Button.
        self._clear_button = ttk.Button(master=self._button_frame, text='Clear', command=self.__clear_entry)
        self._clear_button.pack(expand=True, fill=X, side=LEFT)

        # Window mainloop.
        self._root.mainloop()

    def __add_entry(self):

        entries = [entry.get().strip() for entry in (self._site_entry,
                                                     self._username_entry,
                                                     self._password_entry)]
        error = []
        err_msg_suffix = ' cannot be empty.'
        if entries[0] == '':
            error.append('- Site' + err_msg_suffix)
        if entries[1] == '':
            error.append('- Username' + err_msg_suffix)
        if entries[2] == '':
            error.append('- Password' + err_msg_suffix)

        if error:
            messagebox.showerror('Error', '\n'.join(error))
            return

        confirmation_msg = 'Site: ' + entries[0] \
                           + '\nUsername: ' + entries[1] \
                           + '\nPassword: ' + entries[2]
        if messagebox.askokcancel('Confirmation', 'Verify Details:\n' + confirmation_msg):
            messagebox.showinfo('Success', 'Credentials saved successfully.')

            try:
                with open(self.DATA_FILE) as f:
                    json_data = json.load(f)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                json_data = dict()

            index = '0'
            if json_data.get(entries[0]):
                index = str(len(json_data[entries[0]]))
                json_data[entries[0]].update({
                    index: {
                        'Username': entries[1],
                        'Password': entries[2]
                    }
                })
            else:
                json_data.update({
                    entries[0]: {
                        index: {
                            'Username': entries[1],
                            'Password': entries[2]
                        }
                    }
                })

            with open(self.DATA_FILE, 'w') as f:
                json.dump(json_data, f, indent=4)

            self.__clear_entry()

    def __clear_entry(self):
        for entry in (self._site_entry, self._username_entry, self._password_entry):
            entry.delete(0, END)

    def __copy_to_clipboard(self):
        self._root.clipboard_clear()
        self._root.clipboard_append(self._password_entry.get())
        self._root.update()

    def __generate(self):
        new_password = ''
        for _ in range(self._length_spinbox_variable.get()):
            new_password += random.choice(self.PS_CHARS)

        self._password_entry_variable.set(new_password)

    def __search(self):
        try:
            with open(self.DATA_FILE) as f:
                json_data = json.load(f)

            data = 'Credentials:'
            query_data = json_data[self._site_entry.get()]
            for index in query_data:
                data += f"\n\nIndex {int(index) + 1}:" \
                        f"\n    Username: {query_data[index]['Username']}" \
                        f"\n    Password: {query_data[index]['Password']}"
            messagebox.showinfo('Found', data)
        except FileNotFoundError:
            messagebox.showerror('Error', f"{'data.json'!r} file not found.")
        except json.decoder.JSONDecodeError:
            messagebox.showerror('Error', f"{'data.json'!r} file is corrupted.")
        except KeyError:
            messagebox.showerror('Error', f"{self._site_entry.get()!r} is not found.")


if __name__ == '__main__':
    MyPass()

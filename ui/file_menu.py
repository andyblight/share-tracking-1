import tkinter as tk

from ui.securities_menu import database


class FileMenu(tk.Menu):
    def __init__(self, parent, menu_bar):
        self.parent = parent
        self.menu_file = tk.Menu(menu_bar)
        self.menu_file.add_command(label="New", command=self.new)
        self.menu_file.add_command(label="Open", command=self.open)
        self.menu_file.add_command(label="Save", command=self.save)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=self.parent.quit)
        menu_bar.add_cascade(label="File", menu=self.menu_file)

    def new(self):
        print("File->New")
        # FIXME: Hack for now to have some data to show.
        # Create database if not present
        if not database.is_present():
            database.create()
            # FIXME: This is for testing the GUI.
            # Remove when done.
            database.add_fake_rows()

    def open(self):
        print("File->Open")

    def save(self):
        print("File->Save")

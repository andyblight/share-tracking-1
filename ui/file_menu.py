import tkinter as tk

from database.main import database


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
        # Create database with empty tables if not present
        if not database.is_present():
            database.create()

    def open(self):
        print("File->Open")
        if database.is_present():
            # FIXME: This is for testing the GUI.
            # Remove when done.
            database.add_test_rows()

    def save(self):
        print("File->Save")
        database.dump_tables()

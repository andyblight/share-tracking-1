from tkinter import ttk
import tkinter as tk

from database.main import database
from ui.dialog_about import AboutDialog
from ui.transactions import TransactionsTableView, AddTransactionDialog
from ui.securities import SecuritiesTableView, AddNewSecurityDialog


DEFAULT_APP_WIDTH = 800
DEFAULT_APP_HEIGHT = 500
VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_BUILD = 1

__program_name__ = "Share Tracker"


class HelpMenu(tk.Menu):
    def __init__(self, parent, menu_bar):
        self.parent = parent
        self.menu_help = tk.Menu(menu_bar)
        self.menu_help.add_command(label="Help Index", command=self.index)
        self.menu_help.add_command(label="About...", command=self.dialog_about)
        menu_bar.add_cascade(label="Help", menu=self.menu_help)

    def index(self):
        print("Help->Index")

    def dialog_about(self):
        print("Help->About")
        _ = AboutDialog(self.parent, __program_name__)


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


class SecuritiesMenu(tk.Menu):
    def __init__(self, parent, menu_bar):
        self.parent = parent
        self.menu_file = tk.Menu(menu_bar)
        self.menu_file.add_command(label="Add...", command=self.add)
        self.menu_file.add_command(label="Show", command=self.show)
        menu_bar.add_cascade(label="Securities", menu=self.menu_file)
        # Add treeview table on main window.
        self.table_view = SecuritiesTableView(self.parent)

    def add(self):
        # Create a new dialog box.
        _ = AddNewSecurityDialog(self.parent)

    def show(self):
        self.table_view.refresh()


class TransactionsMenu(tk.Menu):
    def __init__(self, parent, menu_bar):
        self.parent = parent
        self.menu_file = tk.Menu(menu_bar)
        self.menu_file.add_command(label="New...", command=self.new)
        self.menu_file.add_command(label="Show", command=self.show)
        menu_bar.add_cascade(label="Transactions", menu=self.menu_file)
        # Add treeview table on main window.
        self.table_view = TransactionsTableView(self.parent)

    def new(self):
        print("Transactions->New")
        # Create a new dialog box.
        _ = AddTransactionDialog(self.parent)

    def show(self):
        print("Transactions->Show")
        self.table_view.refresh()


class MenuBar(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        self.menu_bar = tk.Menu(parent)
        # File menu
        self.menu_file = FileMenu(parent, self.menu_bar)
        self.menu_securities = SecuritiesMenu(parent, self.menu_bar)
        self.menu_transactions = TransactionsMenu(parent, self.menu_bar)
        self.menu_help = HelpMenu(parent, self.menu_bar)
        # Finally, add the menu to the parent
        parent["menu"] = self.menu_bar


class UserInterface(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        # The parent window.
        self.parent = parent
        self.parent.title(__program_name__)
        self.parent.option_add("*tearOff", False)
        # Set size
        self.parent.geometry("{}x{}".format(DEFAULT_APP_WIDTH, DEFAULT_APP_HEIGHT))
        # Create simplest layout, grid of 1 x 1 using all of window.
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        # Add the menu bar.
        self.menu_bar = MenuBar(self.parent)

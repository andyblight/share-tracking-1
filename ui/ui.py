from tkinter import ttk
import tkinter as tk

from database.main import database
from ui.tabs import TabbedWindow
from ui.help import AboutDialog
from ui.transactions import AddTransactionDialog
from ui.securities import AddNewSecurityDialog


DEFAULT_APP_WIDTH = 800
DEFAULT_APP_HEIGHT = 500
VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_BUILD = 1

__program_name__ = "Share Tracker"


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
    def __init__(self, parent, menu_bar, tabbed_window):
        self.parent = parent
        self.tabbed_window = tabbed_window
        self.menu_file = tk.Menu(menu_bar)
        self.menu_file.add_command(label="Add...", command=self.add)
        self.menu_file.add_command(label="Show", command=self.show)
        menu_bar.add_cascade(label="Securities", menu=self.menu_file)

    def add(self):
        # Create a new dialog box.
        _ = AddNewSecurityDialog(self.parent)

    def show(self):
        print("Securities->Show")
        self.tabbed_window.show_securities()


class TransactionsMenu(tk.Menu):
    def __init__(self, parent, menu_bar, tabbed_window):
        self.parent = parent
        self.tabbed_window = tabbed_window
        self.menu_file = tk.Menu(menu_bar)
        self.menu_file.add_command(label="New...", command=self.new)
        self.menu_file.add_command(label="Show", command=self.show)
        menu_bar.add_cascade(label="Transactions", menu=self.menu_file)

    def new(self):
        print("Transactions->New")
        # Create a new dialog box.
        _ = AddTransactionDialog(self.parent)

    def show(self):
        print("Transactions->Show")
        self.tabbed_window.show_transactions()


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


class MenuBar:
    def __init__(self, parent, tabbed_window):
        self.parent = parent
        self.tabbed_window = tabbed_window
        self.menu_bar = tk.Menu(parent)
        # File menu
        self.menu_file = FileMenu(self.parent, self.menu_bar)
        self.menu_securities = SecuritiesMenu(
            self.parent, self.menu_bar, self.tabbed_window
        )
        self.menu_transactions = TransactionsMenu(
            self.parent, self.menu_bar, self.tabbed_window
        )
        self.menu_help = HelpMenu(self.parent, self.menu_bar)
        # Finally, add the menu to the parent
        parent["menu"] = self.menu_bar


class UserInterface:
    def __init__(self, root):
        # The parent window.
        self.root = root
        self.root.title(__program_name__)
        self.root.option_add("*tearOff", False)
        # Set size
        self.root.geometry("{}x{}".format(DEFAULT_APP_WIDTH, DEFAULT_APP_HEIGHT))
        # Create simplest layout, grid of 1 x 1 using all of window.
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        # Add the tabbed window.
        self.tabbed_window = TabbedWindow(self.root)
        # Add the menu bar.
        self.menu_bar = MenuBar(self.root, self.tabbed_window)
        self.tabbed_window.show_securities()

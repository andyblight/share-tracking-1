from tkinter import ttk
import tkinter as tk

from ui.file_menu import FileMenu
from ui.help_menu import HelpMenu
from ui.securities_menu import SecuritiesMenu
from ui.transactions_menu import TransactionsMenu

DEFAULT_APP_WIDTH = 800
DEFAULT_APP_HEIGHT = 500
VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_BUILD = 1

__program_name__ = "Share Tracker"


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

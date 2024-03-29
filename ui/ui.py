import tkinter as tk

# from tkinter import ttk

from database.main import database
from ui.tabbed_frame import TabbedFrame
from ui.help import AboutDialog
from ui.holdings_view import UpdateHoldingDialog
from ui.holdings_update_dialog import HoldingsUpdateDialog
from ui.securities_add_dialog import SecuritiesAddDialog
from ui.securities_import_dialog import SecuritiesImportDialog
from ui.transactions_add_dialog import TransactionsAddDialog
from ui.transactions_import_dialog import TransactionsImportDialog


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
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=self.parent.quit)
        menu_bar.add_cascade(label="File", menu=self.menu_file)

    def new(self):
        print("File->New")
        # Create database with empty tables if not present
        database.create()

    def open(self):
        print("File->Open")
        if database.is_present():
            # FIXME: This is for testing the GUI.
            # Remove when done.
            database.add_test_rows()


class SummaryMenu(tk.Menu):
    def __init__(self, parent, menu_bar, tabbed_frame):
        self.parent = parent
        self.tabbed_frame = tabbed_frame
        self.menu_file = tk.Menu(menu_bar)
        self.menu_file.add_command(label="Show", command=self.show)
        menu_bar.add_cascade(label="Summary", menu=self.menu_file)

    def show(self):
        print("Summary->Show")
        self.tabbed_frame.show_summary()


class HoldingsMenu(tk.Menu):
    def __init__(self, parent, menu_bar, tabbed_frame):
        self.parent = parent
        self.tabbed_frame = tabbed_frame
        self.menu_file = tk.Menu(menu_bar)
        self.menu_file.add_command(label="Manual update...", command=self.add)
        self.menu_file.add_command(label="Show", command=self.show)
        self.menu_file.add_command(
            label="Update from transactions...", command=self.update
        )
        menu_bar.add_cascade(label="Holdings", menu=self.menu_file)

    def add(self):
        # Create a new dialog box.
        dialog = UpdateHoldingDialog(self.parent)
        dialog.import_file()

    def show(self):
        print("Holdings->Show")
        self.tabbed_frame.show_holdings()

    def update(self):
        print("Holdings->Update")
        _ = HoldingsUpdateDialog(self.parent)


class SecuritiesMenu(tk.Menu):
    def __init__(self, parent, menu_bar, tabbed_frame):
        self.parent = parent
        self.tabbed_frame = tabbed_frame
        self.menu_file = tk.Menu(menu_bar)
        self.menu_file.add_command(label="Add...", command=self.add)
        self.menu_file.add_command(label="Import...", command=self.import_file)
        self.menu_file.add_command(label="Show", command=self.show)
        menu_bar.add_cascade(label="Securities", menu=self.menu_file)

    def add(self):
        # Create a new dialog box.
        _ = SecuritiesAddDialog(self.parent)

    def import_file(self):
        dialog = SecuritiesImportDialog(self.parent)
        dialog.import_file()

    def show(self):
        print("Securities->Show")
        self.tabbed_frame.show_securities()


class TransactionsMenu(tk.Menu):
    def __init__(self, parent, menu_bar, tabbed_frame):
        self.parent = parent
        self.tabbed_frame = tabbed_frame
        self.menu_file = tk.Menu(menu_bar)
        self.menu_file.add_command(label="New...", command=self.new)
        self.menu_file.add_command(label="Import...", command=self.import_file)
        self.menu_file.add_command(label="Show", command=self.show)
        menu_bar.add_cascade(label="Transactions", menu=self.menu_file)

    def new(self):
        _ = TransactionsAddDialog(self.parent)

    def import_file(self):
        dialog = TransactionsImportDialog(self.parent)
        dialog.import_file()

    def show(self):
        print("Transactions->Show")
        self.tabbed_frame.show_transactions()


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
    def __init__(self, parent, tabbed_frame):
        self.parent = parent
        self.tabbed_frame = tabbed_frame
        self.menu_bar = tk.Menu(parent)
        # File menu
        self.menu_file = FileMenu(self.parent, self.menu_bar)
        self.menu_holdings = SummaryMenu(self.parent, self.menu_bar, self.tabbed_frame)
        self.menu_holdings = HoldingsMenu(self.parent, self.menu_bar, self.tabbed_frame)
        self.menu_securities = SecuritiesMenu(
            self.parent, self.menu_bar, self.tabbed_frame
        )
        self.menu_transactions = TransactionsMenu(
            self.parent, self.menu_bar, self.tabbed_frame
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
        # Add the tabbed frame.
        self.tabbed_frame = TabbedFrame(self.root)
        # Add the menu bar.
        self.menu_bar = MenuBar(self.root, self.tabbed_frame)
        # Show holdings tab by default.
        self.tabbed_frame.show_holdings()

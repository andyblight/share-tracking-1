# noqa: E501 From: https://www.activestate.com/resources/quick-reads/how-to-display-data-in-a-table-using-tkinter/

from tkinter import ttk
import tkinter as tk
from database.securities import SecuritiesDatabase

DEFAULT_APP_WIDTH = 800
DEFAULT_APP_HEIGHT = 500

database = SecuritiesDatabase()


class DisplayTab(ttk.Frame):
    def __init__(self, notebook):
        # The frame.
        self.frame = ttk.Frame.__init__(self, notebook)
        # The table list
        self.treeview = ttk.Frame(self.frame, borderwidth=4, relief="ridge")
        # This shows the frame.
        self.treeview.grid(column=0, row=0)
        columns = ("ticker", "name", "quantity", "price")
        self.tree = ttk.Treeview(self.treeview, columns=columns, show="headings")
        self.tree.grid(column=0, row=0)
        # Define headings
        self.tree.heading("ticker", text="Ticker")
        self.tree.column("ticker", width=100)
        self.tree.heading("name", text="Name")
        self.tree.column("name", width=200)
        self.tree.heading("quantity", text="Quantity")
        self.tree.column("quantity", width=100, anchor="e")
        self.tree.heading("price", text="Price")
        self.tree.column("price", width=100, anchor="e")
        # The refresh button
        refresh_button = tk.Button(self.frame, text="Refresh", command=self.view)
        refresh_button.grid(column=0, row=1)
        # FIXME: Hack for now to have some data to show.
        # Create database if not present
        if not database.is_present():
            database.create()
            database.add_rows()

    def view(self):
        all_rows = database.get_all_rows()
        for row in all_rows:
            print(row)
            self.tree.insert("", tk.END, values=row)


class AddSecurityTab(ttk.Frame):
    def __init__(self, notebook):
        # The frame.
        self.frame = ttk.Frame.__init__(self, notebook)
        data_entry_label_frame = ttk.LabelFrame(
            self.frame, text="Enter new security details"
        )
        data_entry_label_frame.grid(column=0, row=0)
        # Ticker label frame
        stock_ticker_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Ticker")
        stock_ticker_entry = ttk.Entry(stock_ticker_label_frame)
        stock_ticker_entry.grid(column=0, row=0)
        # Name label frame
        stock_name_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Name")
        stock_name_entry = ttk.Entry(stock_name_label_frame)
        stock_name_entry.grid(column=0, row=0)
        # Quantity label frame
        stock_quantity_label_frame = ttk.LabelFrame(
            data_entry_label_frame, text="Quantity"
        )
        stock_quantity_entry = ttk.Entry(stock_quantity_label_frame)
        stock_quantity_entry.grid(column=0, row=0)
        # Price label frame
        stock_price_label_frame = ttk.LabelFrame(
            data_entry_label_frame, text="Price (GBX)"
        )
        stock_price_entry = ttk.Entry(stock_price_label_frame)
        stock_price_entry.grid(column=0, row=0)
        # Button
        self.add_new_button = tk.Button(
            data_entry_label_frame, text="Add", command=self.add_new
        )
        # Position label frames
        stock_ticker_label_frame.grid(column=0, row=0)
        stock_name_label_frame.grid(column=1, row=0, columnspan=2)
        stock_quantity_label_frame.grid(column=3, row=0)
        stock_price_label_frame.grid(column=4, row=0)
        # Keep the button on the left.
        self.add_new_button.grid(column=0, row=2, sticky="w")

    def add_new(args):
        pass


class FileMenu(tk.Menu):
    def __init__(self, menu_bar):
        self.menu_file = tk.Menu(menu_bar)
        self.menu_file.add_command(label="New", command=self.do_nothing)
        self.menu_file.add_command(label="Open", command=self.do_nothing)
        self.menu_file.add_command(label="Save", command=self.do_nothing)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=root.quit)
        menu_bar.add_cascade(label="File", menu=self.menu_file)

    def do_nothing(self):
        pass


class SecuritiesMenu(tk.Menu):
    def __init__(self, menu_bar):
        self.menu_file = tk.Menu(menu_bar)
        self.menu_file.add_command(label="Add...", command=self.do_nothing)
        self.menu_file.add_command(label="Show", command=self.do_nothing)
        menu_bar.add_cascade(label="Securities", menu=self.menu_file)

    def do_nothing(self):
        pass


class TransactionsMenu(tk.Menu):
    def __init__(self, menu_bar):
        self.menu_file = tk.Menu(menu_bar)
        self.menu_file.add_command(label="New...", command=self.do_nothing)
        self.menu_file.add_command(label="Show", command=self.do_nothing)
        menu_bar.add_cascade(label="Transactions", menu=self.menu_file)

    def do_nothing(self):
        pass


class HelpMenu(tk.Menu):
    def __init__(self, menu_bar):
        self.menu_help = tk.Menu(menu_bar)
        self.menu_help.add_command(label="Help Index", command=self.do_nothing)
        self.menu_help.add_command(label="About...", command=self.do_nothing)
        menu_bar.add_cascade(label="Help", menu=self.menu_help)

    def do_nothing(self):
        pass


class MenuBar(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        self.menu_bar = tk.Menu(parent)
        # File menu
        self.menu_file = FileMenu(self.menu_bar)
        self.menu_securities = SecuritiesMenu(self.menu_bar)
        self.menu_transactions = TransactionsMenu(self.menu_bar)
        self.menu_help = HelpMenu(self.menu_bar)
        # Finally, add the menu to the parent
        parent["menu"] = self.menu_bar


class MainApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        # The window?
        self.parent = parent
        self.parent.title("Share Tracker 1")
        self.parent.option_add("*tearOff", False)
        # Set size
        self.parent.geometry("{}x{}".format(DEFAULT_APP_WIDTH, DEFAULT_APP_HEIGHT))
        # Create simplest layout, grid of 1 x 1 using all of window.
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        # Add two tabbed frames.
        # self.notebook = ttk.Notebook(root)
        # # Use sticky to ensure the tabs resize with the window.
        # self.notebook.grid(sticky="nsew")
        # # Create the frames for each page.
        # self.display_tab = DisplayTab(self.notebook)
        # self.display_tab.grid(sticky="nsew")
        # self.add_security_tab = AddSecurityTab(self.notebook)
        # self.add_security_tab.grid(sticky="nsew")
        # # Add frames to notebook.
        # self.notebook.add(self.display_tab, text="Display")
        # self.notebook.add(self.add_security_tab, text="Add Security")
        # Add menu bar.
        self.menu_bar = MenuBar(self.parent)


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()

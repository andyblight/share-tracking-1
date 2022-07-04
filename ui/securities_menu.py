from tkinter import ttk
import tkinter as tk

from database.main import database


class AddNewSecurityDialog:
    def __init__(self, parent):
        # Set up new window.
        self.parent = parent
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Add security")
        self.dialog.geometry("500x400")
        self.dialog.grid_rowconfigure(0, pad=10, weight=1)
        self.dialog.grid_columnconfigure(0, pad=10, weight=1)
        # Create windows sized frame.
        self.frame = ttk.Frame(self.dialog, borderwidth=4, relief="ridge")
        self.frame.grid(sticky="nesw")
        # Add data field.
        data_entry_label_frame = ttk.LabelFrame(
            self.frame, text="Enter new security details"
        )
        data_entry_label_frame.grid(column=0, row=0, sticky="new")
        # Ticker label frame
        stock_ticker_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Ticker")
        self.stock_ticker_entry = ttk.Entry(stock_ticker_label_frame)
        self.stock_ticker_entry.grid(column=0, row=0)
        # Name label frame
        stock_name_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Name")
        self.stock_name_entry = ttk.Entry(stock_name_label_frame)
        self.stock_name_entry.grid(sticky="ew")
        # Position label frames
        stock_ticker_label_frame.grid(column=0, row=0)
        stock_name_label_frame.grid(column=0, row=1, columnspan=2, sticky="ew")
        # Buttons
        self.add_new_button = tk.Button(
            data_entry_label_frame, text="Add", command=self.add
        )
        self.cancel_button = tk.Button(
            data_entry_label_frame, text="Cancel", command=self.cancel
        )
        # Keep the button on the left.
        self.add_new_button.grid(column=0, row=4)
        self.cancel_button.grid(column=1, row=4)

    def validate_ticker(self, ticker):
        valid = False
        if len(ticker) > 2 and len(ticker) < 5:
            valid = True
        return valid

    def validate_name(self, name):
        valid = False
        if len(name) > 2:
            valid = True
        return valid

    def add(self):
        print("SecurityDialog Add")
        # Get info from entry boxes.
        ticker = self.stock_ticker_entry.get()
        name = self.stock_name_entry.get()
        print("add: " + ticker + ", " + name)
        # Validate info.
        valid = self.validate_ticker(ticker)
        if valid:
            valid = self.validate_name(name)
            if valid:
                # Write to database.
                database.securities.add_row(ticker, name)

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()


class SecuritiesTableView:
    def __init__(self, parent):
        self.parent = parent
        # Create and show window sized frame.
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(sticky="nesw")
        # Create treeview of database.
        self.treeview_frame = ttk.Frame(self.frame, borderwidth=4, relief="ridge")
        # This shows the frame.
        self.treeview_frame.grid(column=0, row=0)
        columns = ("ticker", "name", "quantity", "price")
        self.tree = ttk.Treeview(self.treeview_frame, columns=columns, show="headings")
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
        refresh_button = tk.Button(self.frame, text="Refresh", command=self.refresh)
        refresh_button.grid(column=0, row=1)
        # Allow scrolling.

    def refresh(self):
        # print("refresh")
        for item in self.tree.get_children():
            self.tree.delete(item)
        all_rows = database.securities.get_all_rows()
        for row in all_rows:
            # print(row)
            self.tree.insert("", tk.END, values=row)


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

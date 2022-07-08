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
        self.stock_name_entry.grid(sticky="news")
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
        # Position buttons.
        self.add_new_button.grid(column=0, row=4)
        self.cancel_button.grid(column=1, row=4)

    def validate_ticker(self, ticker):
        valid = False
        if len(ticker) > 2 and len(ticker) < 20:
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
        # Write to database.
        database.securities.add_row(ticker, name)

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()


class SecuritiesTableView(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # Create and show window sized frame.
        self.grid(sticky="nesw")
        # Create treeview of database.
        self.configure(borderwidth=4, relief="ridge")
        # This shows the frame.
        self.grid(column=0, row=0)
        # Create treeview.
        columns = ("uid", "ticker", "name")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.grid(column=0, row=0)
        # Define headings
        self.tree.heading("uid", text="UID")
        self.tree.column("uid", width=40)
        self.tree.heading("ticker", text="Ticker")
        self.tree.column("ticker", width=100)
        self.tree.heading("name", text="Name")
        self.tree.column("name", width=200)
        # Allow scrolling.
        self.ytree_scroll = ttk.Scrollbar(
            master=self, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.ytree_scroll.grid(row=0, column=2, sticky="nse")
        self.tree.configure(yscrollcommand=self.ytree_scroll.set)
        self.xtree_scroll = ttk.Scrollbar(
            master=self, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        self.xtree_scroll.grid(row=1, column=0, columnspan=2, sticky="ews")
        self.tree.configure(xscrollcommand=self.xtree_scroll.set)

    def show(self):
        self.tkraise()
        for item in self.tree.get_children():
            self.tree.delete(item)
        all_rows = database.securities.get_all_rows()
        for row in all_rows:
            # print(row)
            self.tree.insert("", tk.END, values=row)

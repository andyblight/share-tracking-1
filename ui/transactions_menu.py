import tkinter as tk
from tkinter import ttk
from datetime import datetime, date
from database.main import database

class AddTransactionDialog:
    def __init__(self, parent):
        # Set up new window.
        self.parent = parent
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Add transaction")
        self.dialog.geometry("900x250")
        self.dialog.grid_rowconfigure(0, pad=10, weight=1)
        self.dialog.grid_columnconfigure(0, pad=10, weight=1)
        # Create windows sized frame.
        self.frame = ttk.Frame(self.dialog, borderwidth=4, relief="ridge")
        self.frame.grid(sticky="nesw")
        # Add data field.
        data_entry_label_frame = ttk.LabelFrame(
            self.frame, text="Enter transaction details"
        )
        data_entry_label_frame.grid(column=0, row=0, sticky="new")
        # Date label frame.
        date_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Date")
        self.date_entry = ttk.Entry(date_label_frame)
        self.date_entry.grid(column=0, row=0)
        # Buy or sell label frame.
        # TODO Change to check boxes.
        buy_sell_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Buy/Sell")
        self.buy_sell_entry = ttk.Entry(buy_sell_label_frame)
        self.buy_sell_entry.grid(sticky="ew")
        # Security label frame.
        # TODO Choose from pull down.
        security_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Security")
        self.security_entry = ttk.Entry(security_label_frame)
        self.security_entry.grid(sticky="ew")
        # Quantity label frame.
        quantity_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Quantity")
        self.quantity_entry = ttk.Entry(quantity_label_frame)
        self.quantity_entry.grid(sticky="ew")
        # Price label frame.
        price_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Price")
        self.price_entry = ttk.Entry(price_label_frame)
        self.price_entry.grid(sticky="ew")
        # Fees label frame.
        fees_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Fees")
        self.fees_entry = ttk.Entry(fees_label_frame)
        self.fees_entry.grid(sticky="ew")
        # Tax label frame.
        tax_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Tax")
        self.tax_entry = ttk.Entry(tax_label_frame)
        self.tax_entry.grid(sticky="ew")
        # Total label frame.
        total_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Total")
        self.total_entry = ttk.Entry(total_label_frame)
        self.total_entry.grid(sticky="ew")
        # Position label frames.
        date_label_frame.grid(column=0, row=0)
        buy_sell_label_frame.grid(column=1, row=0)
        security_label_frame.grid(column=2, row=0, columnspan=2, sticky="ew")
        quantity_label_frame.grid(column=0, row=1)
        price_label_frame.grid(column=1, row=1)
        fees_label_frame.grid(column=2, row=1)
        tax_label_frame.grid(column=3, row=1)
        total_label_frame.grid(column=4, row=1)
        # Buttons
        self.add_new_button = tk.Button(
            data_entry_label_frame, text="Add", command=self.add
        )
        self.cancel_button = tk.Button(
            data_entry_label_frame, text="Cancel", command=self.cancel
        )
        # Place buttons.
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


class TransactionsTableView:
    def __init__(self, parent):
        self.parent = parent
        # Create and show window sized frame.
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(sticky="nesw")
        # Create treeview of transactions_table.
        self.treeview_frame = ttk.Frame(self.frame, borderwidth=4, relief="ridge")
        # This shows the frame.
        self.treeview_frame.grid(column=0, row=0)
        columns = (
            "uid",
            "type",
            "date",
            "security_id",
            "quantity",
            "price",
            "fees",
            "tax",
            "total",
        )
        self.tree = ttk.Treeview(self.treeview_frame, columns=columns, show="headings")
        self.tree.grid(column=0, row=0)
        # Define headings
        self.tree.heading("uid", text="UID")
        self.tree.column("uid", width=40)
        self.tree.heading("type", text="B/S")
        self.tree.column("type", width=40)
        self.tree.heading("date", text="Date")
        self.tree.column("date", width=120)
        self.tree.heading("security_id", text="SID")
        self.tree.column("security_id", width=40)
        self.tree.heading("quantity", text="Quantity")
        self.tree.column("quantity", width=80)
        self.tree.heading("price", text="Price")
        self.tree.column("price", width=80)
        self.tree.heading("fees", text="Fees")
        self.tree.column("fees", width=80)
        self.tree.heading("tax", text="Tax")
        self.tree.column("tax", width=80)
        self.tree.heading("total", text="Total")
        self.tree.column("total", width=80)
        # The refresh button
        refresh_button = tk.Button(self.frame, text="Refresh", command=self.refresh)
        refresh_button.grid(column=0, row=1)
        # Allow scrolling.
        # TODO

    def refresh(self):
        print("refresh")
        # Delete the existing data.
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Get all rows of data and add to the treeview object.
        all_rows = database.transactions.get_all_rows()
        for row in all_rows:
            print(row)
            # Convert row into correct format for treeview.
            row_max_index = len(row) - 1
            treeview_row = []
            for i in range(0, row_max_index):
                print("index", i, row[i])
                if i == 2:
                    # Convert datetime string from database into a date string.
                    datetime_str = row[i]
                    print(datetime_str)
                    datetime_obj = datetime.fromisoformat(datetime_str)
                    date_str = datetime_obj.date().isoformat()
                    print(date_str)
                    treeview_row.append(date_str)
                else:
                    treeview_row.append(row[i])
            self.tree.insert("", tk.END, values=treeview_row)


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

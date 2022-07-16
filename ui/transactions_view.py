import tkinter as tk
from tkinter import ttk
from datetime import datetime
from database.main import database
from ui.utils import float_to_currency


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
        # costs label frame.
        costs_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Costs")
        self.costs_entry = ttk.Entry(costs_label_frame)
        self.costs_entry.grid(sticky="ew")
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
        costs_label_frame.grid(column=2, row=1)
        total_label_frame.grid(column=4, row=1)
        # Buttons
        self.validate_button = tk.Button(
            data_entry_label_frame, text="Validate", command=self.validate
        )
        self.add_new_button = tk.Button(
            data_entry_label_frame, text="Add", command=self.add
        )
        self.cancel_button = tk.Button(
            data_entry_label_frame, text="Cancel", command=self.cancel
        )
        # Place buttons.
        self.validate_button.grid(column=0, row=2)
        self.add_new_button.grid(column=1, row=2)
        self.cancel_button.grid(column=2, row=2)

    def add(self):
        print("SecurityDialog Add")
        # Get info from entry boxes.
        date_entered = self.date_entry.get()
        buy_sell = self.buy_sell_entry.get()
        security = self.security_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        costs = self.costs_entry.get()
        total = self.total_entry.get()
        # Convert values.
        security_id = self._convert_security_id(security)
        numerics = self._convert_numerics(quantity, price, costs, total)
        # If all values are valid, write the data.
        if security_id[0] and numerics[0]:
            database.transactions.add_row(
                buy_sell,
                date_entered,
                security_id[1],
                numerics[1][0],
                numerics[1][1],
                numerics[1][2],
                numerics[1][3],
            )

    def _convert_security_id(self, security_string):
        # TODO Look up in securities table.
        # Convert string to int.
        valid = False
        result = 0.0
        try:
            result = int(security_string)
            valid = True
        except ValueError:
            print("Error. '{}' should be a valid security Id.".format(security_string))
        return (valid, result)

    def _to_float(self, value):
        valid = False
        result = 0.0
        try:
            result = float(value)
            valid = True
        except ValueError:
            print("Error. '{}' should be a valid number.".format(value))
        return (valid, result)

    def _convert_numerics(self, quantity, price, costs, total):
        # print(locals())
        # Save dictionary of parameter values.
        values = locals()
        # print(values)
        # Remove self as not a float.
        _ = values.pop("self")
        # Convert all other values to floats.
        results = []
        valid = True
        for key, value in values.items():
            if value is not None:
                value_result = self._to_float(value)
                if value_result[0]:
                    results.append(value_result[1])
                else:
                    print(key, value, " is not a float")
                    valid = False
        return (valid, results)

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()

    def validate(self):
        # Get info from entry boxes.
        date_entered = self.date_entry.get()
        buy_sell = self.buy_sell_entry.get()
        security = self.security_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        costs = self.costs_entry.get()
        total = self.total_entry.get()
        # Validate info.
        write = 0
        write += self.validate_date(date_entered)
        write += self.validate_buy_sell(buy_sell)
        write += self.validate_security(security)
        write += self.validate_quantity(quantity)
        write += self.validate_currency(price)
        write += self.validate_currency(costs)
        write += self.validate_total(quantity, price, costs, total)
        if write > 0:
            print("One or more fields are invalid.")
            # TODO Add some logic here.

    def validate_buy_sell(self, buy_sell_string):
        invalid = 0
        # print(buy_sell_string)
        if not buy_sell_string[0] in "BbSs":
            print("Must be one of 'BbSs'. Given ", buy_sell_string)
            invalid = 1
        return invalid

    def validate_currency(self, value):
        invalid = 0
        # TODO Improve this so there is some other sort of checking?
        try:
            float(value)
        except ValueError:
            print("Incorrect currency format. Should be a valid number.")
            invalid = 1
        return invalid

    def validate_date(self, date_string):
        invalid = 0
        # print(date_string)
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
        except (ValueError, AttributeError):
            print("Incorrect date format, should be YYYY-MM-DD")
            invalid = 1
        return invalid

    def validate_security(self, security_string):
        invalid = 0
        # print(security_string)
        # TODO Should check for presence in database.
        return invalid

    def validate_quantity(self, quantity_string):
        invalid = 0
        # print(quantity_string)
        try:
            float(quantity_string)
        except ValueError:
            print("Invalid quantity. Should be a valid number.")
            invalid = 1
        return invalid

    # def validate_total(self, quantity, price, costs, total):
    # invalid = 0
    # try:
    #     float(quantity_string)
    # except ValueError:
    #     print("Invalid quantity. Should be a valid number.")
    #     invalid = 1
    # return invalid
    # write += self.validate_total(quantity, price, costs, total)


class TransactionsTableView(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # Create and show window sized frame.
        self.grid(sticky="news")
        self.configure(borderwidth=4, relief="ridge")
        # This shows the frame.
        self.grid(column=0, row=0)
        # Create treeview of transactions_table.
        columns = (
            "uid",
            "date",
            "type",
            "security_id",
            "quantity",
            "price",
            "costs",
            "total",
        )
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.grid(column=0, row=0)
        # Define headings
        self.tree.heading("uid", text="UID", anchor=tk.E)
        self.tree.column("uid", width=40)
        self.tree.heading("date", text="Date")
        self.tree.column("date", width=120)
        self.tree.heading("type", text="B/S")
        self.tree.column("type", width=40)
        self.tree.heading("security_id", text="SID")
        self.tree.column("security_id", width=40, anchor=tk.E)
        self.tree.heading("quantity", text="Quantity")
        self.tree.column("quantity", width=80, anchor=tk.E)
        self.tree.heading("price", text="Price")
        self.tree.column("price", width=80, anchor=tk.E)
        self.tree.heading("costs", text="costs")
        self.tree.column("costs", width=80, anchor=tk.E)
        self.tree.heading("total", text="Total")
        self.tree.column("total", width=80, anchor=tk.E)
        # Add scroll bars.
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
        # Delete the existing data.
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Get all rows of data and add to the treeview object.
        all_rows = database.transactions.get_all_rows()
        for row in all_rows:
            # print(row)
            # Convert row into correct format for treeview.
            row_max_index = len(row)
            treeview_row = []
            for i in range(0, row_max_index):
                # print("index", i, row[i])
                if i in (4, 5, 6, 7, 8):
                    currency_str = float_to_currency(row[i])
                    treeview_row.append(currency_str)
                else:
                    treeview_row.append(row[i])
            # print(treeview_row)
            self.tree.insert("", tk.END, values=treeview_row)

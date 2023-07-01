import tkinter as tk
from tkinter import ttk
from babel.dates import format_date

from database.main import database
from ui.utils import float_to_currency


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
            "sid",
            "quantity",
            "price",
            "costs",
            "total",
        )
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.grid(column=0, row=0)
        # Define headings
        self.tree.heading("uid", text="UID")
        self.tree.column("uid", width=40, anchor=tk.E)
        self.tree.heading("date", text="Date")
        self.tree.column("date", width=90, anchor=tk.E)
        self.tree.heading("type", text="B/S")
        self.tree.column("type", width=40)
        self.tree.heading("sid", text="SID")
        self.tree.column("sid", width=40, anchor=tk.E)
        self.tree.heading("quantity", text="Quantity")
        self.tree.column("quantity", width=80, anchor=tk.E)
        self.tree.heading("price", text="Price")
        self.tree.column("price", width=70, anchor=tk.E)
        self.tree.heading("costs", text="Costs")
        self.tree.column("costs", width=70, anchor=tk.E)
        self.tree.heading("total", text="Total")
        self.tree.column("total", width=90, anchor=tk.E)
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
            treeview_row = []
            treeview_row.append(row.uid)
            # FIXME Hardcoded date format.
            date_string = format_date(row.date_obj, format="short", locale="en_GB")
            treeview_row.append(date_string)
            treeview_row.append(row.type)
            treeview_row.append(row.sid)
            currency_str = float_to_currency(row.quantity)
            treeview_row.append(currency_str)
            currency_str = float_to_currency(row.price)
            treeview_row.append(currency_str)
            currency_str = float_to_currency(row.costs)
            treeview_row.append(currency_str)
            currency_str = float_to_currency(row.total)
            treeview_row.append(currency_str)
            # print(treeview_row)
            self.tree.insert("", tk.END, values=treeview_row)

import tkinter as tk
from tkinter import ttk
from datetime import datetime
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

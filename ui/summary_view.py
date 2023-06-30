import tkinter as tk
from tkinter import ttk

from database.main import database
from ui.utils import float_to_currency


class SummaryTableView(ttk.Frame):
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
        columns = (
            "uid",
            "date",
            "sid",
            "quantity",
            "price",
            "value",
            "stop_loss",
            "target",
            "total",
        )
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.grid(column=0, row=0)
        # Define headings
        self.tree.heading("uid", text="UID")
        self.tree.column("uid", width=40, anchor=tk.E)
        self.tree.heading("date", text="Date")
        self.tree.column("date", width=160, anchor=tk.E)
        self.tree.heading("sid", text="SID")
        self.tree.column("sid", width=40, anchor=tk.E)
        self.tree.heading("quantity", text="Quantity")
        self.tree.column("quantity", width=80, anchor=tk.E)
        self.tree.heading("price", text="Price")
        self.tree.column("price", width=70, anchor=tk.E)
        self.tree.heading("value", text="Value")
        self.tree.column("value", width=70, anchor=tk.E)
        self.tree.heading("stop_loss", text="S/L")
        self.tree.column("stop_loss", width=70, anchor=tk.E)
        self.tree.heading("target", text="Target")
        self.tree.column("target", width=70, anchor=tk.E)
        self.tree.heading("total", text="Total")
        self.tree.column("total", width=90, anchor=tk.E)
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
        for item in self.tree.get_children():
            self.tree.delete(item)
        all_rows = database.holdings.get_all_rows()
        for row in all_rows:
            # Convert row into correct format for treeview.
            treeview_row = []
            treeview_row.append(row.uid)
            treeview_row.append(row.date_obj)
            treeview_row.append(row.sid)
            treeview_row.append(row.quantity)
            treeview_row.append(float_to_currency(row.price))
            treeview_row.append(float_to_currency(row.value))
            treeview_row.append(float_to_currency(row.stop_loss))
            treeview_row.append(float_to_currency(row.target))
            treeview_row.append(float_to_currency(row.total))
            # Add new row to treeview.
            self.tree.insert("", tk.END, values=treeview_row)

import tkinter as tk
from tkinter import ttk
from babel.dates import format_date

from database.main import database
from ui.utils import float_to_currency


class UpdateHoldingDialog:
    def __init__(self, parent):
        # Set up new window.
        self.parent = parent
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Update holding")
        self.dialog.geometry("500x400")
        self.dialog.grid_rowconfigure(0, pad=10, weight=1)
        self.dialog.grid_columnconfigure(0, pad=10, weight=1)
        # Create windows sized frame.
        self.frame = ttk.Frame(self.dialog, borderwidth=4, relief="ridge")
        self.frame.grid(sticky="nesw")
        # Add data field.
        data_entry_label_frame = ttk.LabelFrame(self.frame, text="Select holding")
        data_entry_label_frame.grid(column=0, row=0, sticky="new")
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

    def add(self):
        print("UpdateHoldingDialog Add")
        # Get info from entry boxes.

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()


class HoldingsTableView(ttk.Frame):
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
        self.tree.column("date", width=90, anchor=tk.E)
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
            # FIXME Hardcoded date format.
            date_string = format_date(row.date_obj, format="short", locale="en_GB")
            treeview_row.append(date_string)
            treeview_row.append(row.sid)
            treeview_row.append(row.quantity)
            treeview_row.append(float_to_currency(row.price))
            treeview_row.append(float_to_currency(row.value))
            treeview_row.append(float_to_currency(row.stop_loss))
            treeview_row.append(float_to_currency(row.target))
            treeview_row.append(float_to_currency(row.total))
            # Add new row to treeview.
            self.tree.insert("", tk.END, values=treeview_row)

from tkinter import ttk
import tkinter as tk

from database.main import database


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
        self.tree.column("date", width=80)
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
        # print("refresh")
        for item in self.tree.get_children():
            self.tree.delete(item)
        all_rows = database.transactions.get_all_rows()
        for row in all_rows:
            # print(row)
            self.tree.insert("", tk.END, values=row)


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

    def show(self):
        print("Transactions->Show")
        self.table_view.refresh()

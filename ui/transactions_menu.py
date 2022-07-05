import tkinter as tk
from tkinter import ttk
from datetime import datetime, date
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

    def show(self):
        print("Transactions->Show")
        self.table_view.refresh()

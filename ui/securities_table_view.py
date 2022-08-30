import tkinter as tk
from tkinter import ttk

from database.main import database


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
        self.tree.column("name", width=400)
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
        # Bind functions for selection and double click
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.bind("<Double-1>", self.on_double_click)

    def show(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        all_rows = database.securities.get_all_rows()
        for row in all_rows:
            # print(row)
            self.tree.insert("", tk.END, values=row)

    def show_rows(self, rows) -> None:
        print("sr")

    def on_double_click(self, event) -> None:
        print("odc", event)
        item = self.tree.selection()[0]
        print("you clicked on", self.tree.item(item,"text"))
        # Use the UID is first in the list.
        self._selected = item[0]

    def on_select(self, event) -> None:
        print("os", event)
        item_id  = self.tree.focus()
        item = self.tree.item(item_id)
        print("os", item_id,  ",", item)
        uid = item["values"][0]
        print("os", uid)

    def get_selected(self) -> int:
        return self._selected

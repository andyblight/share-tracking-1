import tkinter as tk
from tkinter import ttk

from ui.transactions import TransactionsTableView
from ui.securities import SecuritiesTableView


class TabbedWindow:
    def __init__(self, parent):
        self.parent = parent
        self.notebook = ttk.Notebook(self.parent)
        # Create the views for each tab.
        self.securities_table_view = SecuritiesTableView(self.parent)
        self.transactions_table_view = TransactionsTableView(self.parent)
        # Add views to tabbed window.
        self.notebook.add(
            child=self.securities_table_view, sticky="news", text="Securities"
        )
        self.notebook.add(
            child=self.transactions_table_view, sticky="news", text="Transactions"
        )
        self.notebook.grid(column=0, row=0, sticky=tk.E+tk.W+tk.N+tk.S)
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)

    def on_tab_changed(self, event):
        tab = event.widget.tab('current')['text']
        if tab == "Securities":
            self.show_securities()
        elif tab == "Transactions":
            self.show_transactions()

    def show_securities(self):
        self.notebook.select(0)
        self.transactions_table_view.hide()
        self.securities_table_view.show()
        # pass

    def show_transactions(self):
        self.notebook.select(1)
        self.securities_table_view.hide()
        self.transactions_table_view.show()
        # pass

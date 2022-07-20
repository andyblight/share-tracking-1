from tkinter import ttk

from ui.holdings_view import HoldingsTableView
from ui.securities_table_view import SecuritiesTableView
from ui.transactions_view import TransactionsTableView


class TabbedFrame:
    def __init__(self, parent):
        self.parent = parent
        self.notebook = ttk.Notebook(self.parent)
        # Create the views for each tab.
        self.holdings_table_view = HoldingsTableView(self.parent)
        self.securities_table_view = SecuritiesTableView(self.parent)
        self.transactions_table_view = TransactionsTableView(self.parent)
        self.notebook.add(
            child=self.holdings_table_view, sticky="news", text="Holdings"
        )
        # Add views to tabbed window.
        self.notebook.add(
            child=self.securities_table_view, sticky="news", text="Securities"
        )
        self.notebook.add(
            child=self.transactions_table_view, sticky="news", text="Transactions"
        )
        self.notebook.grid(column=0, row=0, sticky="news")
        # Set up callback to allow tabs to change properly.
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _on_tab_changed(self, event):
        tab = event.widget.tab("current")["text"]
        if tab == "Holdings":
            self.show_holdings()
        elif tab == "Securities":
            self.show_securities()
        elif tab == "Transactions":
            self.show_transactions()

    def show_holdings(self):
        self.notebook.select(0)
        self.holdings_table_view.tkraise()
        self.holdings_table_view.show()

    def show_securities(self):
        self.notebook.select(1)
        self.securities_table_view.tkraise()
        self.securities_table_view.show()

    def show_transactions(self):
        self.notebook.select(2)
        self.transactions_table_view.tkraise()
        self.transactions_table_view.show()

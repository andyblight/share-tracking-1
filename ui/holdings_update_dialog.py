import tkinter as tk
from tkinter import ttk

from database.main import database
from database.holdings_table import HoldingsRow
from database.transactions_table import TransactionsRow


class HoldingsUpdateDialog:
    def __init__(self, parent):
        """
        This dialog reads the data from the transactions table and adds new
        records as needed. This dialog should show:
        Start button.
        Number of records updated label.
        Close button.
        """
        self.parent = parent
        # Set up new window.
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Update from transactions")
        self.dialog.geometry("500x400")
        self.dialog.grid_rowconfigure(0, pad=10, weight=1)
        self.dialog.grid_columnconfigure(0, pad=10, weight=1)
        # Create windows sized frame.
        self.frame = ttk.Frame(self.dialog, borderwidth=4, relief="ridge")
        self.frame.grid(sticky="nesw")
        # Added label.
        self._added_label = ttk.Label(self.frame, text="Added:")
        self._added_label.grid(column=0, row=0)
        self._records_added = tk.IntVar()
        self._added_value_label = ttk.Label(
            self.frame, textvariable=self._records_added
        )
        self._added_value_label.grid(column=1, row=0)
        # Buttons.
        self.update_button = tk.Button(self.frame, text="Update", command=self.update)
        self.update_button.grid(column=0, row=2)
        self.cancel_button = tk.Button(self.frame, text="Cancel", command=self.cancel)
        self.cancel_button.grid(column=1, row=2)

    def _write_row(self, transaction: TransactionsRow) -> None:
        # Translate from transaction to holdings.
        row = HoldingsRow()
        # row.set(0, date(2022, 5, 12), 1, 81, 4.75, 3.90, 5.95, 384.75)
        row.date_obj = transaction.date_obj
        row.sid = transaction.sid
        if transaction.type == "S":
            row.quantity -= transaction.quantity
        else:
            row.quantity += transaction.quantity
        row.total = transaction.total
        row.stop_loss = 0.0
        row.target = 0.0
        row.value = 0.0
        # Set total quantity.
        row.total_quantity = database.holdings.get_total_quantity(transaction.sid)
        row.total_quantity += row.quantity
        print(
            "_w_r: t.q, r.q, r.tq",
            transaction.quantity,
            row.quantity,
            row.total_quantity,
        )
        # Add new row.
        database.holdings.add_row(row)

    def _add_holding(self, sid):
        print("Adding new", sid)
        transaction_row = database.transactions.get_row(sid)
        row = HoldingsRow()
        row.date_obj = transaction_row.date_obj
        row.sid = sid
        row.quantity = transaction_row.quantity
        row.price = transaction_row.price
        row.value = row.price
        row.stop_loss = row.price * 0.8
        row.target = 0.0
        row.total = row.quantity * row.value
        database.holdings.add_row(row)

    def _update_holding(self, transaction) -> None:
        print("Updating using", transaction)
        sid = transaction[0]
        new_quantity = transaction[1]
        # Get holding with SID.
        row = database.holdings.get_row(sid)
        # Get date of latest transaction.
        transaction = database.transactions.get_most_recent(sid)
        # Replace holding with matching SID values date and total quantity.
        row.quantity = new_quantity
        row.date_obj = transaction.date_obj
        database.holdings.replace(row)

    def update(self) -> None:
        print("UpdateFromTransactionsDialog->update")
        transactions_quantities = database.transactions.get_quantities()
        holdings_quantities = database.holdings.get_quantities()
        print(
            "num holdings: ",
            len(holdings_quantities),
            ", filtered transactions:",
            len(transactions_quantities),
        )
        # print(
        #     "holdings: ",
        #     holdings_quantities,
        #     ", \nfiltered transactions:",
        #     transactions_quantities,
        # )
        for transaction in transactions_quantities:
            if transaction[1] == 0:
                database.holdings.delete_row(transaction[0])
            elif transaction[1] > 0:
                matched = False
                for holding in holdings_quantities:
                    if holding[0] == transaction[0]:
                        print("Matched", holding[0])
                        matched = True
                        if holding[1] != transaction[1]:
                            self._update_holding(transaction)
                if not matched:
                    self._add_holding(transaction[0])
            else:
                print("ERROR: transaction.quantity < 0:", transaction.quantity)

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()

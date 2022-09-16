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

    def update(self) -> None:
        print("UpdateFromTransactionsDialog->update")
        all_transactions = database.transactions.get_all_rows()
        all_holdings = database.holdings.get_all_rows()
        print(
            "num holdings: ",
            len(all_holdings),
            "filtered transactions",
            len(all_transactions),
        )
        for holding in all_holdings:
            for transaction in all_transactions:
                if (
                    (holding.sid == transaction.sid)
                    and (holding.date_obj == transaction.date_obj)
                    and (abs(holding.quantity) == abs(transaction.quantity))
                ):
                    print(
                        "Matched", holding.date_obj, holding.sid, abs(holding.quantity)
                    )
                    # pass
                else:
                    self._write_row(transaction)
                    self._records_added.set(self._records_added.get() + 1)

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()

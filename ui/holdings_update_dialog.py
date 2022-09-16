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
        # Updated label.
        self._updated_label = ttk.Label(self.frame, text="Updated:")
        self._updated_label.grid(column=0, row=1)
        self._records_updated = tk.IntVar()
        self._updated_value_label = ttk.Label(
            self.frame, textvariable=self._records_updated
        )
        self._updated_value_label.grid(column=1, row=1)
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
        row.quantity = transaction.quantity
        row.total = transaction.total
        row.stop_loss = 0.0
        row.target = 0.0
        row.value = 0.0
        database.holdings.add_row(row)

    def _new_record_needed(
        self, holding: HoldingsRow, transaction: TransactionsRow
    ) -> None:
        needed = False
        print("nrn: holding.sid", holding.sid, "transaction.sid:", transaction.sid)
        if holding.sid == transaction.sid:
            # Matched security ID so start checking further.
            pass
        return needed

    def update(self) -> None:
        """
        This function is tricky so I had to work what I wanted it to do first
        before coding!  See notes.md for details.
        """
        print("UpdateFromTransactionsDialog->update")
        filtered_transactions = database.transactions.get_current_holdings()
        most_recent_holdings = database.holdings.get_most_recent_rows()
        print(
            "num holdings: ",
            len(most_recent_holdings),
            "filtered transactions",
            len(filtered_transactions),
        )
        # Add and update holdings records.
        matched = False
        for transaction in filtered_transactions:
            transaction_quantity = transaction[0]
            transaction_row = transaction[1]
            for recent_holding in most_recent_holdings:
                if recent_holding.sid == transaction_row.sid:
                    # We have matched the security.
                    matched = True
                    # Does the most recent holding quantity match the
                    # transaction quantity?
                    if recent_holding.quantity != transaction_quantity:
                        # No so write a new record.
                        self._write_row(transaction_row)
                        self._records_updated.set(self._records_updated.get() + 1)
            if not matched:
                # There was no holding record for the transaction so add a new one.
                self._write_row(transaction_row)
                self._records_added.set(self._records_added.get() + 1)

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()

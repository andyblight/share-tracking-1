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
        self.update_button = tk.Button(
            self.frame, text="Update", command=self.update
        )
        self.update_button.grid(column=0, row=2)
        self.cancel_button = tk.Button(
            self.frame, text="Cancel", command=self.cancel
        )
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

    def _update_count_labels(self):
        print("Added:", self._records_added.get())
        print("Updated:", self._records_updated.get())

    def update(self) -> None:
        """
        This function is tricky so I had to work what I wanted it to do first
        before coding!  See notes.md for details.
        """
        print("UpdateFromTransactionsDialog->update")
        filtered_transactions = database.transactions.get_filtered_rows()
        holdings = database.holdings.get_all_rows()
        print(
            "num holdings: ",
            len(holdings),
            "filtered transactions",
            len(filtered_transactions),
        )
        # Add and update holdings records.
        matched = False
        for transaction in filtered_transactions:
            for holding in holdings:
                if holding.sid == transaction.sid:
                    # We have a match so see if it needs to be updated.
                    matched = True

                if self._new_record_needed(holding, transaction):
                    self._write_row(transaction)
                    self._records_updated += 1
            if not matched:
                # There was no holding record for the transaction so add a new one.
                self._write_row(transaction)
                self._records_added += 1
        self._update_count_labels()

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()

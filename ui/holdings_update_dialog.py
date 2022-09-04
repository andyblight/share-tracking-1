import tkinter as tk
from tkinter import ttk

from datetime import date
from database.main import database
from database.holdings_table import HoldingsRow
from database.transactions_table import TransactionsRow, TransactionsRows


class HoldingsUpdateDialog:
    def __init__(self, parent):
        """
        This dialog reads the data from the transactions table and adds new records as needed.
        This dialog should show:
        Start button.
        Number of records updated label.
        Close button.
        """
        self.parent = parent
        self._records_updated = 0
        # Set up new window.
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Update from transactions")
        self.dialog.geometry("500x400")
        self.dialog.grid_rowconfigure(0, pad=10, weight=1)
        self.dialog.grid_columnconfigure(0, pad=10, weight=1)
        # Create windows sized frame.
        self.frame = ttk.Frame(self.dialog, borderwidth=4, relief="ridge")
        self.frame.grid(sticky="nesw")
        # Add data field.
        data_entry_label_frame = ttk.LabelFrame(self.frame, text="Update")
        data_entry_label_frame.grid(column=0, row=0, sticky="new")
        # Buttons
        self.update_button = tk.Button(
            data_entry_label_frame, text="Update", command=self.update
        )
        self.cancel_button = tk.Button(
            data_entry_label_frame, text="Cancel", command=self.cancel
        )
        # Position buttons.
        self.update_button.grid(column=0, row=4)
        self.cancel_button.grid(column=1, row=4)

    def _write_row(self, transaction: TransactionsRow) -> None:
        row = HoldingsRow()
        row.set(date(2022, 5, 12), 1, 81, 4.75, 3.90, 5.95, 384.75)
        database.holdings.add_row(row)
        self._records_updated += 1

    def _new_record_needed(
        self, holding: HoldingsRow, transaction: TransactionsRow
    ) -> None:
        needed = False
        if holding.sid == transaction.sid:
            # Matched security ID so start checking further.
            pass
        return needed

    def update(self) -> None:
        print("UpdateFromTransactionsDialog->update")
        filtered_transactions = database.transactions.get_filtered_rows()
        holdings = database.holdings.get_all_rows()
        print(
            "num holdings: ",
            len(holdings),
            "filtered transactions",
            len(filtered_transactions),
        )
        for holding in holdings:
            for transaction in filtered_transactions:
                if self._new_record_needed(holding, transaction):
                    self._write_row(transaction)

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()

import tkinter as tk
from tkinter import ttk

from datetime import date
from database.main import database
from database.holdings_table import HoldingsRow
from database.transactions_table import TransactionsRow

ZERO_DATETIME_STR = "0000-00-00 00:00:00"


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

    def _filter_transactions(self, all_rows):
        """ Filter all_rows  so that only securities with active shares are returned.
        Active shares are those where the number bought exceeds the number sold.
        A dictionary is used so the results are accessible by the unique security ID.
        """
        print("UpdateFromTransactionsDialog->_filter_transactions")
        filtered_transactions = {}
        for row in all_rows:
            print(row)
            transaction_date = row[1]
            buy = row[2]
            security_id = row[3]
            quantity = row[4]
            price = row[5]
            if buy == "S":
                quantity = -quantity
                date_bought = ZERO_DATETIME_STR
                date_sold = transaction_date
            else:
                date_sold = ZERO_DATETIME_STR
                date_bought = transaction_date
            if security_id in filtered_transactions:
                print("Amend existing row")
                old_entry = filtered_transactions[security_id]
                print("Old entry", old_entry)
                old_date_bought = old_entry[0]
                # old_date_sold = old_entry[1]
                old_quantity = old_entry[2]
                old_price = old_entry[3]
                new_quantity = old_quantity + quantity
                print("Quantity old: {}, new: {}".format(old_quantity, new_quantity))
                if new_quantity < 0:
                    print(
                        "Amend: Security {} has negative quantity of {}".format(
                            security_id, new_quantity
                        )
                    )
                amended_row = (old_date_bought, date_sold, new_quantity, old_price)
                filtered_transactions[security_id] = amended_row
                print("Amended entry", amended_row)
            else:
                print("Add new row")
                if quantity < 0:
                    print(
                        "Add: Security {} has negative quantity of {}".format(
                            security_id, quantity
                        )
                    )
                new_row = (date_bought, date_sold, quantity, price)
                filtered_transactions[security_id] = new_row
            print("")
        print("filtered_transactions: ", filtered_transactions)
        return filtered_transactions

    def _write_row(self, transaction) -> None:
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

    def _update_holdings_table(self, holdings, filtered_transactions) -> None:
        """ Write new holdings to holdings table. """
        print("UpdateFromTransactionsDialog->_update_holdings_table")
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

    def update(self) -> None:
        print("UpdateFromTransactionsDialog->update")
        all_rows = database.transactions.get_all_rows()
        date_ordered_rows = sorted(all_rows, key=lambda x: x[1])
        filtered_transactions = self._filter_transactions(date_ordered_rows)
        holdings = database.holdings.get_all_rows()
        self._update_holdings_table(holdings, filtered_transactions)

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()

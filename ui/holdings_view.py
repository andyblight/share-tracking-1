import tkinter as tk
from tkinter import ttk

from database.main import database
from ui.utils import float_to_currency

ZERO_DATETIME_STR = "0000-00-00 00:00:00"

class UpdateHoldingDialog:
    def __init__(self, parent):
        # Set up new window.
        self.parent = parent
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Update holding")
        self.dialog.geometry("500x400")
        self.dialog.grid_rowconfigure(0, pad=10, weight=1)
        self.dialog.grid_columnconfigure(0, pad=10, weight=1)
        # Create windows sized frame.
        self.frame = ttk.Frame(self.dialog, borderwidth=4, relief="ridge")
        self.frame.grid(sticky="nesw")
        # Add data field.
        data_entry_label_frame = ttk.LabelFrame(self.frame, text="Select holding")
        data_entry_label_frame.grid(column=0, row=0, sticky="new")
        # Buttons
        self.add_new_button = tk.Button(
            data_entry_label_frame, text="Add", command=self.add
        )
        self.cancel_button = tk.Button(
            data_entry_label_frame, text="Cancel", command=self.cancel
        )
        # Position buttons.
        self.add_new_button.grid(column=0, row=4)
        self.cancel_button.grid(column=1, row=4)

    def add(self):
        print("UpdateHoldingDialog Add")
        # # Get info from entry boxes.
        # ticker = self.stock_ticker_entry.get()
        # name = self.stock_name_entry.get()
        # print("add: " + ticker + ", " + name)
        # # Write to database.
        # database.securities.add_row(ticker, name)

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()


class UpdateFromTransactionsDialog:
    def __init__(self, parent):
        """ This dialog should show:
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

    def _update_holdings_table(self, holdings, filtered_transactions):
        """ Write new holdings to holdings table. """
        print("UpdateFromTransactionsDialog->_update_holdings_table")
        print("holdings: ", holdings)
        for holding in holdings:
            pass
        # FIXME!
        self._records_updated = 700

    def update(self):
        print("UpdateFromTransactionsDialog->update")
        all_rows = database.transactions.get_all_rows()
        date_ordered_rows = sorted(all_rows, key=lambda x: x[1])
        filtered_transactions = self._filter_transactions(date_ordered_rows)
        holdings = database.holdings.get_all_rows()
        self._update_holdings_table(holdings, filtered_transactions)

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()


class HoldingsTableView(ttk.Frame):
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
        columns = (
            "uid",
            "date",
            "sid",
            "quantity",
            "value",
            "stop_loss",
            "target",
            "total",
        )
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.grid(column=0, row=0)
        # Define headings
        self.tree.heading("uid", text="UID")
        self.tree.column("uid", width=40, anchor=tk.E)
        self.tree.heading("date", text="Date")
        self.tree.column("date", width=100, anchor=tk.E)
        self.tree.heading("sid", text="SID")
        self.tree.column("sid", width=40, anchor=tk.E)
        self.tree.heading("quantity", text="Quantity")
        self.tree.column("quantity", width=100, anchor=tk.E)
        self.tree.heading("value", text="Value")
        self.tree.column("value", width=80, anchor=tk.E)
        self.tree.heading("stop_loss", text="S/L")
        self.tree.column("stop_loss", width=80, anchor=tk.E)
        self.tree.heading("target", text="target")
        self.tree.column("target", width=80, anchor=tk.E)
        self.tree.heading("total", text="Total")
        self.tree.column("total", width=120, anchor=tk.E)
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

    def show(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        all_rows = database.holdings.get_all_rows()
        for row in all_rows:
            # print(row)
            # Convert row into correct format for treeview.
            row_max_index = len(row)
            treeview_row = []
            for i in range(0, row_max_index):
                # Convert currency values to strings so they look right.
                if i in (3, 4, 5, 6, 7):
                    currency_str = float_to_currency(row[i])
                    treeview_row.append(currency_str)
                else:
                    treeview_row.append(row[i])
            # print(treeview_row)
            self.tree.insert("", tk.END, values=treeview_row)

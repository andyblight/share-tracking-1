import tkinter as tk
from tkinter import ttk

from database.main import database


class AddSecurityDialog:
    def __init__(self, parent) -> None:
        # Set up new window.
        self.parent = parent
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Add security")
        dialog_width = 5 * 120
        dialog_height = 3 * 100
        dialog_size = str(dialog_width) + "x" + str(dialog_height)
        self.dialog.geometry(dialog_size)
        self.dialog.grid_columnconfigure(0, minsize=dialog_width, pad=5)
        self.dialog.grid_columnconfigure(1, minsize=dialog_width, pad=5)
        self.dialog.grid_columnconfigure(2, minsize=dialog_width, pad=5)
        self.dialog.grid_columnconfigure(3, minsize=dialog_width, pad=5)
        self.dialog.grid_rowconfigure(0, minsize=dialog_height, pad=5)
        self.dialog.grid_rowconfigure(1, minsize=dialog_height, pad=5)
        self.dialog.grid_rowconfigure(2, minsize=dialog_height, pad=5)
        # Create windows sized label frame.
        self.data_entry_label_frame = ttk.LabelFrame(
            self.dialog, text="Enter new security details"
        )
        self.data_entry_label_frame.grid(columnspan=4, rowspan=3, sticky="news")
        # Add description text.
        self._description_label = ttk.Label(
            self.data_entry_label_frame, text="Description:"
        )
        self._description_label.grid(column=0, row=0)
        self._description_string = tk.StringVar()
        self._description = ttk.Label(
            self.data_entry_label_frame, textvariable=self._description_string
        )
        self._description.grid(column=1, row=0)
        # Ticker label frame
        self.stock_ticker_label = ttk.Label(self.data_entry_label_frame, text="Ticker")
        self.stock_ticker_label.grid(column=0, row=0)
        self.stock_ticker_entry = ttk.Entry(self.data_entry_label_frame)
        self.stock_ticker_entry.grid(column=1, row=0)
        # Name label frame
        self.stock_name_label = ttk.Label(self.data_entry_label_frame, text="Name")
        self.stock_name_label.grid(column=0, row=1)
        self.stock_name_entry = ttk.Entry(self.data_entry_label_frame)
        self.stock_name_entry.grid(column=1, row=1, columnspan=2, sticky="w")
        # Buttons
        self.add_new_button = tk.Button(
            self.data_entry_label_frame, text="Add", command=self.add
        )
        self.add_new_button.grid(column=1, row=2)
        self.cancel_button = tk.Button(
            self.data_entry_label_frame, text="Cancel", command=self.cancel
        )
        self.cancel_button.grid(column=3, row=2)

    def validate_ticker(self, ticker):
        valid = False
        if len(ticker) > 2 and len(ticker) < 20:
            valid = True
        return valid

    def validate_name(self, name):
        valid = False
        if len(name) > 2:
            valid = True
        return valid

    def add(self):
        print("SecurityDialog Add")
        # Get info from entry boxes.
        ticker = self.stock_ticker_entry.get()
        name = self.stock_name_entry.get()
        print("add: " + ticker + ", " + name)
        # Write to database.
        database.securities.add_row(ticker, name)

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()

    def set_description(self, description) -> None:
        self._description_string.set(description)

    def top(self) -> None:
        """ Get the dialog to the top of the pile of windows and wait until closed. """
        self.dialog.attributes("-topmost", 1)
        self.dialog.wait_window()

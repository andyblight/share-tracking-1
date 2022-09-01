import tkinter as tk
from tkinter import ttk

from database.main import database


class AddSecurityDialog:
    def __init__(self, parent) -> None:
        # Set up new window.
        self.parent = parent
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Add security")
        ticker_width_chars = 10
        description_width_chars = 80
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        # Create windows sized label frame.
        self.data_entry_label_frame = ttk.LabelFrame(
            self.dialog, text="Enter new security details"
        )
        self.data_entry_label_frame.grid(sticky="nsew")
        # Add description text.
        self._description_label = ttk.Label(
            self.data_entry_label_frame, text="Description:"
        )
        self._description_label.grid(column=0, row=0, sticky="w")
        # The description value is a disabled entry box to allow copying of the text.
        self._description_string = tk.StringVar()
        self._description = ttk.Entry(
            self.data_entry_label_frame,
            textvariable=self._description_string,
            width=description_width_chars,
        )
        self._description.grid(column=1, row=0, sticky="nsew")
        self._description.configure(state="disabled")
        # Ticker label frame
        self.stock_ticker_label = ttk.Label(self.data_entry_label_frame, text="Ticker")
        self.stock_ticker_label.grid(column=0, row=1, sticky="w")
        self.stock_ticker_entry = ttk.Entry(
            self.data_entry_label_frame, width=ticker_width_chars
        )
        self.stock_ticker_entry.grid(column=1, row=1, sticky="w")
        # Name label frame
        self.stock_name_label = ttk.Label(self.data_entry_label_frame, text="Name")
        self.stock_name_label.grid(column=0, row=2, sticky="w")
        self.stock_name_entry = ttk.Entry(
            self.data_entry_label_frame, width=description_width_chars
        )
        self.stock_name_entry.grid(column=1, row=2, sticky="nsew")
        # Buttons
        self.add_new_button = tk.Button(
            self.data_entry_label_frame, text="Add", command=self.add
        )
        self.add_new_button.grid(column=0, row=3)
        self.cancel_button = tk.Button(
            self.data_entry_label_frame, text="Cancel", command=self.cancel
        )
        self.cancel_button.grid(column=1, row=3)

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
        self.dialog.destroy()

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()

    def set_description(self, description) -> None:
        self._description_string.set(description)

    def wait(self) -> None:
        """ Get the dialog to the top of the pile of windows and wait until closed. """
        self.dialog.attributes("-topmost", 1)
        self.dialog.wait_window()

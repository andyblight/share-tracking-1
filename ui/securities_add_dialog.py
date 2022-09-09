import tkinter as tk
from tkinter import ttk

from database.main import database


class SecuritiesAddDialog:
    def __init__(self, parent) -> None:
        # Set up new window.
        self._parent = parent
        self._dialog = tk.Toplevel(self._parent)
        self._dialog.title("Add security")
        ticker_width_chars = 10
        description_width_chars = 80
        self._dialog.columnconfigure(0, weight=1)
        self._dialog.rowconfigure(0, weight=1)
        # Create windows sized label frame.
        self._data_entry_label_frame = ttk.LabelFrame(
            self._dialog, text="Enter new security details"
        )
        self._data_entry_label_frame.grid(sticky="nsew")
        # Add description text.
        self._description_label = ttk.Label(
            self._data_entry_label_frame, text="CS Description:"
        )
        self._description_label.grid(column=0, row=0, sticky="w", padx=10, pady=10)
        # The description value is a disabled entry box to allow copying of the text.
        self._description_string = tk.StringVar()
        self._description = ttk.Entry(
            self._data_entry_label_frame,
            textvariable=self._description_string,
            width=description_width_chars,
        )
        self._description.grid(column=1, row=0, sticky="nsew", padx=10, pady=10)
        self._description.configure(state="readonly")
        # Ticker label frame
        self._stock_ticker_label = ttk.Label(
            self._data_entry_label_frame, text="Ticker:"
        )
        self._stock_ticker_label.grid(column=0, row=1, sticky="w", padx=10, pady=5)
        self._stock_ticker_entry = ttk.Entry(
            self._data_entry_label_frame, width=ticker_width_chars
        )
        self._stock_ticker_entry.grid(column=1, row=1, sticky="w", padx=10, pady=5)
        # Name label frame
        self._name_string = tk.StringVar()
        self._stock_name_label = ttk.Label(self._data_entry_label_frame, text="Name:")
        self._stock_name_label.grid(column=0, row=2, sticky="w", padx=10, pady=5)
        self._stock_name_entry = ttk.Entry(
            self._data_entry_label_frame,
            textvariable=self._name_string,
            width=description_width_chars,
        )
        self._stock_name_entry.grid(column=1, row=2, sticky="nsew", padx=10, pady=5)
        # Buttons
        self._add_new_button = tk.Button(
            self._data_entry_label_frame, text="Add", command=self._add
        )
        self._add_new_button.grid(column=0, row=3, padx=10, pady=10)
        self._cancel_button = tk.Button(
            self._data_entry_label_frame, text="Cancel", command=self._cancel
        )
        self._cancel_button.grid(column=1, row=3, padx=10, pady=10)

    def _validate_ticker(self, ticker):
        valid = False
        if len(ticker) > 2 and len(ticker) < 20:
            valid = True
        return valid

    def _validate_name(self, name):
        valid = False
        if len(name) > 2:
            valid = True
        return valid

    def _add(self):
        print("SecurityDialog Add")
        # Get info from entry boxes.
        ticker = self._stock_ticker_entry.get()
        name = self._stock_name_entry.get()
        print("add: " + ticker + ", " + name)
        # Write to database.
        database.securities.add_row(ticker, name)
        self._dialog.destroy()

    def _cancel(self):
        # Quit dialog doing nothing.
        self._dialog.destroy()

    def set_description(self, description) -> None:
        self._description_string.set(description)
        # Set the name field to the description text as the description is
        # pretty close to what is needed most times.
        self._name_string.set(description)

    def wait(self) -> None:
        """Get the dialog to the top of the pile of windows and wait until closed."""
        self._dialog.attributes("-topmost", 1)
        self._dialog.wait_window()

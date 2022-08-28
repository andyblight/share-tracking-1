import tkinter as tk
from tkinter import ttk

from database.main import database


class AddSecurityDialog:
    def __init__(self, parent) -> None:
        # Set up new window.
        self.parent = parent
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Add security")
        self.dialog.geometry("500x400")
        self.dialog.grid_rowconfigure(0, pad=10, weight=1)
        self.dialog.grid_columnconfigure(0, pad=10, weight=1)
        # Create windows sized frame.
        self.frame = ttk.Frame(self.dialog, borderwidth=4, relief="ridge")
        self.frame.grid(sticky="nesw")
        # Add data field.
        data_entry_label_frame = ttk.LabelFrame(
            self.frame, text="Enter new security details"
        )
        data_entry_label_frame.grid(column=0, row=0, sticky="new")
        # Ticker label frame
        stock_ticker_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Ticker")
        self.stock_ticker_entry = ttk.Entry(stock_ticker_label_frame)
        self.stock_ticker_entry.grid(column=0, row=0)
        # Name label frame
        stock_name_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Name")
        self.stock_name_entry = ttk.Entry(stock_name_label_frame)
        self.stock_name_entry.grid(sticky="news")
        # Position label frames
        stock_ticker_label_frame.grid(column=0, row=0)
        stock_name_label_frame.grid(column=0, row=1, columnspan=2, sticky="ew")
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

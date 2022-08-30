import tkinter as tk
from tkinter import ttk

from database.main import database
from ui.securities_table_view import SecuritiesTableView


class SelectSecurityDialog:
    def __init__(self, parent, rows) -> None:
        self.parent = parent
        self._security_id = -1
        # Set up new window.
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Add security")
        self.dialog.geometry("600x400")
        self.dialog.grid_rowconfigure(0, pad=10, weight=1)
        self.dialog.grid_columnconfigure(0, pad=10, weight=1)
        # Create window sized frame.
        self.frame = ttk.Frame(self.dialog, borderwidth=4, relief="ridge")
        self.frame.grid(columnspan=5, rowspan=2, sticky="nesw")
        # Add security table view in its own frame.
        self.security_frame = ttk.Frame(self.frame, borderwidth=1)
        self.securities_table_view = SecuritiesTableView(self.security_frame)
        self.security_frame.grid(columnspan=5, column=0, row=0, sticky="ne")
        self.securities_table_view.grid(sticky="nesw")
        # Buttons
        self.ok_button = tk.Button(self.frame, text="Ok", command=self.ok)
        self.cancel_button = tk.Button(self.frame, text="Cancel", command=self.cancel)
        # Position buttons.
        self.ok_button.grid(column=1, row=2)
        self.cancel_button.grid(column=3, row=2)

    def get_security_id(self):
        return self._security_id

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()

    def ok(self):
        # Quit dialog doing nothing.
        print("SSD ok called")

    def top(self):
        self.dialog.top()

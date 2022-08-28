import tkinter as tk
from tkinter import ttk

from database.main import database
from ui.securities_table_view import SecuritiesTableView


class SelectSecurityDialog:
    def __init__(self, parent, rows) -> None:
        self.parent = parent
        self._security_id = -1
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
        self.securities_table_view = SecuritiesTableView(self.parent)
        # Buttons
        self.cancel_button = tk.Button(
            self.frame, text="Cancel", command=self.cancel
        )
        # Position buttons.
        self.cancel_button.grid(column=1, row=4)

    def get_security_id(self):
        return self._security_id

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()

    def top(self):
        pass

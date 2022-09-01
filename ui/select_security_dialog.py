import tkinter as tk
from tkinter import ttk

from database.main import database
from ui.securities_table_view import SecuritiesTableView


class SelectSecurityDialog:
    def __init__(self, parent) -> None:
        self.parent = parent
        self._security_id = -1
        # Set up new window.
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Select security")
        self.dialog.geometry("600x400")
        self.dialog.grid_rowconfigure(0, pad=10, weight=1)
        self.dialog.grid_columnconfigure(0, pad=10, weight=1)
        # Create window sized frame.
        self.frame = ttk.Frame(self.dialog, borderwidth=4, relief="ridge")
        self.frame.grid(columnspan=5, rowspan=2, sticky="nesw")
        # Add description text.
        self._description_label = ttk.Label(self.frame, text="Description:")
        self._description_label.grid(column=0, row=0)
        self._description_string = tk.StringVar()
        self._description = ttk.Label(self.frame, textvariable=self._description_string)
        self._description.grid(column=1, row=0)
        # Add security table view in its own frame.
        self.security_frame = ttk.Frame(self.frame, borderwidth=1)
        self.securities_table_view = SecuritiesTableView(self.security_frame)
        self.security_frame.grid(columnspan=5, column=0, row=1, sticky="ne")
        self.securities_table_view.grid(sticky="nesw")
        # Buttons
        self.ok_button = tk.Button(self.frame, text="Ok", command=self.ok)
        self.cancel_button = tk.Button(self.frame, text="No match", command=self.cancel)
        # Position buttons.
        self.ok_button.grid(column=1, row=2)
        self.cancel_button.grid(column=3, row=2)

    def set_description(self, description) -> None:
        self._description_string.set(description)

    def set_rows(self, rows) -> None:
        self.securities_table_view.show_rows(rows)

    def get_security_id(self) -> int:
        print("SSD gsi", self._security_id)
        return self._security_id

    def cancel(self) -> None:
        """ Quit dialog doing nothing. """
        self.dialog.destroy()

    def ok(self) -> None:
        """ Set the selected security Id for later use. """
        self._security_id = self.securities_table_view.get_selected_uid()
        print("SSD ok set id", self._security_id)
        self.dialog.destroy()

    def wait(self) -> None:
        """ Get the dialog to the top of the pile of windows and wait until closed. """
        self.dialog.attributes("-topmost", 1)
        self.dialog.wait_window()

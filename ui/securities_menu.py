from tkinter import ttk
import tkinter as tk

# from database.securities import SecuritiesDatabase


class AddNewSecurityDialog:
    def __init__(self, parent):
        # Set up new window.
        self.parent = parent
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Add security")
        self.dialog.geometry("500x400")
        self.dialog.grid_rowconfigure(0, pad=10, weight=1)
        self.dialog.grid_columnconfigure(0, pad=10, weight=1)
        # Create windows sized frame.
        self.frame = ttk.Frame(
            self.dialog, borderwidth=4, relief="ridge"
        )
        self.frame.grid(sticky="nesw")
        # Add dada field.
        data_entry_label_frame = ttk.LabelFrame(
            self.frame, text="Enter new security details"
        )
        data_entry_label_frame.grid(column=0, row=0)
        # Ticker label frame
        stock_ticker_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Ticker")
        stock_ticker_entry = ttk.Entry(stock_ticker_label_frame)
        stock_ticker_entry.grid(column=0, row=0)
        # Name label frame
        stock_name_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Name")
        stock_name_entry = ttk.Entry(stock_name_label_frame)
        stock_name_entry.grid(column=0, row=0)
        # Quantity label frame
        stock_quantity_label_frame = ttk.LabelFrame(
            data_entry_label_frame, text="Quantity"
        )
        stock_quantity_entry = ttk.Entry(stock_quantity_label_frame)
        stock_quantity_entry.grid(column=0, row=0)
        # Price label frame
        stock_price_label_frame = ttk.LabelFrame(
            data_entry_label_frame, text="Price (GBX)"
        )
        stock_price_entry = ttk.Entry(stock_price_label_frame)
        stock_price_entry.grid(column=0, row=0)
        # Position label frames
        stock_ticker_label_frame.grid(column=0, row=0)
        stock_name_label_frame.grid(column=0, row=1)
        stock_quantity_label_frame.grid(column=0, row=2)
        stock_price_label_frame.grid(column=0, row=3)
        # Buttons
        self.add_new_button = tk.Button(
            data_entry_label_frame, text="Add", command=self.add
        )
        self.cancel_button = tk.Button(
            data_entry_label_frame, text="Cancel", command=self.cancel
        )
        # Keep the button on the left.
        self.add_new_button.grid(column=0, row=4)
        self.cancel_button.grid(column=1, row=4)

    def add(self):
        # Write
        print("add called")

    def cancel(self):
        # Quit dialog doing nothing.
        self.dialog.destroy()


class SecuritiesMenu(tk.Menu):
    def __init__(self, parent, menu_bar):
        self.parent = parent
        self.menu_file = tk.Menu(menu_bar)
        self.menu_file.add_command(label="Add...", command=self.add)
        self.menu_file.add_command(label="Show", command=self.show)
        menu_bar.add_cascade(label="Securities", menu=self.menu_file)

    def add(self):
        # Create a new dialog box.
        _ = AddNewSecurityDialog(self.parent)

    def show(self):
        # Create treeview of database.
        # Allow scrolling.
        pass

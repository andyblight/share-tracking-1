# From: https://www.activestate.com/resources/quick-reads/how-to-display-data-in-a-table-using-tkinter/

from tkinter import ttk
import tkinter as tk
import sqlite3
from pathlib import Path


class sqlite_wrapper:
    def __init__(self):
        self.file_name = "shares.db"
        self.table_name = "shares"

    def create(self):
        con1 = sqlite3.connect(self.file_name)
        cur1 = con1.cursor()
        sql_query = "CREATE TABLE IF NOT EXISTS "
        sql_query += self.table_name
        sql_query += "(ticker text, name text, quantity real, price real)"
        cur1.execute(sql_query)
        con1.commit()
        con1.close()

    def add_rows(self):
        con1 = sqlite3.connect(self.file_name)
        cur = con1.cursor()
        cur.execute("INSERT INTO shares VALUES ('FRED', 'Frederick', '12', '75.4')")
        cur.execute("INSERT INTO shares VALUES ('BERT', 'Bertrand', '34', '175.4')")
        cur.execute("INSERT INTO shares VALUES ('TOM', 'Thomas', '256', '275.4')")
        con1.commit()
        con1.close()

    def get_all_rows(self):
        con1 = sqlite3.connect(self.file_name)
        cur1 = con1.cursor()
        sql_query = "SELECT * FROM " + self.table_name
        cur1.execute(sql_query)
        rows = cur1.fetchall()
        con1.close()
        return rows

    def is_present(self):
        db_file = Path(self.file_name)
        return db_file.is_file()


def view():
    all_rows = database.get_all_rows()
    for row in all_rows:
        print(row)
        tree.insert("", tk.END, values=row)


def add_new():
    pass


database = sqlite_wrapper()
# Create database if not present
if not database.is_present():
    database.create()
    database.add_rows()

DEFAULT_APP_WIDTH = 800
DEFAULT_APP_HEIGHT = 500

# The window?
root = tk.Tk()
root.title("Share Tracker 1")
# Set size
root.geometry("{}x{}".format(DEFAULT_APP_WIDTH, DEFAULT_APP_HEIGHT))
# Create simplest layout, grid of 1 x 1 using all of window.
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Use tabbed layout.
notebook = ttk.Notebook(root)
# Use sticky to ensure the tabs resize with the window.
notebook.grid(sticky="nsew")

# Create the frames for each page.
display_frame = ttk.Frame(notebook)
display_frame.grid(sticky="nsew")

entry_frame = ttk.Frame(notebook)
entry_frame.grid(sticky="nsew")

# Add frames to notebook.
notebook.add(display_frame, text="Display")
notebook.add(entry_frame, text="Entry")

# Display tab
# The table list
treeview_frame = ttk.Frame(display_frame, borderwidth=4, relief="ridge")
# This shows the frame.
treeview_frame.grid(column=0, row=0)
columns = ("ticker", "name", "quantity", "price")
tree = ttk.Treeview(treeview_frame, columns=columns, show="headings")
tree.grid(column=0, row=0)
# Define headings
tree.heading("ticker", text="Ticker")
tree.column("ticker", width=100)
tree.heading("name", text="Name")
tree.column("name", width=200)
tree.heading("quantity", text="Quantity")
tree.column("quantity", width=100, anchor="e")
tree.heading("price", text="Price")
tree.column("price", width=100, anchor="e")

# The refresh button
refresh_button = tk.Button(display_frame, text="Refresh", command=view)
refresh_button.grid(column=0, row=1)

# Data entry tab
data_entry_label_frame = ttk.LabelFrame(entry_frame, text="Enter new stock details")
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
stock_quantity_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Quantity")
stock_quantity_entry = ttk.Entry(stock_quantity_label_frame)
stock_quantity_entry.grid(column=0, row=0)
# Price label frame
stock_price_label_frame = ttk.LabelFrame(data_entry_label_frame, text="Price (GBX)")
stock_price_entry = ttk.Entry(stock_price_label_frame)
stock_price_entry.grid(column=0, row=0)

add_new_button = tk.Button(data_entry_label_frame, text="Add", command=add_new)

# Position label frames
stock_ticker_label_frame.grid(column=0, row=0)
stock_name_label_frame.grid(column=1, row=0, columnspan=2)
stock_quantity_label_frame.grid(column=3, row=0)
stock_price_label_frame.grid(column=4, row=0)
# Keep the button on the left.
add_new_button.grid(column=0, row=2, sticky="w")

root.mainloop()

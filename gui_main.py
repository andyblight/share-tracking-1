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
        # tree.insert("", tk.END, values=row)


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
root.geometry('{}x{}'.format(DEFAULT_APP_WIDTH, DEFAULT_APP_HEIGHT))
# Create simplest layout, grid of 1 x 1 using all of window.
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Use tabbed layout.
notebook = ttk.Notebook(root)
# Use sticky to ensure the tabs resize with the window.
notebook.grid(sticky="nsew")


display_frame = ttk.Frame(notebook)
display_frame.grid(columnspan=4, rowspan=2)

entry_frame = ttk.Frame(notebook)
entry_frame.grid(columnspan=5, rowspan=3)

notebook.add(display_frame, text="Display")
notebook.add(entry_frame, text="Entry")



# Layout each tab
# The table list
# treeview_frame = ttk.Frame(display_frame, borderwidth=2, relief="ridge")
# tree = ttk.Treeview(treeview_frame, column=("c1", "c2", "c3", "c4"), show="headings")
# tree.column("#1", anchor=tk.CENTER)
# tree.heading("#1", text="Ticker")
# tree.column("#2", anchor=tk.CENTER)
# tree.heading("#2", text="Name")
# tree.column("#3", anchor=tk.CENTER)
# tree.heading("#3", text="Quantity")
# tree.column("#4", anchor=tk.CENTER)
# tree.heading("#4", text="Price")
# # treeview_frame.grid(column=0, row=0, columnspan=4, rowspan=4)

# The refresh button
refresh_button = tk.Button(display_frame, text="Refresh", command=view)
refresh_button.grid(column=0, row=4)

# Data entry area
data_entry_label_frame = ttk.LabelFrame(entry_frame, text="Enter new stock details")
data_entry_label_frame.grid(column=0, row=0)

ticker_label = ttk.Label(data_entry_label_frame, text="Ticker")
ticker_label.grid(column=0, row=0)
ticker_entry = ttk.Entry(data_entry_label_frame)
ticker_entry.grid(column=0, row=1)

add_new_button = tk.Button(data_entry_label_frame, text="Add", command=add_new)
add_new_button.grid(column=0, row=2)

root.mainloop()

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

# The window?
root = tk.Tk()
root.geometry("600x400")
root.title("Share Tracker 1")

# Use tabbed layout.
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

display_frame = ttk.Frame(notebook, width=600, height=380)
display_frame.pack(fill='both', expand=True)

entry_frame = ttk.Frame(notebook, width=600, height=380)
entry_frame.pack(fill='both', expand=True)

notebook.add(display_frame, text="Display")
notebook.add(entry_frame, text="Entry")

# The display frame
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
# # The update button
# display_button = tk.Button(display_frame, text="Update", command=view)

# # Data entry area
# ticker_label_frame = ttk.LabelFrame(entry_frame, text="Ticker")
# ticker_entry = ttk.Entry(ticker_label_frame)
# stock_name_label_frame = ttk.LabelFrame(entry_frame, text="Name")
# stock_name_entry = ttk.Entry(stock_name_label_frame)
# quantity_label_frame = ttk.LabelFrame(entry_frame, text="Quantity")
# quantity_entry = ttk.Entry(quantity_label_frame)
# price_label_frame = ttk.LabelFrame(entry_frame, text="Price")
# price_entry = ttk.Entry(price_label_frame)
# add_new_button = tk.Button(entry_frame, text="Add", command=add_new)

# Layout items on the grid
# Display frame
# display_frame.grid(column=0, row=0)
# treeview_frame.grid(column=0, row=0)
# tree.grid(column=0, row=0, columnspan=5, rowspan=4)
# display_button.grid(column=0, row=4)
# # Entry frame
# entry_frame.grid(column=0, row=5, columnspan=5, rowspan=3)
# ticker_label_frame.grid(column=0, row=5)
# stock_name_label_frame.grid(column=1, row=5, columnspan=2)
# quantity_label_frame.grid(column=3, row=5)
# price_label_frame.grid(column=4, row=5)
# add_new_button.grid(column=2, row=7)

root.mainloop()

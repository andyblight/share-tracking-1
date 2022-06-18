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


database = sqlite_wrapper()
# Create database if not present
if not database.is_present():
    database.create()
    database.add_rows()

# The window?
root = tk.Tk()
# The frame for everything.
content_frame = ttk.Frame(root)

# The display frame
display_frame = ttk.Frame(content_frame, borderwidth=5, relief="ridge")
# The table list
treeview_frame = ttk.Frame(display_frame, borderwidth=2, relief="ridge")
tree = ttk.Treeview(treeview_frame, column=("c1", "c2", "c3", "c4"), show="headings")
tree.column("#1", anchor=tk.CENTER)
tree.heading("#1", text="Ticker")
tree.column("#2", anchor=tk.CENTER)
tree.heading("#2", text="Name")
tree.column("#3", anchor=tk.CENTER)
tree.heading("#3", text="Quantity")
tree.column("#4", anchor=tk.CENTER)
tree.heading("#4", text="Price")
# The update button
update_button = tk.Button(display_frame, text="Update", command=view)

# Data entry area
entry_frame = ttk.Frame(content_frame)
ticker_label = ttk.Label(entry_frame, text="Ticker")
ticker_entry = ttk.Entry(entry_frame)

# Layout items on the grid
# Everything in here
content_frame.grid(column=0, row=0)
# Display frame
display_frame.grid(column=0, row=0)
treeview_frame.grid(column=0, row=0)
tree.grid(column=0, row=0, columnspan=5, rowspan=4)
update_button.grid(column=0, row=4)
# Entry frame
# entry_frame.grid(column=0, row=5, columnspan=5, rowspan=2)
# ticker_label.grid

root.mainloop()

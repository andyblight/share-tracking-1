# From: https://www.activestate.com/resources/quick-reads/how-to-display-data-in-a-table-using-tkinter/

from tkinter import ttk
import tkinter as tk
import sqlite3

from pathlib import Path

DB_FILE_NAME = "shares.db"
TABLE_NAME = "shares"

def connect():
    con1 = sqlite3.connect(DB_FILE_NAME)
    cur1 = con1.cursor()
    sql_query = "CREATE TABLE IF NOT EXISTS "
    sql_query += TABLE_NAME
    sql_query += "(ticker text, name text, quantity real, price real)"
    cur1.execute(sql_query)
    con1.commit()
    con1.close()

def add_rows():
    connection = sqlite3.connect(DB_FILE_NAME)
    cur = connection.cursor()
    cur.execute("INSERT INTO shares VALUES ('FRED', 'Frederick', '12', '75.4')")
    cur.execute("INSERT INTO shares VALUES ('BERT', 'Bertrand', '34', '175.4')")
    cur.execute("INSERT INTO shares VALUES ('TOM', 'Thomas', '256', '275.4')")
    connection.commit()
    connection.close()

def view():
    con1 = sqlite3.connect(DB_FILE_NAME)
    cur1 = con1.cursor()
    sql_query = "SELECT * FROM " + TABLE_NAME
    cur1.execute(sql_query)
    rows = cur1.fetchall()
    for row in rows:
        print(row)
        tree.insert("", tk.END, values=row)
    con1.close()


# connect to the database
db_file = Path(DB_FILE_NAME)
if not db_file.is_file():
    # No file so create one.
    connect()
    add_rows()

root = tk.Tk()
tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4"), show="headings")
tree.column("#1", anchor=tk.CENTER)
tree.heading("#1", text="Ticker")
tree.column("#2", anchor=tk.CENTER)
tree.heading("#2", text="Name")
tree.column("#3", anchor=tk.CENTER)
tree.heading("#3", text="Quantity")
tree.column("#4", anchor=tk.CENTER)
tree.heading("#4", text="Price")
tree.pack()

button1 = tk.Button(text="Display data", command=view)
button1.pack(pady=10)

root.mainloop()

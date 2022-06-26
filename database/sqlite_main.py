import sqlite3


def create():
    connection = sqlite3.connect("shares.db")
    cur = connection.cursor()
    cur.execute(
        """CREATE TABLE shares (
        ticker text,
        name text,
        quantity real,
        price real)"""
    )
    connection.commit()
    connection.close()


def add_row():
    connection = sqlite3.connect("shares.db")
    cur = connection.cursor()
    cur.execute("INSERT INTO shares VALUES ('FRED', 'Frederick', '100', '75.4'")
    connection.commit()
    connection.close()


def read_row():
    connection = sqlite3.connect("shares.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM shares WHERE ticker='FRED'")
    result = cur.fetchone()
    print(result)
    connection.commit()
    connection.close()


def dump():
    print("Dumping all data")
    row_count = 0
    connection = sqlite3.connect("shares.db")
    cur = connection.cursor()
    for row in cur.execute("SELECT * FROM shares"):
        print(row)
        row_count += 1
    connection.commit()
    connection.close()
    print("Dumped ", row_count, "rows")


# create()
add_row()
read_row()
dump()

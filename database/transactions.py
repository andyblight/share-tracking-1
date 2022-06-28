import sqlite3
from pathlib import Path

from database.common import database_file_name


class TransactionsTable:
    def __init__(self):
        self._file_name = database_file_name
        self._table_name = "transactions"

    def create(self):
        con1 = sqlite3.connect(self._file_name)
        cur1 = con1.cursor()
        sql_query = "CREATE TABLE IF NOT EXISTS "
        sql_query += self._table_name
        sql_query += "(ticker text, name text, quantity real, price real)"
        cur1.execute(sql_query)
        con1.commit()
        con1.close()

    def add_fake_rows(self):
        self.add_row("FRED", "Frederick", "12", "75.4")
        self.add_row("BERT", "Bertrand", "34", "175.4")
        self.add_row("TOM", "Thomas", "256", "275.4")

    def add_row(self, ticker, name, quantity_float, price_float):
        con1 = sqlite3.connect(self._file_name)
        cur = con1.cursor()
        command_string = "INSERT INTO {} VALUES ({}, {}, {}, {})".format(
            self._table_name, ticker, name, quantity_float, price_float
        )
        print("Adding row [", command_string, "]")
        cur.execute(command_string)
        con1.commit()
        con1.close()

    def get_all_rows(self):
        con1 = sqlite3.connect(self._file_name)
        cur1 = con1.cursor()
        sql_query = "SELECT * FROM " + self._table_name
        cur1.execute(sql_query)
        rows = cur1.fetchall()
        con1.close()
        return rows

    def is_present(self):
        db_file = Path(self._file_name)
        return db_file.is_file()

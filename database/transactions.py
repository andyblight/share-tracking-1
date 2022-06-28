import sqlite3
from pathlib import Path


class TransactionsTable:
    def __init__(self, file_name):
        self._file_name = file_name
        self._table_name = "Transactions"
        self._type_table_name = "TransactionType"

    def create_transactions_type_table(self, cursor):
        # Create Transactions Type table.
        sql_query = "CREATE TABLE IF NOT EXISTS "
        sql_query += self._type_table_name
        sql_query += " (Type CHAR(1) PRIMARY KEY, "
        sql_query += " Label TEXT)"
        cursor.execute(sql_query)
        # Insert the values.
        sql_query = "INSERT "
        sql_query += self._type_table_name
        sql_query += " (Type, Label) VALUES ('B' 'Buy')"
        cursor.execute(sql_query)
        sql_query = "INSERT "
        sql_query += self._type_table_name
        sql_query += " (Type, Label) VALUES ('N' 'None')"
        cursor.execute(sql_query)
        sql_query = "INSERT "
        sql_query += self._type_table_name
        sql_query += " (Type, Label) VALUES ('S' 'Sell')"
        cursor.execute(sql_query)

    def create_transactions_table(self, cursor):
        # Create Transactions table.
        sql_query = "CREATE TABLE IF NOT EXISTS "
        sql_query += self._table_name
        sql_query += " (transaction_id INTEGER "
        sql_query += "PRIMARY KEY AUTOINCREMENT NOT NULL, "
        sql_query += "type CHAR(1) "
        sql_query += "NOT NULL DEFAULT ('N') REFERENCES TransactionType(Type), "
        sql_query += "date INTEGER NOT NULL, "
        sql_query += "security_id INTEGER NOT NULL, "
        sql_query += "quantity REAL NOT NULL, "
        sql_query += "price REAL NOT NULL, "
        sql_query += "fees REAL NOT NULL, "
        sql_query += "tax REAL NOT NULL, "
        sql_query += "total REAL NOT NULL, "
        sql_query += ")"
        cursor.execute(sql_query)

    def create(self):
        con1 = sqlite3.connect(self._file_name)
        cur1 = con1.cursor()
        cur1.execute()
        if cur1.fetchone()[0] != 1:
            # Table does not exist so create them.
            self.create_transactions_type_table(cur1)
            self.create_transactions_table(cur1)
        con1.commit()
        con1.close()

    def add_test_rows(self):
        self.add_row(self, "B", 1, 1, 20, 1.23, 0.10, 0.50, 25.20)
        self.add_row(self, "S", 2, 2, 30, 1.00, 2.00, 1.50, 33.50)

    def add_row(self, type, date, security_id, quantity, price, fees, tax, total):
        con1 = sqlite3.connect(self._file_name)
        cur = con1.cursor()
        sql_query = "INSERT INTO {} ".format(self._table_name)
        sql_query += "(type, date, security_id, quantity, price, fees, tax, total) "
        sql_query += "VALUES ({}, {}, {}, {}, {}, {}, {}, {})".format(
            type, date, security_id, quantity, price, fees, tax, total
        )
        print("Adding row [", sql_query, "]")
        cur.execute(sql_query)
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

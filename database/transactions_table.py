import csv
import sqlite3
from datetime import date


class TransactionsTable:
    def __init__(self, file_name):
        self._file_name = file_name
        self._table_name = "Transactions"
        self._type_table_name = "TransactionType"

    def _get_cursor(self):
        self.connection = sqlite3.connect(
            self._file_name, detect_types=sqlite3.PARSE_COLNAMES
        )
        cursor = self.connection.cursor()
        return cursor

    def _release_cursor(self):
        self.connection.commit()
        self.connection.close()

    def _create_transactions_type_table(self, cursor):
        # Create Transactions Type table.
        sql_query = "CREATE TABLE IF NOT EXISTS "
        sql_query += self._type_table_name
        sql_query += " (Type CHAR(1) PRIMARY KEY, "
        sql_query += " Label TEXT);"
        print(sql_query)
        cursor.execute(sql_query)
        # Insert the values.
        sql_query = "INSERT INTO "
        sql_query += self._type_table_name
        sql_query += " (Type, Label) VALUES ('B', 'Buy');"
        print(sql_query)
        cursor.execute(sql_query)
        sql_query = "INSERT INTO "
        sql_query += self._type_table_name
        sql_query += " (Type, Label) VALUES ('N', 'None');"
        print(sql_query)
        cursor.execute(sql_query)
        sql_query = "INSERT INTO "
        sql_query += self._type_table_name
        sql_query += " (Type, Label) VALUES ('S', 'Sell');"
        print(sql_query)
        cursor.execute(sql_query)

    def _create_transactions_table(self, cursor):
        # Create Transactions table.
        sql_query = "CREATE TABLE IF NOT EXISTS "
        sql_query += self._table_name
        sql_query += " (uid INTEGER "
        sql_query += "PRIMARY KEY AUTOINCREMENT NOT NULL, "
        sql_query += "date timestamp NOT NULL, "
        sql_query += "type CHAR(1) "
        sql_query += "NOT NULL DEFAULT ('N') REFERENCES TransactionType(Type), "
        sql_query += "security_id INTEGER NOT NULL, "
        sql_query += "quantity REAL NOT NULL, "
        sql_query += "price REAL NOT NULL, "
        sql_query += "fees REAL NOT NULL, "
        sql_query += "tax REAL NOT NULL, "
        sql_query += "total REAL NOT NULL"
        sql_query += ");"
        print(sql_query)
        cursor.execute(sql_query)

    def create(self):
        cursor = self._get_cursor()
        # Create tables if not existing.
        self._create_transactions_type_table(cursor)
        self._create_transactions_table(cursor)
        self._release_cursor()

    def add_test_rows(self):
        self.add_row(date(2022, 5, 22), "B", 4, 20, 1.23, 0.10, 0.50, 25.20)
        self.add_row(date(2022, 6, 22), "S", 3, 30, 1.00, 2.00, 1.50, 33.50)

    def add_row(self, date_obj, type, security_id, quantity, price, fees, tax, total):
        sql_query = "INSERT INTO {} ".format(self._table_name)
        sql_query += "(date, type, security_id, quantity, price, fees, tax, total) "
        sql_query += "VALUES ('{}', '{}', {}, {}, {}, {}, {}, {})".format(
            date_obj, type, security_id, quantity, price, fees, tax, total
        )
        print("Adding row [", sql_query, "]")
        cursor = self._get_cursor()
        cursor.execute(sql_query)
        self._release_cursor()

    def get_all_rows(self):
        rows = []
        cursor = self._get_cursor()
        sql_query = "SELECT * FROM " + self._table_name
        try:
            cursor.execute(sql_query)
            rows = cursor.fetchall()
        except sqlite3.OperationalError:
            print("ERROR: No table", self._table_name)
        self._release_cursor()
        return rows

    def get_quantities(self):
        """ Returns a list of tuples.
        Each tuple contains (security id, quantity).
        The quantity is the total of all quantities for that security where
        buy is a positive quantity and sell is a negative quantity.
        """
        quantities = []
        cursor = self._get_cursor()
        sql_query = "SELECT security_id, quantity FROM " + self._table_name
        try:
            cursor.execute(sql_query)
            quantities = cursor.fetchall()
        except sqlite3.OperationalError:
            print("ERROR: No table", self._table_name)
        self._release_cursor()
        return quantities

    def import_csv(self, filename):
        print("Transactions->ImportCSV", filename)
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                print(row)

import sys
import traceback
import sqlite3
from datetime import date, datetime
from typing import List
from database.utils import str_to_datetime


class TransactionsRow:
    """Names the elements in a single row."""

    def __init__(self) -> None:
        self.uid = 0
        self.date_obj = datetime(1900, 1, 1)
        self.type = ""
        self.sid = 0.0
        self.quantity = 0.0
        self.price = 0.0
        self.costs = 0.0
        self.total = 0.0

    def set(
        self,
        date_obj: datetime,
        type: str,
        sid: int,
        quantity: float,
        price: float,
        costs: float,
        total: float,
    ) -> None:
        self.uid = 0
        self.date_obj = date_obj
        self.type = type
        self.sid = sid
        self.quantity = quantity
        self.price = price
        self.costs = costs
        self.total = total

    def set_from_raw(self, raw_row) -> None:
        self.uid = raw_row[0]
        self.date_obj = str_to_datetime(raw_row[1])
        self.type = raw_row[2]
        self.sid = raw_row[3]
        self.quantity = raw_row[4]
        self.price = raw_row[5]
        self.costs = raw_row[6]
        self.total = raw_row[7]


TransactionsRows = List[TransactionsRow]


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

    def _execute(self, sql_query) -> None:
        cursor = self._get_cursor()
        try:
            cursor.execute(sql_query)
        except sqlite3.Error as er:
            print("SQLite error: %s" % (" ".join(er.args)))
            print("Exception class is: ", er.__class__)
            print("SQLite traceback: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def _release_cursor(self):
        self.connection.commit()
        self.connection.close()

    def _create_transactions_type_table(self):
        # Create Transactions Type table.
        sql_query = "CREATE TABLE IF NOT EXISTS "
        sql_query += self._type_table_name
        sql_query += " (Type CHAR(1) PRIMARY KEY, "
        sql_query += " Label TEXT);"
        print(sql_query)
        self._execute(sql_query)
        # Insert the values.
        sql_query = "INSERT INTO "
        sql_query += self._type_table_name
        sql_query += " (Type, Label) VALUES ('B', 'Buy');"
        print(sql_query)
        self._execute(sql_query)
        sql_query = "INSERT INTO "
        sql_query += self._type_table_name
        sql_query += " (Type, Label) VALUES ('N', 'None');"
        print(sql_query)
        self._execute(sql_query)
        sql_query = "INSERT INTO "
        sql_query += self._type_table_name
        sql_query += " (Type, Label) VALUES ('S', 'Sell');"
        print(sql_query)
        self._execute(sql_query)

    def _create_transactions_table(self):
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
        sql_query += "costs REAL NOT NULL, "
        sql_query += "total REAL NOT NULL"
        sql_query += ");"
        print(sql_query)
        self._execute(sql_query)

    def create(self):
        # Create tables if not existing.
        self._create_transactions_type_table()
        self._create_transactions_table()
        self._release_cursor()

    def add_test_rows(self):
        row = TransactionsRow()
        row.set(date(2022, 5, 22), "B", 4, 20, 1.23, 0.6, 25.20)
        self.add_row(row)
        row.set(date(2022, 6, 22), "S", 3, 30, 1.00, 3.50, 33.50)
        self.add_row(row)

    def add_row(self, row: TransactionsRow) -> None:
        sql_query = "INSERT INTO {} ".format(self._table_name)
        sql_query += "(date, type, security_id, quantity, price, costs, total) "
        sql_query += "VALUES ('{}', '{}', {}, {}, {}, {}, {})".format(
            row.date_obj,
            row.type,
            row.sid,
            row.quantity,
            row.price,
            row.costs,
            row.total,
        )
        print("Adding row [", sql_query, "]")
        self._execute(sql_query)
        self._release_cursor()

    def get_all_rows(self) -> TransactionsRows:
        rows = []
        cursor = self._get_cursor()
        sql_query = "SELECT * FROM " + self._table_name
        try:
            cursor.execute(sql_query)
            for raw_row in cursor:
                row = TransactionsRow()
                row.set_from_raw(raw_row)
                rows.append(row)
        except sqlite3.OperationalError:
            print("ERROR: No table", self._table_name)
        self._release_cursor()
        return rows

    def get_row(self, security_id) -> TransactionsRow:
        cursor = self._get_cursor()
        sql_query = "SELECT * FROM {} ".format(self._table_name)
        sql_query += "WHERE security_id = {}".format(security_id)
        try:
            row = TransactionsRow()
            cursor.execute(sql_query)
            for raw_row in cursor:
                row.set_from_raw(raw_row)
        except sqlite3.OperationalError:
            print("ERROR: No table", self._table_name)
        self._release_cursor()
        return row

    def get_quantities(self):
        """Return a list of tuples.
        Each tuple contains (security id, quantity).
        The quantity is the total of all quantities for that security where
        buy is a positive quantity and sell is a negative quantity.
        """
        quantities = []
        cursor = self._get_cursor()
        sql_query = "SELECT security_id, SUM(quantity) "
        sql_query += "FROM {} ".format(self._table_name)
        sql_query += "GROUP BY security_id "
        sql_query += "ORDER BY security_id ASC"
        try:
            cursor.execute(sql_query)
            quantities = cursor.fetchall()
        except sqlite3.Error as er:
            print("SQLite error: %s" % (" ".join(er.args)))
            print("Exception class is: ", er.__class__)
            print("SQLite traceback: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        self._release_cursor()
        return quantities

    def get_most_recent(self, security_id) -> TransactionsRow:
        cursor = self._get_cursor()
        sql_query = "SELECT MAX(date), security_id FROM {} ".format(self._table_name)
        try:
            row = TransactionsRow()
            cursor.execute(sql_query)
            for raw_row in cursor:
                row.set_from_raw(raw_row)
        except sqlite3.OperationalError:
            print("ERROR: No table", self._table_name)
        self._release_cursor()
        return row

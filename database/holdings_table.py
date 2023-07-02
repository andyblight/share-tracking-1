import sys
import traceback
import sqlite3
from datetime import date, datetime
from typing import List
from database.utils import str_to_datetime

class HoldingsRow:
    """Used to name the row values."""

    def __init__(self) -> None:
        self.uid = 0
        self.date_obj = datetime(1900, 1, 1)
        self.sid = 0.0
        self.quantity = 0.0
        self.price = 0.0
        self.value = 0.0
        self.stop_loss = 0.0
        self.target = 0.0
        self.total = 0.0

    def set(
        self,
        uid: int,
        date_obj: datetime,
        sid: int,
        quantity: float,
        price: float,
        value: float,
        stop_loss: float,
        target: float,
        total: float,
    ) -> None:
        self.uid = uid
        self.date_obj = date_obj
        self.sid = sid
        self.quantity = quantity
        self.price = price
        self.value = value
        self.stop_loss = stop_loss
        self.target = target
        self.total = total

    def set_from_raw(self, raw_row) -> None:
        self.uid = raw_row[0]
        self.date_obj = str_to_datetime(raw_row[1])
        self.sid = raw_row[2]
        self.quantity = raw_row[3]
        self.price = raw_row[4]
        self.value = raw_row[5]
        self.stop_loss = raw_row[6]
        self.target = raw_row[7]
        self.total = raw_row[8]


HoldingsRows = List[HoldingsRow]


class HoldingsTable:
    """An interface to the SQLite holdings table."""

    def __init__(self, file_name) -> None:
        self._file_name = file_name
        self._table_name = "Holdings"

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

    def _release_cursor(self) -> None:
        self.connection.commit()
        self.connection.close()

    def _create_holdings_table(self) -> None:
        # Create holdings table.
        sql_query = "CREATE TABLE IF NOT EXISTS "
        sql_query += self._table_name
        sql_query += " (uid INTEGER"
        sql_query += " PRIMARY KEY AUTOINCREMENT NOT NULL,"
        sql_query += " date timestamp NOT NULL,"
        sql_query += " sid INTEGER NOT NULL,"
        sql_query += " quantity REAL NOT NULL, "
        sql_query += " price REAL NOT NULL, "
        sql_query += " value REAL NOT NULL, "
        sql_query += " stop_loss REAL NOT NULL,"
        sql_query += " target REAL NOT NULL, "
        sql_query += " total REAL NOT NULL"
        sql_query += ");"
        print(sql_query)
        self._execute(sql_query)
        self._release_cursor()

    def create(self) -> None:
        self._create_holdings_table()

    def add_test_rows(self) -> None:
        row = HoldingsRow()
        row.set(0, date(2022, 5, 12), 1, 81, 81, 4.75, 3.90, 5.95, 384.75)
        self.add_row(row)
        row.set(0, date(2022, 5, 12), 2, 100, 100, 2.00, 1.60, 3.25, 200.00)
        self.add_row(row)
        row.set(0, date(2022, 5, 19), 1, 81, 162, 4.85, 3.95, 5.95, 392.85)
        self.add_row(row)

    def add_row(self, row: HoldingsRow) -> None:
        sql_query = "INSERT INTO {} ".format(self._table_name)
        sql_query += "(date, sid, quantity, price, value, "
        sql_query += "stop_loss, target, total) "
        sql_query += "VALUES ('{}', {}, {}, {}, {}, {}, {}, {})".format(
            row.date_obj,
            row.sid,
            row.quantity,
            row.price,
            row.value,
            row.stop_loss,
            row.target,
            row.total,
        )
        print("Adding row [", sql_query, "]")
        self._execute(sql_query)
        self._release_cursor()

    def replace(self, row: HoldingsRow) -> None:
        sql_query = "REPLACE INTO {} ".format(self._table_name)
        sql_query += "(date, sid, quantity, price, value, "
        sql_query += "stop_loss, target, total) "
        sql_query += "VALUES ('{}', {}, {}, {}, {}, {}, {}, {})".format(
            row.date_obj,
            row.sid,
            row.quantity,
            row.price,
            row.value,
            row.stop_loss,
            row.target,
            row.total,
        )
        print("Replacing row [", sql_query, "]")
        self._execute(sql_query)
        self._release_cursor()

    def delete_row(self, security_id) -> None:
        sql_query = "DELETE FROM {} ".format(self._table_name)
        sql_query += "WHERE sid = {}".format(security_id)
        print("Deleting row [", sql_query, "]")
        self._execute(sql_query)
        self._release_cursor()

    def _get_rows(self, sql_query) -> HoldingsRows:
        rows = []
        cursor = self._get_cursor()
        try:
            cursor.execute(sql_query)
            for raw_row in cursor:
                row = HoldingsRow()
                row.set_from_raw(raw_row)
                rows.append(row)
                # print(row.date_obj)
        except sqlite3.Error as er:
            print("SQLite error: %s" % (" ".join(er.args)))
            print("Exception class is: ", er.__class__)
            print("SQLite traceback: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        self._release_cursor()
        return rows

    def get_all_rows(self) -> HoldingsRows:
        sql_query = "SELECT * "
        sql_query += "FROM {} ".format(self._table_name)
        rows = self._get_rows(sql_query)
        return rows

    def get_row(self, security_id) -> HoldingsRow:
        cursor = self._get_cursor()
        sql_query = "SELECT * FROM {} ".format(self._table_name)
        sql_query += "WHERE sid = {}".format(security_id)
        try:
            row = HoldingsRow()
            cursor.execute(sql_query)
            for raw_row in cursor:
                row.set_from_raw(raw_row)
        except sqlite3.Error as er:
            print("SQLite error: %s" % (" ".join(er.args)))
            print("Exception class is: ", er.__class__)
            print("SQLite traceback: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        self._release_cursor()
        return row

    def get_total_quantity(self, sid: int) -> HoldingsRows:
        """
        Gets the most recent record for the given security ID and returns the
        value of the total_quantity field.
        """
        # Based on: https://www.sqlitetutorial.net/sqlite-max/
        sql_query = "SELECT MAX(date), sid, quantity, total_quantity "
        sql_query += "FROM {} ".format(self._table_name)
        sql_query += "WHERE sid = {} ".format(sid)
        rows = self._get_rows(sql_query)
        print("gtq:", rows)
        return rows

    def get_most_recent_rows(self) -> HoldingsRows:
        # Based on: https://www.sqlitetutorial.net/sqlite-max/
        sql_query = "SELECT uid, MAX(date), sid, quantity, value, "
        sql_query += "stop_loss, target, total "
        sql_query += "FROM {} ".format(self._table_name)
        sql_query += "GROUP BY sid "
        rows = self._get_rows(sql_query)
        return rows

    def get_quantities(self):
        """Return a list of tuples.
        Each tuple contains (security id, quantity).
        """
        quantities = []
        cursor = self._get_cursor()
        sql_query = "SELECT sid, quantity "
        sql_query += "FROM {} ".format(self._table_name)
        sql_query += "ORDER BY sid ASC"
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

import sys
import traceback
import sqlite3
from datetime import datetime
from typing import List
from database.utils import str_to_datetime


class SummaryRow:
    """Used to name the row values."""

    def __init__(self) -> None:
        self.date_obj = datetime(1900, 1, 1)
        self.ticker = ""
        self.security_name = ""
        self.quantity = 0.0
        self.price = 0.0
        self.value = 0.0
        self.stop_loss = 0.0
        self.target = 0.0
        self.total = 0.0

    def set(
        self,
        date_obj: datetime,
        ticker: str,
        security_name: str,
        quantity: float,
        price: float,
        value: float,
        stop_loss: float,
        target: float,
        total: float,
    ) -> None:
        self.date_obj = date_obj
        self.ticker = ticker
        self.security_name = security_name
        self.quantity = quantity
        self.price = price
        self.value = value
        self.stop_loss = stop_loss
        self.target = target
        self.total = total

    def set_from_raw(self, raw_row) -> None:
        self.date_obj = str_to_datetime(raw_row[0])
        self.ticker = raw_row[1]
        self.security_name = raw_row[2]
        self.quantity = raw_row[3]
        self.price = raw_row[4]
        self.value = raw_row[5]
        self.stop_loss = raw_row[6]
        self.target = raw_row[7]
        self.total = raw_row[8]


SummaryRows = List[SummaryRow]


class SummaryTable:
    """
    An interface to the SQLite query that creates the Summary table.

    Note: The Summary table is formed from an inner join of the Holdings
    and Securities tables.
    """

    def __init__(self, file_name) -> None:
        self._file_name = file_name
        self._holdings_table_name = "Holdings"
        self._securities_table_name = "Securities"

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

    def _get_rows(self, sql_query) -> SummaryRows:
        rows = []
        cursor = self._get_cursor()
        try:
            cursor.execute(sql_query)
            for raw_row in cursor:
                row = SummaryRow()
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

    def get_all_rows(self) -> SummaryRows:
        sql_query = "SELECT "
        sql_query += "date, "
        sql_query += "ticker, "
        sql_query += "name, "
        sql_query += "quantity, "
        sql_query += "price, "
        sql_query += "value, "
        sql_query += "stop_loss, "
        sql_query += "target, "
        sql_query += "total "
        sql_query += "FROM {} ".format(self._holdings_table_name)
        sql_query += "INNER JOIN {} ".format(self._securities_table_name)
        sql_query += "ON {}.sid = {}.uid ".format(
            self._holdings_table_name, self._securities_table_name
        )
        print("summary '{}'".format(sql_query))
        rows = self._get_rows(sql_query)
        return rows

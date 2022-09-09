import sqlite3
from datetime import date, datetime
from typing import List


class HoldingsRow:
    """Used to name the row values."""

    def __init__(self) -> None:
        self.uid = 0
        self.date_obj = datetime(1900, 1, 1)
        self.sid = 0.0
        self.quantity = 0.0
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
        value: float,
        stop_loss: float,
        target: float,
        total: float,
    ) -> None:
        self.uid = uid
        self.date_obj = date_obj
        self.sid = sid
        self.quantity = quantity
        self.value = value
        self.stop_loss = stop_loss
        self.target = target
        self.total = total

    def set_from_raw(self, raw_row) -> None:
        self.uid = raw_row[0]
        self.date_obj = raw_row[1]
        self.sid = raw_row[2]
        self.quantity = raw_row[3]
        self.value = raw_row[4]
        self.stop_loss = raw_row[5]
        self.target = raw_row[6]
        self.total = raw_row[7]


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

    def _release_cursor(self) -> None:
        self.connection.commit()
        self.connection.close()

    def _create_holdings_table(self, cursor) -> None:
        # Create holdings table.
        sql_query = "CREATE TABLE IF NOT EXISTS "
        sql_query += self._table_name
        sql_query += " (uid INTEGER"
        sql_query += " PRIMARY KEY AUTOINCREMENT NOT NULL,"
        sql_query += " date timestamp NOT NULL,"
        sql_query += " sid INTEGER NOT NULL,"
        sql_query += " quantity REAL NOT NULL, "
        sql_query += " value REAL NOT NULL, "
        sql_query += " stop_loss REAL NOT NULL,"
        sql_query += " target REAL NOT NULL, "
        sql_query += " total REAL NOT NULL"
        sql_query += ");"
        print(sql_query)
        cursor.execute(sql_query)

    def create(self) -> None:
        cursor = self._get_cursor()
        self._create_holdings_table(cursor)
        self._release_cursor()

    def add_test_rows(self) -> None:
        row = HoldingsRow()
        row.set(0, date(2022, 5, 12), 1, 81, 4.75, 3.90, 5.95, 384.75)
        self.add_row(row)
        row.set(0, date(2022, 5, 12), 2, 100, 2.00, 1.60, 3.25, 200.00)
        self.add_row(row)
        row.set(0, date(2022, 5, 19), 1, 81, 4.85, 3.95, 5.95, 392.85)
        self.add_row(row)

    def add_row(self, row: HoldingsRow) -> None:
        cursor = self._get_cursor()
        sql_query = "INSERT INTO {} ".format(self._table_name)
        sql_query += "(date, sid, quantity, value, "
        sql_query += "stop_loss, target, total) "
        sql_query += "VALUES ('{}', {}, {}, {}, {}, {}, {})".format(
            row.date_obj,
            row.sid,
            row.quantity,
            row.value,
            row.stop_loss,
            row.target,
            row.total,
        )
        print("Adding row [", sql_query, "]")
        cursor.execute(sql_query)
        self._release_cursor()

    def get_all_rows(self) -> HoldingsRows:
        rows = []
        cursor = self._get_cursor()
        sql_query = "SELECT * FROM " + self._table_name
        try:
            cursor.execute(sql_query)
            for raw_row in cursor:
                row = HoldingsRow()
                row.set_from_raw(raw_row)
                rows.append(row)
                # print(row.date_obj)
        except sqlite3.OperationalError:
            print("ERROR: No table", self._table_name)
        self._release_cursor()
        return rows

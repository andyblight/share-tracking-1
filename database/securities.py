import sqlite3


class SecuritiesTable:
    def __init__(self, file_name):
        self._file_name = file_name
        self._table_name = "Securities"
        self._connection = None

    def _get_cursor(self):
        self._connection = sqlite3.connect(
            self._file_name, detect_types=sqlite3.PARSE_COLNAMES
        )
        cursor = self._connection.cursor()
        return cursor

    def _release_cursor(self):
        self._connection.commit()
        self._connection.close()

    def create_securities_table(self, cursor):
        # Create securities table.
        sql_query = "CREATE TABLE IF NOT EXISTS "
        sql_query += self._table_name
        sql_query += " (uid INTEGER"
        sql_query += " PRIMARY KEY AUTOINCREMENT NOT NULL,"
        sql_query += " ticker TEXT NOT NULL,"
        sql_query += " name TEXT NOT NULL"
        sql_query += ");"
        print(sql_query)
        cursor.execute(sql_query)

    def create(self):
        cursor = self._get_cursor()
        self.create_securities_table(cursor)
        self._release_cursor()

    def add_test_rows(self):
        self.add_row("ABCD.L", "Alphabet Corporation")
        self.add_row("BR.L", "British Railways Limited")
        self.add_row("Fund", "MAN GLG UNDERVAL AST PROFESSIONAL C ACC")

    def add_row(self, ticker, name):
        ticker_upper = ticker.upper()
        cursor = self._get_cursor()
        sql_query = "INSERT INTO {} ".format(self._table_name)
        sql_query += "(ticker, name) "
        sql_query += "VALUES ('{}', '{}')".format(ticker_upper, name)
        print("Adding row [", sql_query, "]")
        cursor.execute(sql_query)
        self._release_cursor()

    def get_all_rows(self):
        cursor = self._get_cursor()
        sql_query = "SELECT * FROM " + self._table_name
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        self._release_cursor()
        return rows

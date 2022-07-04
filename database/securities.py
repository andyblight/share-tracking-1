import sqlite3


class SecuritiesTable:
    def __init__(self, file_name):
        self._file_name = file_name
        self._table_name = "Securities"

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
        connection = sqlite3.connect(self._file_name)
        cursor = connection.cursor()
        # Create table if not existing.
        self.create_securities_table(cursor)
        connection.commit()
        connection.close()

    def add_test_rows(self):
        self.add_row("ABCD.L", "Alphabet Corporation")
        self.add_row("BR.L", "British Railways Limited")

    def add_row(self, ticker, name):
        connection = sqlite3.connect(self._file_name)
        cursor = connection.cursor()
        sql_query = "INSERT INTO {} ".format(self._table_name)
        sql_query += "(ticker, name) "
        sql_query += "VALUES ('{}', '{}')".format(ticker, name)
        print("Adding row [", sql_query, "]")
        cursor.execute(sql_query)
        connection.commit()
        connection.close()

    def get_all_rows(self):
        connection = sqlite3.connect(self._file_name)
        cursor = connection.cursor()
        sql_query = "SELECT * FROM " + self._table_name
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        connection.close()
        return rows

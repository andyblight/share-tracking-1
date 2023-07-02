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

    def _commit_cursor(self):
        self._connection.commit()
        self._connection.close()

    def _create_securities_table(self, cursor):
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
        self._create_securities_table(cursor)
        self._commit_cursor()

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
        self._commit_cursor()

    def get_all_rows(self):
        rows = []
        cursor = self._get_cursor()
        sql_query = "SELECT * FROM " + self._table_name
        try:
            cursor.execute(sql_query)
            rows = cursor.fetchall()
        except sqlite3.OperationalError:
            print("ERROR: No table", self._table_name)
        self._connection.close()
        return rows

    def _query_security(self, security_description_upper):
        # Find existing security.
        rows = []
        cursor = self._get_cursor()
        sql_query = "SELECT * FROM " + self._table_name
        sql_query += " WHERE name LIKE '"
        sql_query += security_description_upper
        sql_query += "'"
        print(sql_query)
        try:
            cursor.execute(sql_query)
            rows = cursor.fetchall()
        except sqlite3.OperationalError:
            print("ERROR: No table", self._table_name)
        self._connection.close()
        return rows

    def get_security(self, security_description):
        security_description_upper = security_description.upper()
        # Try match for first 10 characters.
        accurate_match = True
        query_str = security_description_upper[:10] + "%"
        rows = self._query_security(query_str)
        if len(rows) < 1:
            accurate_match = False
            # Try match of first 5 characters.
            query_str = security_description_upper[:5] + "%"
            rows = self._query_security(query_str)
            if len(rows) < 1:
                # Try for 6 character match anywhere.
                query_str = "%" + security_description_upper[:6] + "%"
                rows = self._query_security(query_str)
                if len(rows) < 1:
                    # Try to 3 character match anywhere.
                    query_str = "%" + security_description_upper[:3] + "%"
                    rows = self._query_security(query_str)
        return (accurate_match, rows)

    def _get_ticker(self, security_description):
        # TODO Find ticker from security name.
        ticker = "TEMP.L"
        return ticker

    def get_security_from_ticker(self, ticker):
        ticker_upper = ticker.upper()
        # Find existing security.
        rows = []
        cursor = self._get_cursor()
        sql_query = "SELECT * FROM " + self._table_name
        sql_query += " WHERE ticker LIKE '"
        sql_query += ticker_upper
        sql_query += "'"
        print(sql_query)
        try:
            cursor.execute(sql_query)
            rows = cursor.fetchall()
        except sqlite3.OperationalError:
            print("ERROR: No table", self._table_name)
        self._connection.close()
        return rows

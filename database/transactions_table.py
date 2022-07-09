import pandas
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

    def _get_clean_df(self):
        # Create an empty DF based on the SQL table values.
        self.connection = sqlite3.connect(
            self._file_name, detect_types=sqlite3.PARSE_COLNAMES
        )
        # print("Test read all rows")
        df = pandas.read_sql_query(
            "SELECT * FROM {}".format(self._table_name), self.connection
        )
        self.connection.close()
        # df.info()
        clean_df = df[0:0]
        # clean_df.info()
        return clean_df

    def _copy_excel_to_df(self, excel_df, clean_df):
        # The rows from the spreadsheet look like this:
        #
        # Header row: Pandas(Index=2, _1='Date', _2='Description',
        # _3='Sedol', _4='Stock Description', _5='Contract Reference',
        # _6='Price', _7='Debit', _8='Credit', At='Settlement Date', _10='Balance')
        #
        # Sample row: Pandas(Index=8, _1='23-Nov-2020',
        # _2='1057 BEEK FINL  Del     .93 S Date 25/11/20', _3='BZ0X8W1',
        # _4='BEEKS FINANCIAL CL ORD GBP0.00125', _5='N45263',
        # _6=0.93399, _7=998.74, _8=0, At='25-Nov-2020', _10=7340.12)
        #
        # Output format:
        # 0|uid|INTEGER|1||1
        # 1|date|timestamp|1||0
        # 2|type|CHAR(1)|1|'N'|0
        # 3|security_id|INTEGER|1||0
        # 4|quantity|REAL|1||0
        # 5|price|REAL|1||0
        # 6|fees|REAL|1||0
        # 7|tax|REAL|1||0
        # 8|total|REAL|1||0

        # Copy and convert data from the Excel DF.
        start_index = 3
        end_index = excel_df.index[-9]
        # print("Indices:", start_index, end_index)
        # Only process range of rows.
        for row in excel_df.loc[start_index:end_index].itertuples(index=True):
            # print("Data row:", row._1)
            index = row.Index
            # Copy easy values.
            clean_df[index].date = date(row._1).timestamp()
            clean_df[index].price = row._6
            # Extract info from _2='Description'
            description = row._2.split()
            clean_df[index].quantity = float(description[0])
            clean_df[index].fees = clean_df[index].total - (
                clean_df[index].quantity * clean_df[index].price
            )
            # Buy/sell related info.
            if row._7 > row._8:
                clean_df[index].type = "B"
                clean_df[index].total = row._7
            else:
                clean_df[index].type = "S"
                clean_df[index].total = row._8
            # Look up security from _4='Stock Description'
            # TODO
            clean_df[index].security_id = 1
            return clean_df

    def import_file(self, filename):
        print("Transactions->ImportFile", filename)
        excel_df = pandas.read_excel(filename)
        clean_df = self._get_clean_df()
        clean_df = self._copy_excel_to_df(excel_df, clean_df)
        print("Row", clean_df[1])

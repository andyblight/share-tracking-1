import sqlite3
from pathlib import Path


class SecuritiesDatabase:
    def __init__(self):
        self.__file_name = "shares.db"
        self.__table_name = "shares"

    def create(self):
        con1 = sqlite3.connect(self.__file_name)
        cur1 = con1.cursor()
        sql_query = "CREATE TABLE IF NOT EXISTS "
        sql_query += self.__table_name
        sql_query += "(ticker text, name text, quantity real, price real)"
        cur1.execute(sql_query)
        con1.commit()
        con1.close()

    def add_fake_rows(self):
        con1 = sqlite3.connect(self.__file_name)
        cur = con1.cursor()
        cur.execute("INSERT INTO shares VALUES ('FRED', 'Frederick', '12', '75.4')")
        cur.execute("INSERT INTO shares VALUES ('BERT', 'Bertrand', '34', '175.4')")
        cur.execute("INSERT INTO shares VALUES ('TOM', 'Thomas', '256', '275.4')")
        con1.commit()
        con1.close()

    def add_record(self, ticker, name, quantity_float, price_float):
        con1 = sqlite3.connect(self.__file_name)
        cur = con1.cursor()
        row_string = "('" + ticker + "',"
        row_string += "'" + name + "',"
        row_string += "'" + str(quantity_float) + "',"
        row_string += "'" + str(price_float) + "')"
        print("Adding row [", row_string, "]")
        cur.execute("INSERT INTO shares VALUES " + row_string)
        con1.commit()
        con1.close()

    def get_all_rows(self):
        con1 = sqlite3.connect(self.__file_name)
        cur1 = con1.cursor()
        sql_query = "SELECT * FROM " + self.__table_name
        cur1.execute(sql_query)
        rows = cur1.fetchall()
        con1.close()
        return rows

    def is_present(self):
        db_file = Path(self.__file_name)
        return db_file.is_file()

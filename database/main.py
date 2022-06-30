# The main database file.
# This class owns all tables in the database.
import sqlite3
from pathlib import Path

from database.securities import SecuritiesTable
from database.transactions import TransactionsTable


class SharesDatabase:
    def __init__(self):
        self._file_name = "shares.db"
        # TODO Add tables owned by this class.
        self.securities = SecuritiesTable(self._file_name)
        self.transactions = TransactionsTable(self._file_name)

    def get_file_name(self):
        return self._file_name

    def is_present(self):
        db_file = Path(self._file_name)
        return db_file.is_file()

    def create(self):
        # Add empty tables.
        print("SharesDB.create")
        self.securities.create()
        self.transactions.create()

    def add_test_rows(self):
        print("SharesDB.add test rows")
        self.securities.add_test_rows()
        self.transactions.add_test_rows()

    def _dump_table_info(self):
        print("SharesDB.dump table info")
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(tables)
        cursor.close()
        db.close()

    def dump_tables(self):
        print("SharesDB.dump tables")
        self._dump_table_info()
        # self.securities.dump()
        # self.transactions.dump()


database = SharesDatabase()

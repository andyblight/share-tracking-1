import pandas
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime

from database.main import database
from ui.select_security_dialog import SelectSecurityDialog
from ui.user_settings import UserSettings


class ImportTransactionsDialog:
    def __init__(self, parent):
        self.parent = parent

    def _get_filename(self):
        # Open file.
        filetypes = (
            ("Excel files", "*.xlsx"),
            ("CSV files", "*.csv"),
            ("All files", "*.*"),
        )
        initial_dir = UserSettings().get_import_path()
        filename = filedialog.askopenfilename(
            parent=self.parent,
            title="Open a file",
            initialdir=initial_dir,
            filetypes=filetypes,
        )
        return filename

    def _get_security_id(self, security_name):
        security_id = 0
        rows = database.securities.get_security(security_name[:6])
        num_ids = len(rows)
        if num_ids == 1:
            security_id = rows[0][0]
        elif num_ids > 1:
            security_dialog = SelectSecurityDialog(self.parent, rows)
            self.parent.wait_window(security_dialog.top)
            security_id = security_dialog.get_security_id()
            print("DEBUG: Returned security_id: ", security_id)
        else:
            print("Security Id not found for ", security_name)
        return security_id

    def _write_df_to_db(self, excel_df):
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
        # SQLite output format.
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
            # Share purchases or sales start with a quantity.
            # Everything else is a string and can be ignored.
            # Extract info from _2='Description'
            description = row._2.split()
            # print(description)
            try:
                quantity = float(description[0])
                # We have a number so copy date into the new row and write to DB.
                # Convert date from string to datetime object.
                date_obj = datetime.strptime(row._1, "%d-%b-%Y")
                # Look up security from _4='Stock Description'
                security_id = self._get_security_id(row._4)
                # Copy price.
                price = row._6
                # Buy/sell related info.
                if row._7 > row._8:
                    type = "B"
                    total = row._7
                else:
                    type = "S"
                    total = row._8
                # Calculate fees.
                costs = total - (quantity * price)
                # Append new row.
                database.transactions.add_row(
                    date_obj, type, security_id, quantity, price, costs, total
                )
            except ValueError:
                # Ignore this row.
                pass

    def import_file(self):
        # Import the CSV data into the transactions table.
        filename = self._get_filename()
        print("Importing transactions file", filename)
        excel_df = pandas.read_excel(filename)
        self._write_df_to_db(excel_df)

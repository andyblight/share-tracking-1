import pandas
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import date

from database.main import database


class ImportFileDialog:
    def __init__(self, parent):
        self.parent = parent

    def import_file(self):
        # Import the CSV data into the transactions table.
        filename = self._get_filename()
        print("Importing transactions file", filename)
        excel_df = pandas.read_excel(filename)
        clean_df = database.transactions.get_clean_df()
        filled_df = self._copy_excel_to_df(excel_df, clean_df)
        database.transactions.write_df(filled_df)

    def _get_filename(self):
        # Open file.
        filetypes = (
            ("Excel files", "*.xlsx"),
            ("CSV files", "*.csv"),
            ("All files", "*.*"),
        )
        filename = filedialog.askopenfilename(
            parent=self.parent,
            title="Open a file",
            initialdir="~/Documents",
            filetypes=filetypes,
        )
        return filename

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
            print(type(clean_df[index].date))
            clean_df[index].date = date(row._1)
            clean_df[index].price = row._6
            # Extract info from _2='Description'
            description = row._2.split()
            clean_df[index].quantity = float(description[0])
            # Fees
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
            clean_df[index].security_id = self._get_security(row._4)
            return clean_df

    def _get_security(self, security_description):
        security_id = database.securities.find_security(security_description)
        if security_id < 0:
            # Not found so add the security.
            ticker = self._get_ticker(security_description)
            database.securities.add_row(ticker, security_description)
        return security_id

    def _get_ticker(self, security_description):
        # TODO Find ticker from security name.
        ticker = "TEMP.L"
        return ticker

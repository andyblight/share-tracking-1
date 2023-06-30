import pandas
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime

from database.main import database
from ui.user_settings import UserSettings


class SecuritiesImportDialog:
    def __init__(self, parent):
        self._parent = parent

    def import_file(self):
        # Import the CSV data into the transactions table.
        filename = self._get_filename()
        print("Importing securities file", filename)
        csv_df = pandas.read_csv(filename, sep="\t", encoding="utf-8")
        self._write_df_to_db(csv_df)

    def _get_filename(self):
        # Open file.
        filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
        initial_dir = UserSettings().get_import_path()
        filename = filedialog.askopenfilename(
            parent=self._parent,
            title="Open a file",
            initialdir=initial_dir,
            filetypes=filetypes,
        )
        return filename

    def _write_df_to_db(self, csv_df):
        # print(csv_df)
        # The rows from the dataframe after import look like this:
        #      Symbol                                      Description
        # 0      02NG  STATOILHYDRO ASA 6.125% NOTES 27/11/28 GBP(VAR)
        # 1      0A0B                                AHLERS AG ORD NPV
        # 2      0A0C                       AHLERS AG NON VTG PREF NPV
        # 3      0A1H     MILANO ASSICURAZIONI DI RISP EUR0.52(NON CV)
        # 4      0A1U                                              NaN
        #
        # To get this into the database, we ignore the first line (header text),
        # and add all other lines mapping:
        #   Symbol to ticker
        #   Description to name
        start_index = 1
        # Only process range of rows.
        for row in csv_df.loc[start_index:].itertuples(index=True):
            # Append new row.
            ticker = row.Symbol
            if len(ticker) <= 4:
                try:
                    name = str(row.Description)
                    # Replace single quotes with back ticks like all the other
                    # "quote characters" int he CSV file.
                    security = name.replace("'", "`")
                    # print("Ticker:'", ticker, "', security:'", security, "'")
                    database.securities.add_row(ticker, security)
                except Exception as e:
                    print("ERROR: ", repr(e))
                    sys.exit()

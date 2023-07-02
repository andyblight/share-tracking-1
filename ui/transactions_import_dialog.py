import csv
import locale
import pandas
import re
from tkinter import filedialog
from datetime import datetime

from database.main import database
from database.transactions_table import TransactionsRow
from ui.securities_add_dialog import SecuritiesAddDialog
from ui.select_security_dialog import SelectSecurityDialog
from ui.user_settings import UserSettings


def _currency_string_to_float(string) -> float:
    # There is no pre-built way to do this.  Why not???
    clean_string = re.sub(r"[^.0-9]", "", string)
    try:
        result = float(clean_string)
    except ValueError:
        result = 0.0
        pass
    # print("Input: {}, clean: {}, value {}".format(string, clean_string, result))
    return result


def _extract_ii_description(string) -> tuple[bool, float, float]:
    description = string.split()
    print("Description", description)
    dividend = False
    quantity = 0.0
    price = 0.0
    if description[0] == "Div":
        dividend = True
        quantity = float(description[1])
        # This is no price for dividends.
    else:
        quantity = float(description[0])
        # There are a variable number of items between quantity and price.
        # Before the price, there is always "Del"
        found_del = False
        for item in description:
            if found_del:
                price = float(item)
                break
            if item == "Del":
                found_del = True
    return (dividend, quantity, price)


class TransactionsImportDialog:
    def __init__(self, parent):
        self.parent = parent

    def import_file(self):
        filename = self._get_filename()
        print("Importing transactions file", filename)
        import_source = "II"
        if import_source == "II":
            self._import_ii_csv(filename)
        elif import_source == "CSD":
            # Import the Excel data into the transactions table.
            excel_df = pandas.read_excel(filename)
            self._write_csd_df_to_db(excel_df)

    def _get_filename(self):
        # Open file.
        filetypes = (
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
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
        (accurate_match, rows) = database.securities.get_security(security_name)
        num_ids = len(rows)
        if num_ids == 1 and accurate_match:
            security_id = rows[0][0]
            print(
                "DEBUG: Exact match for security: ", security_name, " is ", rows[0][2]
            )
        elif num_ids > 1:
            print("DEBUG: Choosing security id from name: ", security_name)
            security_dialog = SelectSecurityDialog(self.parent)
            security_dialog.set_description(security_name)
            security_dialog.set_rows(rows)
            security_dialog.wait()
            security_id = security_dialog.get_security_id()
            print("DEBUG: Returned security_id: ", security_id)
        # If not found, then try adding the security manually.
        if security_id <= 0:
            # No security ID so manually add a new security.
            print("Security Id not found for ", security_name)
            add_dialog = SecuritiesAddDialog(self.parent)
            add_dialog.set_description(security_name)
            add_dialog.wait()
            # Check that security ID can be found.
            (accurate_match, rows) = database.securities.get_security(security_name)
            if accurate_match:
                # Exact match.
                security_id = rows[0][0]
            else:
                print(
                    "ERROR: Multiple matches in database for security: ", security_name
                )
                print(rows)
                print("")

        return security_id

    def _write_csd_df_to_db(self, excel_df):
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
        #
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
                new_row = TransactionsRow()
                new_row.set(date_obj, type, security_id, quantity, price, costs, total)
                database.transactions.add_row(new_row)
            except ValueError:
                # Ignore this row.
                pass

    def _extract_ii_data(self, row) -> None:
        # The rows from the CSV file look like this:
        # Header row
        # Date,Settlement Date,Symbol,Sedol,Description,Reference,
        #   Debit,Credit,Running Balance
        # One line of data:
        # ['15/06/2023', '19/06/2023', 'NXT', '1234567',
        #  '15 NEXT  Del   64.58 S Date 19/06/23', '12345AA6AAA',
        #  '£973.66', 'n/a', '£1,000.00']
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
        #
        # If the symbol is not "n/a" the it is buy, sell or dividend.
        # Everything else can be ignored.
        if row[2] != "n/a":
            # Found one.
            # Tease apart the description.
            (dividend, quantity, price) = _extract_ii_description(row[4])
            # Ignore dividends for now.
            if dividend:
                print("Found dividend")
            else:
                # Use settlement date.
                date_obj = datetime.strptime(row[1], "%d/%m/%Y")
                # Security ID is from Symbol column.
                security_id = self._get_security_id(row[2])
                # Buy if debit is not "n/a".
                if row[6] != "n/a":
                    type = "B"
                    total = _currency_string_to_float(row[6])
                else:
                    type = "S"
                    total = _currency_string_to_float(row[7])
                costs = total - (quantity * price)
                print(
                    "Extracted",
                    date_obj,
                    security_id,
                    type,
                    quantity,
                    price,
                    costs,
                    total,
                )
                # Append new row.
                new_row = TransactionsRow()
                new_row.set(date_obj, type, security_id, quantity, price, costs, total)
                database.transactions.add_row(new_row)

    def _import_ii_csv(self, filename) -> None:
        with open(filename, newline="") as csv_file:
            ii_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
            i = 0
            for row in ii_reader:
                if i > 0:
                    # print(i, row)
                    # Extract data from row.
                    self._extract_ii_data(row)
                i += 1

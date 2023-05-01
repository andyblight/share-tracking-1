# Design Notes

## Database schema

One of the things that it really helps to get right is the database schema.
Getting this right is important as most of the effort of creating an
application that uses a database is the GUI and that is very dependent on the
information that the user needs to view and change.

### Securities

The first table is the `securities`.  Each security has the following
attributes:

| Field name | Type | Notes |
|---|---|---|
| Unique ID | Integer | Unique ID for each security. |
| Ticker | Text | The 3 or 4 letter code use for each share. EPIC is LSE term. |
| Name | Text | The long name for the security. |

The `securities` table has been split out as other data that related to the
security might need to be added at a later date.

### Transactions

The `transaction` table where the purchase and sale records are stored.  The
attributes are:

| Field name | Type | Notes |
|---|---|---|
| Unique ID | Integer | Unique ID for each transaction. |
| Date | Date | The date of the transaction. |
| Security ID | Integer | Link to the security unique ID. |
| Transaction Type | Text | Short name for the transaction type e.g. `Buy`, `Sell`.|
| Quantity | Real | The number of things involved in the transaction.|
| Price | Real | The price paid per unit. |
| Fees | Real | Commission or other fees. |
| Tax | Real | Stamp duty in the UK. |
| Total | Real | Total cost paid.  Should be (Quantity * Price) + Fees + Tax. |

### Holdings

The `holdings` table holds information about the current value of each of the
securities held.  This table is generated from:

* The transaction data:
    * security Id.
    * quantity bought/sold.
    * price.
* The valuation data:
    * "current" value of a single share.
    * stop/loss value.
    * target value.

The valuation date will initially be entered using a dialog box.

We end up with a table that looks like this:

| Field name | Type | Notes |
|---|---|---|
| Unique ID | Integer | Unique ID for each holding record. |
| Date | Date | The date of the update. |
| Security ID | Integer | Link to the security unique ID. |
| Quantity | Real | The total number of units held. |
| Price | Real | The price paid per unit. |
| Value | Real | The valuation for each unit. |
| Gain | Real | Change in value since purchased. |
| StopLoss | Real | Sell at this price. |
| Target | Real | Target value. |
| Total | Real | (Quantity * Value) |

Holdings records should work as per the
[spreadsheet](TransactionHoldingInteraction.ods)
but have more fields for stop loss and target values.

The valuation wil be based on share price data that is downloaded as a file.
For now, this will be a file from EODData.com.

## Reports

The objective of this project is to give me better information about the
securities I have purchased so that I can make better financial decisions.  To this end, I need the following reports.

### Security value over time

For each security held, I want to be able to see how the security is
progressing.  To do this, I need this information:

* Purchase price.
* Price at the end of each week.
* A graph of progress of each security would be ideal.

## References

* <https://tkdocs.com/tutorial/tree.html>
* <https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Treeview.html>
* <https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/grid-config.html>

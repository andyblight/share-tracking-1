# Share Tracking Database

Python wrapper around a SQLite database that is used to track the buying and
selling of my shares.

## Usage


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
| Price | Real | The price per unit. |
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
    * value of a single share.
    * stop/loss value.
    * target value.

The valuation date will initially be entered using a dialog box.

We end up with a table that looks like this:

| Field name | Type | Notes |
|---|---|---|
| Unique ID | Integer | Unique ID for each transaction. |
| Date | Date | The date of the transaction. |
| Security ID | Integer | Link to the security unique ID. |
| Quantity | Real | The number of unit involved in the transaction.|
| Value | Real | The valuation for each unit. |
| StopLoss | Real | Sell at this price. |
| Target | Real | Target value. |
| Total | Real | (Quantity * Value) |

Holdings records should work as per the (spreadsheet)[]
but have more fields for stop loss and target values.

## Future plans

Time permitting, I would like to pull in the "end of day" data and do some
clever stuff like:
- Report on crystallized profits.
- Report on potential profits so far.
- Rate of growth, % per month, ideally with graph.

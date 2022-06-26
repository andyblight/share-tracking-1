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
| Security ID | Integer | Link to the security unique ID. |
| Date | Date | The date of the transaction. |
| Transaction Type | Text | Short name for the transaction type e.g. `Buy`, `Sell`.|
| Quantity | Real | The number of things involved in the transaction.|
| Price | Real | The price per unit. |
| Fees | Real | Commission or other fees. |
| Tax | Real | Stamp duty in the UK. |
| Total | Real | Total cost paid.  Should be (Quantity * Price) + Fees + Tax. |

### Holdings

The `holdings` table holds information about the current value of each of the
securities held.  This table is generated from the transaction data and is
not quite so obvious as the previous tables as can be seen using the following
example for a single security.

1. Buy 200 shares.
2. Buy 200 shares.  Total holding 400.
3. Sell 100 shares.  Total holding 300.
4. Sell 100 shares.  Total holding 200.
5. Sell 100 shares.  Total holding 100.
6. Sell 100 shares.  Total holding 0.

At any point, I want to generate performance information about the security
including historical performance.  After a lot of thought, I decided the best
way to do this was to create a new holding record after each transaction.

The attributes are:

| Field name | Type | Notes |
|---|---|---|
| UniqueID | Integer | Unique ID for each holding record. |
| SecurityID | Integer | Link to the security unique ID. |
| Status | Text | Open = holding is active, Closed = sale occurred |
| Created | Date | Date when the record was created. |
| UnitCost | Real | Price per share. |
| TotalCost | Real | Total paid. |
| Closed | Date | Date when the record was finalised. |
| UnitSale | Real | Unit value received. |
| TotalSale | Real | Total received. |
| Profit | Real | Total Sale - Total Cost. |

### Running

The `running` table of is to hold the latest information for the holdings.
The attributes are:

| Field name | Type | Notes |
|---|---|---|
| UniqueID | Integer | Unique ID for each running record. |
| HoldingID | Integer | Link to the holding unique ID. |
| StopLoss | Real | The stop loss value. |
| Target | Real | The target value. |
| Value | Real | The current value of the holding. |

NOTE: The above tables and content may be different in the code, so beware!

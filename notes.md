# Notes

Notes made during coding.

## Updating holdings from transactions

Implemented in `HoldingsUpdateDialog.update`.

This function started to make my head hurt so I decided to try proper design
for once.

### Iteration 1

#### Pre-requisites

A filtered list of the transactions is available.  This list will have a
single record of every security bought or sold with the current number of
shares held.

The current holdings table.

#### Analysis

Case 1: There is a transaction entry that has no holding entry at all.
    This is when the security was first purchased or initial import.
    Add new holding record based on the transaction info.

Case 2: Filtered transactions entry has one or more holding entry.
    This is going to happen most times.
    There are going to be many holdings records for each security held.
    However, for this function we need to know the number of shares held in
    the record nearest the date and time that the update is taking place.
    The other records can be ignored.

    So this implies that we need to provide a filtered list of holdings to
    this function.

### Iteration 2

#### Pre-requisites

A list of transaction records that has a single record of every security
bought or sold with the current quantity of shares held including securities
with 0 shares.  Each record returned is the last transaction for that security.

A filtered list of the current holdings table is available.  This list will
only contain the most up to date holdings records (nearest datetime.now()).

#### Analysis

Case 1: There is a transaction entry that has no holding entry at all.
    This is when the security was first purchased or initial import.
    Add new holding record based on the transaction info.

Case 2: Filtered transactions entry has a matching holding entry.
    When this happens, compare the quantity values of both.
    If they are different, add a new record.
    Else do nothing.

This looks pretty simple so now I have the following things to do:

1. Change the filtered list of transactions to include zero quantity values.
2. Get a filtered list of holdings with only the most recent records.  This is
probably best done using a new SQL query.
3. Implement the rest of the code.

### Iteration 3

It was after I got most of iteration 2 working that I realised that I had
missed the whole point!

#### Description

After the import, there should be exactly one matching holding record for each
transaction record.

The holding record matches the transaction record when:

1. The security IDs match.
2. The dates match.
3. The absolute quantities match.  Holdings stores the quantity as positive for
buy and negative for sell.

Other holdings records are added for valuation and tracking purposes.

The only things we have to be careful about is making sure that only new
transactions are added to the holdings and existing holdings are not modified.

The holdings table will hold more records than the transactions database, so
we should iterate over the holdings once only.

#### Pre-requisites

All transaction records sorted in date order, oldest first.

All holdings records sorted in date order, oldest first.

#### Implementation

This looks much simpler than before so I'm just going to write this.

### Iteration 4

Got it wrong again.  Seems to be more difficult to get my head around than it
should be.

#### Analysis

These are the cases that we need to consider.

1. A security is only present the transactions table.

    **ACTION**: Add a new record holdings record for the security,
2. A security is present in the holdings table and occurs one or more times in
the transactions table.
    1. The security appears exactly once in the transaction table.

        **ACTION**: Do nothing as this is correct.
    2. The security appears more than once in the transaction table.
        1. The total quantity for a given security held is zero.

            **ACTION**: Delete the holding record.
        2. The total quantity for a given security held is greater than zero.
            1. The quantity held is equal to the total quantity from the
            transaction table.

            **ACTION**: Do nothing as the holdings value is correct.
            2. The quantity held is not equal to the total quantity from the
            transaction table.

            **ACTION**: Update the holding record with:
                    1. The quantity total from the transactions table.
                    2. The latest date from the transactions table.
        3. The total quantity for a given security held is less than zero.

            **ACTION**: This is an error case.  The transaction may have been
            entered incorrectly so prompt user to check the transactions for
            this security.
3. A security is only present in the holdings table.
    * ACTION: This is an error case.  This should never happen.  How do we
    handle this error condition?

#### Implementation

```python
transactions_quantities = database.transactions.get_quantities()
holdings_quantities = database.holdings.get_quantities()
for transaction in transactions_quantities:
    if transaction.quantity == 0:
        # Delete holding.
    elif transaction.quantity > 0:
        for holding in holdings_quantities:
            if holding.sid == transaction.sid:
                if holding.quantity != transaction.quantity:
                    # Update holding.
    else:
        # Print error message.
```

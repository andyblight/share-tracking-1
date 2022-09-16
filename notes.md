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

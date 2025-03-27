# Graph Improvements

## Objective

The objective of this task was to modify the transaction graph to display data points in a more continuous manner, while still showing the x-axis labels by day.

## Problem

The original graph displayed data points only on the day level, which caused multiple transactions on the same day to overlap, resulting in a less informative visualization.

## Solution

The solution involved the following steps:

1.  **Attempted Virtual Timestamps:** Initially, I attempted to create virtual timestamps for each transaction based on its order within the day. This approach aimed to distribute the transactions evenly across the day. However, due to the lack of unique identifiers or timestamps in the data, I was unable to reliably sort the transactions within the same day, leading to incorrect plotting.

2.  **Horizontal Offset:** I reverted to the original approach of plotting all transactions on the same day at the same point. To improve the visualization, I added a small horizontal offset to each transaction to visually separate them. This offset is calculated based on the number of transactions for the selected month.

## Code Changes

### `src/data_processing.py`

The code that calculated virtual timestamps and the "Virtual Booking Date" column was removed.

### `src/visualization.py`

The `generate_monthly_graph` function was modified to add a horizontal offset to each transaction:

```python
offset = 0.1 / selected_data.shape[0]  # Small offset based on the number of transactions
ax1.plot(selected_data['Booking_Date'] + pd.to_timedelta(offset * selected_data.index, unit='D'), selected_data['Balance_After_Booking'], marker='o', color='skyblue')
```

This code calculates a small offset based on the number of transactions and adds it to the `Booking_Date` before plotting. The `pd.to_timedelta` function is used to convert the offset to a `timedelta` object, which can be added to the `Booking_Date` column (which is of type `datetime64[ns]`).

## Result

The resulting graph displays data points with a small horizontal offset to visually separate transactions on the same day, while still showing the x-axis labels by day. This provides a more informative and visually appealing representation of the transaction data.
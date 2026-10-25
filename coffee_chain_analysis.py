import numpy as np
import pandas as pd

rng = np.random.default_rng(7)

stores = pd.DataFrame({
    "store_id": [1, 2, 3, 4, 5],
    "city": ["Austin", "Dallas", "Houston", "Austin", "El Paso"],
    "opened": pd.to_datetime(["2023-03-01", "2024-06-15", "2022-11-01", "2026-02-01", "2025-01-10"]),
})

products = pd.DataFrame({
    "sku": ["A1", "A2", "B1", "B2", "C1", "C2"],
    "product": ["Latte", "Mocha", "Croissant", "Muffin", "Beans 1lb", "Beans 2lb"],
    "group": ["Drink", "Drink", "Food", "Food", "Retail", "Retail"],
    "price": [4.50, 5.25, 3.75, 3.25, 14.00, 26.00],
})

n = 1500
sales = pd.DataFrame({
    "ts": pd.to_datetime("2026-03-01") + pd.to_timedelta(rng.integers(0, 92 * 24 * 60, n), unit="min"),
    "store_id": rng.choice([1, 2, 3, 4, 5, 6], n, p=[.25, .2, .25, .15, .13, .02]),
    "sku": rng.choice(["A1", "A2", "B1", "B2", "C1", "C2", "D9"], n, p=[.3, .2, .2, .15, .08, .05, .02]),
    "qty": rng.integers(1, 4, n),
})
sales = pd.concat([sales, sales.sample(25, random_state=1)]).sample(frac=1, random_state=2).reset_index(drop=True)

#1. Find and remove exact duplicate rows. How many were there?
sales.duplicated().sum() #25 exact duplicates in sales
sales = sales.drop_duplicates() #removing duplicates and reassigning

#2. How many sales rows have a store_id or sku that doesn’t match the lookup tables? Find them without merging.
valid_rows = (sales['store_id'].isin(stores['store_id'])) & (sales['sku'].isin(products['sku']))
number_of_invalid_rows = 1500 - valid_rows.sum()
#sixty-four (64) sales rows have a store_id or sku that doesn't match the lookup tables

#3. Merge all three tables into one frame df. Which how= did you pick, and why? Prove your row count makes sense.
sales = sales.merge(right=stores, how='inner').merge(right=products, how='inner')

#4. Add revenue.
sales['revenue'] = sales['qty'] * sales['price']

#5. Daily total revenue for the whole chain as a Series indexed by date, with no missing days.
sales['date'] = sales['ts'].dt.normalize()
daily_total_revenue = sales.groupby('date')['revenue'].sum()
calendar = pd.date_range(start=sales['date'].min(), end=sales['date'].max(), freq='D')
daily_total_revenue = daily_total_revenue.reindex(calendar, fill_value=0)

#6. 7-day rolling average of #5. Which week had the best average?
rolling_avg = daily_total_revenue.rolling(7).mean()
rolling_avg.idxmax()
#The week of 2026-04-19 had the best average of 238.82142857142858

#7. Weekly revenue per city, cities as columns.
sales['week'] = sales['ts'].dt.to_period('W')
weekly_rev_per_city = sales.groupby(['week', 'city'])['revenue'].sum().unstack()
weekly_rev_per_city = weekly_rev_per_city[weekly_rev_per_city.index.start_time >= sales['date'].min()]

#8. Revenue by hour of day. What’s the peak hour?
sales['hour'] = sales['ts'].dt.hour
rev_per_hour = sales.groupby('hour')['revenue'].sum()
rev_per_hour.idxmax()
#hour 22 with 1010.00

#9. Store 4 opened recently. Compare its average daily revenue to the others. Is that fair to do with a plain mean?
daily_sums = sales.groupby(['store_id', 'date'])['revenue'].sum()
daily_sums = daily_sums.unstack(level='store_id', fill_value=0)
daily_sums.mean()
#A plain mean is fair because store 4 has been opened for all of the days in this data

#10. Month-over-month % change in revenue for each product group.
sales['month'] = sales['ts'].dt.to_period('M')
monthly_rev_per_product = sales.groupby(['month', 'group'])['revenue'].sum().unstack()
month_over_month_in_rev_per_group = monthly_rev_per_product.pct_change()*100
"""
group       Drink       Food     Retail
month                                  
2026-03       NaN        NaN        NaN
2026-04 -5.105297  -1.797540  -6.127451
2026-05  3.328850  22.904624  23.324630
"""

#Bonus: For each store, find the date of its single best day, and that day’s revenue.

best_day_df = sales.groupby(['store_id', 'date'])['revenue'].sum().unstack(level='store_id', fill_value=0)
best_day_df = best_day_df.agg(['idxmax', 'max']).T
"""
                       idxmax     max
store_id                             
1         2026-05-24 00:00:00   190.5
2         2026-05-09 00:00:00  162.25
3         2026-03-13 00:00:00   162.5
4         2026-04-10 00:00:00   178.5
5         2026-03-29 00:00:00  161.25
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 200

orders = pd.DataFrame({
    "order_id": np.arange(1001, 1001 + n),
    "order_date": pd.to_datetime("2026-01-01") + pd.to_timedelta(rng.integers(0, 180, n), unit="D"),
    "customer_id": rng.integers(1, 41, n),
    "category": rng.choice(["Electronics", "Clothing", "Home", "Toys", "Books"], n),
    "quantity": rng.integers(1, 6, n),
    "unit_price": rng.uniform(5, 200, n).round(2),
    "region": rng.choice(["North", "South", "East", "West"], n),
})

#Dirty it up
orders.loc[rng.choice(n, 10, replace=False), "unit_price"] = np.nan
orders.loc[rng.choice(n, 5, replace=False), "region"] = None

#1. How many rows and columns? What are the dtypes?
orders.info()
"""
<class 'pandas.DataFrame'>
RangeIndex: 200 entries, 0 to 199
Data columns (total 7 columns):
 #   Column       Non-Null Count  Dtype         
---  ------       --------------  -----         
 0   order_id     200 non-null    int64         
 1   order_date   200 non-null    datetime64[us]
 2   customer_id  200 non-null    int64         
 3   category     200 non-null    str           
 4   quantity     200 non-null    int64         
 5   unit_price   190 non-null    float64       
 6   region       195 non-null    str           
dtypes: datetime64[us](1), float64(1), int64(3), str(2)
memory usage: 11.1 KB  
 """

#2. Which columns have missing values, and how many?
orders.isnull().sum()
"""
unit_price (10) and region (5) have missing values
"""

#3. Fill missing unit_price with the median price of that row’s category.
orders['unit_price'] = orders['unit_price'].fillna(orders.groupby('category')['unit_price'].transform('median'))

#4. Add a revenue column (quantity * unit_price).
orders['revenue'] = orders['quantity'] * orders['unit_price']

#5. Total revenue per category, sorted highest to lowest.
total_revenue = orders.groupby('category')['revenue'].sum().sort_values(ascending=False)

#6. Average revenue per order by region. (Watch the missing regions.)
average_revenue_by_region = orders.groupby('region', dropna=True)['revenue'].mean()

#7. Which month had the highest total revenue?
orders['month'] = orders['order_date'].dt.month
total_month_revenue = orders.groupby(orders['month'])['revenue'].sum().idxmax()
"""
May had the highest total revenue
"""

#8. Who are the top 5 customers by total revenue?
top_customers = orders.groupby('customer_id')['revenue'].sum().sort_values(ascending=False).head()
"""
customer_id
19    2851.39
11    2607.28
39    2507.91
4     2469.84
13    2370.16
Name: revenue, dtype: float64
"""

#9. What share of total revenue does each category contribute (as %)?
share_of_revenue_by_category = orders.groupby('category')['revenue'].sum()/orders['revenue'].sum()*100
"""
category
Books          22.773496
Clothing       15.804586
Electronics    27.759733
Home           17.939473
Toys           15.722711
Name: revenue, dtype: float64
"""

#10. Add an order_size column: “small” (<$100), “medium” ($100–$300), “large” (>$300). Count orders per size.
condlist = [
    orders['revenue'] < 100,
    (orders['revenue'] >= 100) & (orders['revenue'] <= 300),
    orders['revenue'] > 300
]
choicelist = [
    'small',
    'medium',
    'large'
]
orders['order_size'] = np.select(condlist, choicelist, default="unknown")
orders['order_size'].value_counts()
"""
large     97
medium    64
small     39
"""

#Bonus: Build a pivot table: months as rows, categories as columns, revenue as values.
orders.pivot_table(columns='category', index='month', values='revenue', aggfunc='sum')
"""
category    Books  Clothing  Electronics      Home      Toys
month                                                       
1         3417.17   939.970      2993.79  2542.230  1229.270
2         2007.19  1558.910      2393.10   428.070  1028.580
3         2913.80  1300.445      3133.38  4977.090  1535.525
4         2161.80  2629.440      3116.15  1149.180   505.610
5         2593.40  2538.050      4899.87  1438.780  3252.950
6         1367.67  1069.000      1090.97   856.105  2431.890
"""
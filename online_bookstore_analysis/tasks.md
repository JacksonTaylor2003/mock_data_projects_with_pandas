# Scenario 3: Page & Pine online bookstore

Run `python make_data.py` (numpy + pandas). It writes `orders.csv`, `books.csv`, `customers.csv`, `targets.csv`.
`price` in orders is the **unit** price paid, in euros. Negative `qty` = a return.

## Tasks
1. Load all four files with sensible dtypes. Remove exact duplicate rows from orders. How many were there?
2. Convert `price` to float. Normalise `channel` to three clean labels.
3. Clean `genre` in books so it uses exactly the five labels in `targets.csv`. Clean `city` too. Prove there are no leftovers.
4. Add a `revenue` column (net of returns). How many return rows? Total net revenue for 2025? Which **book title** has the most return rows?
5. Merge orders with books. Add a column giving each order's share of its customer's total net revenue. (Check for NaNs before you trust it.)
6. Reshape `targets.csv` to long format. Build actual revenue per genre per month and join it to the targets on both keys. Which genre met its target in the most months? Which month had the worst overall attainment (actual / target)?
7. `pivot_table`: net revenue by channel (rows) × genre (columns), with totals.
8. Age at end of 2025. Bands: 18–25, 26–35, 36–50, 51–65, 66+. Average revenue **per customer** in each band (not per order). Then split customers into four equal-size spending groups. How many orders does the average customer in each group place?
9. Per customer, running total of net revenue over time. How many customers ever crossed €100? For those who did, what is the median number of days from first order to crossing?
10. Per customer, rolling mean of revenue over their last 3 orders. Which customer has the highest value of it?
11. Management says the Store channel launched in July 2025. Compare Store's average monthly revenue before and after launch.

## Bonus: cohort retention
Cohort = month of a customer's **first order** (not signup). For each cohort, the share of its customers who order again 1, 2, 3, ... months later. Show it as a cohort × month-offset table. Which cohort has the best month-3 retention?

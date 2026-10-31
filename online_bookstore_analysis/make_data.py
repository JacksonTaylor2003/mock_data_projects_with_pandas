"""Scenario 3: Page & Pine online bookstore. Run once; writes 4 CSVs to the current folder."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)

# ---------- books ----------
genres_clean = ["Fantasy", "Mystery", "Sci-Fi", "Romance", "Nonfiction"]
genre_variants = {
    "Fantasy": ["Fantasy", "fantasy", " FANTASY", "Fantasy "],
    "Mystery": ["Mystery", "mystery ", "MYSTERY"],
    "Sci-Fi": ["Sci-Fi", "sci-fi", "Sci Fi", "SciFi", " sci fi"],
    "Romance": ["Romance", "romance", "ROMANCE "],
    "Nonfiction": ["Nonfiction", "Non-Fiction", "non fiction", "NONFICTION"],
}
n_books = 60
book_genre = rng.choice(genres_clean, n_books)
books = pd.DataFrame({
    "isbn": [f"978-{rng.integers(1000, 9999)}-{i:03d}" for i in range(n_books)],
    "title": [f"Book {i}" for i in range(n_books)],
    "genre": [rng.choice(genre_variants[g]) for g in book_genre],
    "list_price": np.round(rng.uniform(8, 35, n_books), 2),
})

# ---------- customers ----------
n_cust = 400
signup = pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n_cust), unit="D")
cities = ["Helsinki", " helsinki", "HELSINKI", "Espoo", "espoo ", "Tampere", "tampere", "Turku", "Oulu"]
customers = pd.DataFrame({
    "customer_id": [f"C{i:04d}" for i in range(n_cust)],
    "signup_date": signup.strftime("%Y-%m-%d"),
    "birth_year": rng.integers(1950, 2008, n_cust).astype(float),
    "city": rng.choice(cities, n_cust),
})
customers.loc[rng.choice(n_cust, 25, replace=False), "birth_year"] = np.nan

# ---------- orders ----------
rows = []
oid = 100000
for _, c in customers.iterrows():
    sd = pd.Timestamp(c["signup_date"])
    loyalty = rng.uniform(0.2, 0.95)          # chance of ordering again each month
    month = sd
    while month <= pd.Timestamp("2025-12-31"):
        if month == sd or rng.random() < loyalty * 0.6:
            for _ in range(rng.integers(1, 3)):
                ts = month + pd.Timedelta(minutes=int(rng.integers(0, 60 * 24 * 27)))
                if ts > pd.Timestamp("2025-12-31 23:59"):
                    continue
                b = rng.integers(0, n_books)
                rows.append([oid, ts, c["customer_id"], books.isbn[b], int(rng.integers(1, 4)),
                             books.list_price[b], rng.choice(["web", "Web", "APP", "app ", "Store"], p=[.3, .15, .2, .15, .2])])
                oid += 1
        month = month + pd.DateOffset(months=1)
orders = pd.DataFrame(rows, columns=["order_id", "order_ts", "customer_id", "isbn", "qty", "price", "channel"])

# discounts: price stored as messy strings
disc = rng.choice([1.0, 0.9, 0.8], len(orders), p=[.7, .2, .1])
p = np.round(orders.price * disc, 2)
fmt = rng.choice(["{:.2f}", "€{:.2f}", "{:.2f} EUR", "{:.2f}".replace(".", ",")], len(orders))
orders["price"] = [f.format(v) if "," not in f else f"{v:.2f}".replace(".", ",") for f, v in zip(fmt, p)]
orders["order_ts"] = orders.order_ts.dt.strftime("%Y-%m-%d %H:%M")

# returns: a few negative qty rows referencing earlier orders
ret_idx = rng.choice(len(orders), 40, replace=False)
returns = orders.iloc[ret_idx].copy()
returns["order_id"] = np.arange(oid, oid + 40)
returns["qty"] = -returns["qty"]
orders = pd.concat([orders, returns, orders.sample(15, random_state=1)]).sample(frac=1, random_state=2).reset_index(drop=True)

# ---------- monthly genre revenue targets (wide) ----------
months = pd.period_range("2025-01", "2025-12", freq="M").strftime("%b").tolist()
targets = pd.DataFrame({"genre": genres_clean})
for m in months:
    targets[m] = (rng.integers(8, 30, len(genres_clean)) * 100)

books.to_csv("books.csv", index=False)
customers.to_csv("customers.csv", index=False)
orders.to_csv("orders.csv", index=False)
targets.to_csv("targets.csv", index=False)
print("wrote books.csv, customers.csv, orders.csv, targets.csv")

import numpy as np
import pandas as pd

#Step 1. Loading the files
books = pd.read_csv("online_bookstore_analysis/data_files/books.csv",
                    dtype = {
                        'isbn': str,
                        'title': str,
                        'genre': str,
                        'list_price': float
                    })
customers = pd.read_csv("online_bookstore_analysis/data_files/customers.csv",
                    dtype = {
                        'customer_id': str,
                        'signup_date': str,
                        'birth_year': str,
                        'city': str
                    }, parse_dates=['signup_date', 'birth_year'])


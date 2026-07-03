import pandas as pd
import numpy as np

# 1. Load ALL required data files (Naye files ke sath)
orders = pd.read_csv(r'd:\Project\Ecommerce Logistic\olist_orders_dataset.csv')
items = pd.read_csv(r'd:\Project\Ecommerce Logistic\olist_order_items_dataset.csv')
products = pd.read_csv(r'd:\Project\Ecommerce Logistic\olist_products_dataset.csv')
customers = pd.read_csv(r'd:\Project\Ecommerce Logistic\olist_customers_dataset.csv') # Added for customer_state
sellers = pd.read_csv(r'd:\Project\Ecommerce Logistic\olist_sellers_dataset.csv')     # Added for seller_state

print("All Olist Tables Loaded Successfully!")

# 2. Convert text dates to proper Datetime formats
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

# 3. Calculate Operational Metrics
orders['actual_delivery_days'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days
orders['delay_days'] = (orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']).dt.days
orders['delay_days'] = orders['delay_days'].apply(lambda x: x if x > 0 else 0)

# 4. Master Merge (Tying everything together into one big matrix)
master_df = pd.merge(items, orders, on='order_id', how='inner')
master_df = pd.merge(master_df, products, on='product_id', how='left')
master_df = pd.merge(master_df, customers, on='customer_id', how='left') # Adds customer_state column
master_df = pd.merge(master_df, sellers, on='seller_id', how='left')     # Adds seller_state column

# Clean rows where delivery dates are missing
master_df.dropna(subset=['actual_delivery_days'], inplace=True)

# 5. Export clean dataset for Power BI
master_df.to_csv(r'd:\Project\Ecommerce Logistic\olist_supply_chain_clean.csv', index=False)
print("Updated Master Supply Chain File Ready with Regional States!")
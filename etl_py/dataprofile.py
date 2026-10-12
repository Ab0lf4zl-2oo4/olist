import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from pathlib import Path


df_customers=pd.read_csv('brazilian/olist_customers_dataset.csv')
df_order_item=pd.read_csv('brazilian/olist_order_items_dataset.csv')
df_payments=pd.read_csv('brazilian/olist_order_payments_dataset.csv')
df_reviews=pd.read_csv('brazilian/olist_order_reviews_dataset.csv')
df_orders=pd.read_csv('brazilian/olist_orders_dataset.csv')
df_products=pd.read_csv('brazilian/olist_products_dataset.csv')
df_sellers=pd.read_csv('brazilian/olist_sellers_dataset.csv')
df_category=pd.read_csv('brazilian/product_category_name_translation.csv')


print(df_category.describe())
print(df_customers.describe())
print(df_order_item.describe())
print(df_orders.describe())
print(df_payments.describe())
print(df_products.describe())
print(df_reviews.describe())
print(df_sellers.describe())


print(df_category.columns)
print(df_customers.columns)
print(df_order_item.columns)
print(df_orders.columns)
print(df_payments.columns)
print(df_products.columns)
print(df_reviews.columns)
print(df_sellers.columns)



print(df_category.shape)
print(df_customers.shape)
print(df_order_item.shape)
print(df_orders.shape)
print(df_payments.shape)
print(df_products.shape)
print(df_reviews.shape)
print(df_sellers.shape)

#customers_orders
print(df_customers["customer_id"].nunique())
print(df_orders["customer_id"].nunique())
#orders_orderitem
print(df_orders["order_id"].nunique())
print(df_order_item["order_id"].nunique())
#products_orderitem
print(df_products["product_id"].nunique())
print(df_order_item["product_id"].nunique())



orders_without_items = df_orders[
    ~df_orders["order_id"].isin(df_order_item["order_id"])
]

print(orders_without_items["order_status"].value_counts())
#seller_oi
print(df_sellers["seller_id"].nunique())
print(df_order_item["seller_id"].nunique())

print(df_order_item["seller_id"].value_counts().head(10))

#payments_orders
print(df_payments["order_id"].nunique())
print(df_orders["order_id"].nunique())

orders_without_payment = df_orders[
    ~df_orders["order_id"].isin(df_payments["order_id"])
]

print(orders_without_payment["order_status"].value_counts())

#revews_orders
print(df_reviews["order_id"].nunique())
print(df_orders["order_id"].nunique())


# data quality

print(df_reviews.isnull().sum())
print(df_products.isnull().sum())
print(df_category.isnull().sum())
print(df_sellers.isnull().sum())
print(df_order_item.isnull().sum())
print(df_orders.isnull().sum())
print(df_payments.isnull().sum())



print(
    df_orders.groupby("order_status")[
        [
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date"
        ]
    ].apply(lambda x: x.isnull().sum())
)

for file, key in [
    ("olist_customers_dataset.csv", "customer_id"),
    ("olist_products_dataset.csv", "product_id"),
    ("olist_sellers_dataset.csv", "seller_id")
]:
    df = pd.read_csv("brazilian/" + file)
    print(file)
    print("Rows:", len(df))
    print("Unique:", df[key].nunique())
    print()

print("false price and freght value:")
print(df_order_item[df_order_item["price"]<0])
print(df_order_item[df_order_item["freight_value"]<0])
print("true price and freit value:")
print(df_order_item[df_order_item["price"]>0])
print(df_order_item[df_order_item["freight_value"]>0])


print("false payment")
print(df_payments[df_payments["payment_value"]<0])



print("false revews")
print(df_reviews[df_reviews['review_score']<1])
print(df_reviews[df_reviews['review_score']>5])






# -----------------------------
# 1. Database configuration
# -----------------------------

SERVER = r"DESKTOP-JKUS70M"
DATABASE = "ecommerce_dw"

CONNECTION_STRING = (
    f"mssql+pyodbc://@{SERVER}/{DATABASE}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)


# -----------------------------
# 2. Create database engine
# -----------------------------

def create_db_engine():
    return create_engine(
        CONNECTION_STRING,
        fast_executemany=True
    )


# -----------------------------
# 3. Load CSV into SQL Server
# -----------------------------

def load_csv_to_sql(csv_path, table_name):
    csv_path = Path(csv_path)

    if not csv_path.exists():
        print(f"ERROR: CSV file not found: {csv_path}")
        return

    engine = create_db_engine()

    try:
        print(f"\nReading: {csv_path}")

        df = pd.read_csv(csv_path)

        print(f"Rows found: {len(df):,}")
        print(f"Loading into staging.{table_name} ...")

        df.to_sql(
            name=table_name,
            con=engine,
            schema="staging",
            if_exists="append",
            index=False,
            chunksize=1000
        )

        print(
            f"SUCCESS: staging.{table_name} "
            f"loaded with {len(df):,} rows."
        )

    except Exception as error:
        print(f"ERROR loading {table_name}:")
        print(error)

    finally:
        engine.dispose()


# -----------------------------
# 4. CSV file paths
# -----------------------------

DATA_DIR = Path("brazilian")

files_to_load = {
    "customers": DATA_DIR / "olist_customers_dataset.csv",
    "order_items": DATA_DIR / "olist_order_items_dataset.csv",
    "payments": DATA_DIR / "olist_order_payments_dataset.csv",
    "reviews": DATA_DIR / "olist_order_reviews_dataset.csv",
    "products": DATA_DIR / "olist_products_dataset.csv",
    "sellers": DATA_DIR / "olist_sellers_dataset.csv",
    "category": DATA_DIR / "product_category_name_translation.csv",
}


# -----------------------------
# 5. Load all remaining tables
# -----------------------------

if __name__ == "__main__":
    for table_name, csv_path in files_to_load.items():
        load_csv_to_sql(csv_path, table_name)

    print("\nCSV loading process finished.")



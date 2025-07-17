import requests
import pandas as pd

# Step 1: Fetch product data
url = "https://fakestoreapi.com/products"
response = requests.get(url)
products = response.json()
df = pd.DataFrame(products)

# Step 2: Create categories.csv
categories = df["category"].drop_duplicates().reset_index(drop=True).to_frame(name="category_name")
categories.to_csv("categories.csv", index=False)

# Step 3: Create products.csv
# Temporarily assign numeric category_id to match with categories.csv
categories["category_id"] = categories.index + 1
df = df.merge(categories, on="category", how="left")

products_df = df[["id", "title", "price", "description", "category_id", "image"]].copy()
products_df.columns = ["product_id", "title", "price", "description", "category_id", "image"]
products_df.to_csv("products.csv", index=False)

# Step 4: Create product_reviews.csv
df["rating_value"] = df["rating"].apply(lambda x: x["rate"])
df["rating_count"] = df["rating"].apply(lambda x: x["count"])
reviews_df = df[["id", "rating_value", "rating_count"]].copy()
reviews_df.columns = ["product_id", "rating", "count"]
reviews_df.to_csv("product_reviews.csv", index=False)

print("Data downloaded and saved to CSV files.")

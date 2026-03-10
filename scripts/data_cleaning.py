import pandas as pd

print("Reading dataset...")

df = pd.read_csv("data/raw/Uber_Eats_data.csv")

print("Original rows:", len(df))

# -----------------------------
# 1️⃣ Remove Duplicate Rows
# -----------------------------
df = df.drop_duplicates()
print("Rows after removing duplicates:", len(df))

# -----------------------------
# 2️⃣ Handle Missing Values
# -----------------------------
df = df.dropna(subset=["name", "location", "cuisines"])

# -----------------------------
# 3️⃣ Rating Normalization
# -----------------------------
# Clean the strings first
df["rate"] = df["rate"].astype(str).str.replace("/5", "", regex=False)
# Convert to numeric (Non-numeric like 'NEW' becomes NaN)
df["rate"] = pd.to_numeric(df["rate"], errors="coerce")
# NOW calculate mean and fill
df["rate"] = df["rate"].fillna(df["rate"].mean())

# -----------------------------
# 4️⃣ Cost Standardization
# -----------------------------
df["approx_cost(for two people)"] = (
    df["approx_cost(for two people)"]
    .astype(str)
    .str.replace(",", "", regex=False)
)
# Use the correct original name here
df["approx_cost(for two people)"] = pd.to_numeric(df["approx_cost(for two people)"], errors="coerce").fillna(0)


# -----------------------------
# 5️⃣ Feature Engineering
# -----------------------------

# Pricing Segments
def price_category(cost):
    if cost <= 500:
        return "Low"
    elif cost <= 1000:
        return "Mid"
    else:
        return "Premium"

df["price_segment"] = df["approx_cost(for two people)"].apply(price_category)

# Rating Categories
def rating_category(rate):
    if rate < 3:
        return "Low Rating"
    elif rate < 4:
        return "Average"
    else:
        return "High Rating"

df["rating_category"] = df["rate"].apply(rating_category)



# -----------------------------
# 5️⃣ Mapping & Renaming
# -----------------------------
column_mapping = {
    "name": "restaurant_name",
    "location": "location",
    "cuisines": "cuisines",
    "rate": "rate",
    "approx_cost(for two people)": "approx_cost_for_two",
    "online_order": "online_order",
    "book_table": "book_table",
    "price_segment": "price_segment",  
    "rating_category": "rating_category" 
}

df.rename(columns=column_mapping, inplace=True)

# Important: If you want to save the new "Segments" to the DB, 
# you must add them to this list and your SQL table!
final_columns = list(column_mapping.values()) # + ["price_segment", "rating_category"]
df = df[final_columns]

df = df.dropna(subset=["rate", "approx_cost_for_two"])

# -----------------------------
# Save Cleaned Dataset
# -----------------------------
df.to_csv("data/processed/db_cleaned_restaurants.csv", index=False)

print("Cleaned file saved successfully!")
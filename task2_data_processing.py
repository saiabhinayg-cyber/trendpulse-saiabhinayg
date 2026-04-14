import json
import pandas as pd
import os

def stars():
    print("*"*57)

# STEP 1: Load JSON File from data folder, converting to data frames with pandas and printing how many rows were loaded.

file_path = "data/trends_20260414.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)
print(f"\nLoaded {len(df)} stories from {file_path}\n")

# STEP 2: Clean the Data by removing the duplicates based on post_id and rows with missing data. printing no of rows remaining after cleaning

df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Convert data types and Remove low quality posts
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}\n")

# Remove extra whitespace in title column
df["title"] = df["title"].str.strip() 

# STEP 3: Save as CSV and printing a quick summary of how many stories per category

output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

stars()
print(f"\nSaved {len(df)} rows to {output_file}\n")
stars()
print("\nStories per category:")
print("__"*20)
print(df["category"].value_counts())
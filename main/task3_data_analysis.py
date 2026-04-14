import pandas as pd
import numpy as np

# STEP 1: Loading the data from csv file and convert them to panda data frames for analysing the data 

cleaned_data = "main/data/trends_clean.csv"
df = pd.read_csv(cleaned_data)

#Print the shape of the DataFrame (rows and columns)
print(f"\nLoaded data: {df.shape}")
print("-"*12)

#Print the first 5 rows
print("\nFirst 5 rows:")
print("-"*13)
print(df.head())

# Print the average score and average num_comments across all stories
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()
print(f"\nAverage score   : {avg_score:.2f}")
print(f"Average comments: {avg_comments:.2f}")

# STEP 2: Basic Analysis with NumPy

scores = df["score"].values
comments = df["num_comments"].values
print("\n--- NumPy Stats ---")

# Mean, median, and standard deviation of score
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")

# highest score and lowest score
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}")

# Finging which category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()
print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Finding the Story with most comments
max_comments_index = np.argmax(comments)
top_story = df.iloc[max_comments_index]
print(f"\nMost commented story:")
print(f"\"{top_story['title']}\" — {top_story['num_comments']} comments")

# STEP 3: Add New Columns engagement and is_popular

df["engagement"] = df["num_comments"] / (df["score"] + 1)
df["is_popular"] = df["score"] > avg_score

# STEP 4: Save the result to CSV

analysed_data = "main/data/trends_analysed.csv"
df.to_csv(analysed_data, index=False)
print(f"\nSaved to {analysed_data}")
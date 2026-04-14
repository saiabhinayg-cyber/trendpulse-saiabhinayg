import pandas as pd
import matplotlib.pyplot as plt
import os

# STEP 1: Load Data + Setup
# -----------------------------
analysed_data = "main/data/trends_analysed.csv"
df = pd.read_csv(analysed_data)

# Create outputs folder if not exists
if not os.path.exists("main/outputs"):
    os.makedirs("main/outputs")

# STEP 2: Chart 1- Top 10 Stories by Score

top10 = df.sort_values(by="score", ascending=False).head(10)

# Shorten titles to 50 characters
top10["short_title"] = top10["title"].apply(
    lambda x: x[:50] + "..." if len(x) > 50 else x
)

plt.figure()
plt.barh(top10["short_title"], top10["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()

#using plt.savefig() for saving the chart as img
plt.savefig("main/outputs/chart1_top_stories.png")
plt.close()

# STEP 3: Chart 2 — Stories per Category

category_counts = df["category"].value_counts()

plt.figure()
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

#using plt.savefig() for saving the chart as img
plt.savefig("main/outputs/chart2_categories.png")
plt.close()

# STEP 4: Chart 3 — Scatter Plot

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure()
plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

#using plt.savefig() for saving the chart as img
plt.savefig("main/outputs/chart3_scatter.png")
plt.close()

# BONUS: Dashboard

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1
axes[0].barh(top10["short_title"], top10["score"])
axes[0].set_title("Top 10 Stories")
axes[0].set_xlabel("Score")
axes[0].invert_yaxis()

# Chart 2
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Count")

# Chart 3
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].legend()

# Overall title
plt.suptitle("TrendPulse Dashboard")
plt.savefig("main/outputs/dashboard.png")
plt.close()
print("\nAll charts saved in 'outputs/' folder")
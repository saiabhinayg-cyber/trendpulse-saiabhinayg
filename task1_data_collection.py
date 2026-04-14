import json
import requests
import time
import os
import datetime


headers = {"User-Agent": "TrendPulse/1.0"} # headers according to the task
topstories_url = "https://hacker-news.firebaseio.com/v0/topstories.json" #url for top stories

# ketworks for categories
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}



# checks the title and returns the category based on keyword matching.

def get_category(title):
    title = title.lower()  # make lowercase for matching
    for category, keywords in categories.items():
        for word in keywords:
            if word in title:
                return category

    return None  # if no match found

# feaching the data

def fetch_data():
    try:
        ids = requests.get(topstories_url, headers=headers).json()[:500]
    except Exception as e:
        print("Error fetching top stories:", e)
        return []

    final_data = []
    category_count = {cat: 0 for cat in categories}

    # Loop for category-wise
    for cat in categories:
        print(f"Processing {cat}...")

        for story_id in ids:

            if category_count[cat] >= 25:
                break

            try:
                res = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                    headers=headers
                )
                data = res.json()

                if not data or "title" not in data:
                    continue

                assigned = get_category(data["title"])

                # Only collect for current category
                if assigned != cat:
                    continue

                story_data = {
                    "post_id": data.get("id"),
                    "title": data.get("title"),
                    "category": assigned,
                    "score": data.get("score", 0),
                    "num_comments": data.get("descendants", 0),
                    "author": data.get("by"),
                    "collected_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                final_data.append(story_data)
                category_count[cat] += 1

            except Exception as e:
                print(f"Error fetching {story_id}: {e}")

        # Sleep AFTER each category
        time.sleep(2)

    return final_data


data = fetch_data()
# Create folder if not exists
if not os.path.exists("data"):
    os.makedirs("data")

file_name = f"data/trends_{datetime.datetime.now().strftime('%Y%m%d')}.json"

with open(file_name, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print(f"Collected {len(data)} stories.Saved to {file_name}")

import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

# --------------------------
# 1️⃣ Read Reddit JSONL data
# --------------------------
REDDIT_FILE = r"D:\pushshift\endsars_oct2020.jsonl"  # Use raw string for Windows paths

reddit_dates = []

with open(REDDIT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        post = json.loads(line)
        # Convert Unix timestamp to date
        created = datetime.utcfromtimestamp(post.get("created_utc"))
        reddit_dates.append(created.date())

# Count posts per day
reddit_counts = Counter(reddit_dates)
reddit_df = pd.DataFrame(
    sorted(reddit_counts.items()), columns=["date", "reddit_posts"]
)

# --------------------------
# 2️⃣ Read News CSV data
# --------------------------
NEWS_FILE = r"D:\Documents\news_crawler\vanguard_2020_10_endsars.csv"  # replace with your CSV path
news_df = pd.read_csv(NEWS_FILE, header=0)

# Convert date column to datetime
# Specify the exact format
news_df['date'] = pd.to_datetime(
    news_df['date'],
    format="%d-%b-%y",  # Day-Month(abbr)-Year(two digits)
    errors='coerce'
).dt.date

news_df = news_df.dropna(subset=['date'])

# Count posts per day
news_counts = news_df['date'].value_counts().sort_index()
news_df_count = pd.DataFrame({
    "date": news_counts.index,
    "news_posts": news_counts.values
})

# --------------------------
# 3️⃣ Merge DataFrames
# --------------------------
merged_df = pd.merge(reddit_df, news_df_count, on='date', how='outer').fillna(0)
merged_df = merged_df.sort_values("date")

# --------------------------
# 4️⃣ Plot
# --------------------------
plt.figure(figsize=(12,6))
plt.plot(merged_df['date'], merged_df['reddit_posts'], marker='o', label='Reddit')
plt.plot(merged_df['date'], merged_df['news_posts'], marker='x', label='News Sites')
plt.xlabel("Date")
plt.ylabel("Number of Posts")
plt.title("EndSARS Coverage: Reddit vs News Sites (October 2020)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

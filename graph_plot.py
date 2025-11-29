import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Path to your JSONL file
INPUT_FILE = r"D:\pushshift\endsars_oct2020_500.jsonl"

# List to store the post timestamps
timestamps = []

# Read JSONL file line by line
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        # Extract the 'created_utc' field
        if "created_utc" in data:
            timestamps.append(data["created_utc"])

# Convert Unix timestamps to datetime objects
dates = [datetime.utcfromtimestamp(ts).date() for ts in timestamps]

# Create a DataFrame
df = pd.DataFrame({"date": dates})

# Filter for October 2020
df = df[(df["date"] >= datetime(2020, 10, 1).date()) & 
        (df["date"] <= datetime(2020, 10, 31).date())]

# Count posts per day
counts = df.groupby("date").size().reset_index(name="num_posts")

# Plot
plt.figure(figsize=(12,6))
plt.plot(counts["date"], counts["num_posts"], marker="o")
plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("Number of Posts")
plt.title("EndSARS-related Reddit Posts per Day in October 2020")
plt.grid(True)
plt.tight_layout()
plt.show()

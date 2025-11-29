import json
import time

INPUT_FILE = r"D:\pushshift\RS_2020-10"
OUTPUT_FILE = r"D:\pushshift\endsars_oct2020.jsonl"

# Keywords to search
KEYWORDS = ["endsars", "end sars", "#endsars"]

# Time range: 8 Oct 2020 → 31 Oct 2020 (inclusive)
OCT_8_2020_UTC = 1602115200    # 2020-10-08 00:00 UTC
NOV_1_2020_UTC = 1604188800    # 2020-11-01 00:00 UTC (exclusive)

count = 0
line_number = 0

print("Starting extraction...")
print(f"Reading large file: {INPUT_FILE}")

start_time = time.time()

with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as infile, \
     open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:

    for line in infile:
        line_number += 1

        # Show progress every 100k lines
        if line_number % 100000 == 0:
            elapsed = time.time() - start_time
            print(f"[INFO] Processed {line_number:,} lines "
                  f"({elapsed:.1f}s elapsed), matched {count} so far.")

        # Quick keyword check first (fast)
        low = line.lower()
        if not any(k in low for k in KEYWORDS):
            continue

        # Parse JSON safely
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue

        created = data.get("created_utc")
        if not isinstance(created, int):
            continue

        # Filter by date range
        if not (OCT_8_2020_UTC <= created < NOV_1_2020_UTC):
            continue

        # Write matching post
        outfile.write(line)
        count += 1

        print(f"[MATCH] #{count}: created_utc={created}")

elapsed = time.time() - start_time
print("\nExtraction complete!")
print(f"Total matched posts: {count}")
print(f"Took {elapsed:.1f} seconds.")
print(f"Saved output to: {OUTPUT_FILE}")

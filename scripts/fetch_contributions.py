import json
import os
import re
import sys
import requests
from bs4 import BeautifulSoup

USERNAME = "ravin972"


def fetch_contributions(username: str = USERNAME):
    url = f"https://github.com/users/ravin972/contributions"
    headers = {"User-Agent": "Mozilla/5.0 (GitHub-Profile-Sync)"}
    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code != 200:
        print(
            f"Error: Received HTTP {resp.status_code} fetching contributions."
        )
        sys.exit(1)

    soup = BeautifulSoup(resp.text, "html.parser")
    cells = soup.find_all(
        ["td", "rect"], class_=re.compile(r"ContributionCalendar-day")
    )

    days = []
    total_count = 0

    for cell in cells:
        date = cell.get("data-date")
        level = int(cell.get("data-level", 0))
        if not date:
            continue

        text = cell.get_text() or cell.get("aria-label", "")
        count_match = re.search(r"(\d+)\s+contribution", text)
        count = int(count_match.group(1)) if count_match else level

        total_count += count
        days.append({"date": date, "count": count, "level": level})

    days.sort(key=lambda d: d["date"])

    current_streak = 0
    for day in reversed(days):
        if day["count"] > 0:
            current_streak += 1
        elif current_streak > 0:
            break

    data = {
        "username": username,
        "total_year": total_count,
        "current_streak": current_streak,
        "days": days,
    }

    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(
        f"✓ Scraped {len(days)} days ({total_count} total commits, {current_streak}-day streak) -> 'data/contributions.json'"
    )


if __name__ == "__main__":
    fetch_contributions()
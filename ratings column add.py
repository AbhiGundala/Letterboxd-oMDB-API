

df = pd.read_csv("Complete final.csv")
print(df.head())  # This confirms it's loaded
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Load your CSV file
df = pd.read_csv("Complete final.csv")
print(df.head())  # Confirm it's loaded

# Convert title to slug for URL
def title_to_slug(title):
    slug = title.lower().strip()
    slug = slug.replace("’", "").replace("'", "").replace(",", "").replace(":", "").replace(".", "")
    slug = slug.replace("&", "and")
    slug = '-'.join(slug.split())
    return slug

# Get average rating from Letterboxd
def get_letterboxd_rating(slug):
    url = f"https://letterboxd.com/film/{slug}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        meta = soup.find("meta", {"name": "twitter:data2"})
        if meta and "★" in meta["content"]:
            rating = float(meta["content"].split(" ")[0])
            print(f"{slug}: {rating}")
            return rating
    except Exception as e:
        print(f"Error with {slug}: {e}")
    return None

# Generate slugs
df['Slug'] = df['Title'].apply(title_to_slug)

# Scrape average ratings
df['Average Rating'] = df['Slug'].apply(get_letterboxd_rating)

# Save final CSV
df.to_csv("Letterboxd_Average_Ratings.csv", index=False)
print("✅ Done! Ratings saved to 'Letterboxd_Average_Ratings.csv'")



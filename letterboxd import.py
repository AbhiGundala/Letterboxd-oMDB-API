import pandas as pd
import requests
import time
from fuzzywuzzy import fuzz

API_KEY = "your_api_key_here"  # Replace with your OMDb API key
BASE_URL = "http://www.omdbapi.com/"
CONFIDENCE_THRESHOLD = 80  # Set your own fuzzy match confidence level

# Read titles from your CSV
df = pd.read_csv("missing_letterboxd_titles_cased.csv")
corrected_titles = []
years = []
confidence_scores = []

for idx, original_title in enumerate(df["Title"], start=1):
    params = {"apikey": API_KEY, "t": original_title}
    try:
        resp = requests.get(BASE_URL, params=params, timeout=5)
        data = resp.json()

        if data.get("Response") == "True":
            api_title = data.get("Title")
            api_year = data.get("Year")

            # Compute fuzzy similarity
            confidence = fuzz.token_set_ratio(original_title.lower(), api_title.lower())

            if confidence >= CONFIDENCE_THRESHOLD:
                corrected_titles.append(api_title)
                years.append(api_year)
                confidence_scores.append(confidence)
            else:
                corrected_titles.append(None)
                years.append(None)
                confidence_scores.append(confidence)
                print(f"[LOW CONFIDENCE] {original_title} → {api_title} ({confidence}%)")

        else:
            corrected_titles.append(None)
            years.append(None)
            confidence_scores.append(0)
            print(f"[NOT FOUND] {original_title}")

    except Exception as e:
        print(f"[ERROR] {original_title} – {e}")
        corrected_titles.append(None)
        years.append(None)
        confidence_scores.append(0)

    print(f"{idx}/{len(df)} processed")
    time.sleep(0.2)  # To avoid rate limiting

# Add results to the dataframe
df["Corrected Title"] = corrected_titles
df["Year"] = years
df["Match Confidence"] = confidence_scores

# Save to new CSV
df.to_csv("letterboxd_corrected_with_years.csv", index=False, encoding="utf-8")
print("Done! Saved to letterboxd_corrected_with_years.csv")


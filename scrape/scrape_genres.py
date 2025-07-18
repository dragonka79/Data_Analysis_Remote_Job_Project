import requests
import pandas as pd
import scrape_basic

# === Get Genres ===

genre_url = f"{scrape_basic.BASE_URL}/genre/movie/list?language={scrape_basic.LANG}&api_key={scrape_basic.API_KEY}"
genres = requests.get(genre_url).json()["genres"]
genre_df = pd.DataFrame(genres)
genre_df.to_csv(f"{scrape_basic.output_folder}/genres.csv", index=False)

print("✅ Data saved to:", scrape_basic.output_folder)

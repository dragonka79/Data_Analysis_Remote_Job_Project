import requests
import pandas as pd
from tqdm import tqdm
import os

# === CONFIG ===
API_KEY = "0c4b5ab9d640aca7af65ca66721a4a65"  # Insert your TMDB API key
BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
LANG = "en-US"
NUM_PAGES = 5  # 5 pages × 20 movies = 100 movies

output_folder = "tmdb_data"
os.makedirs(output_folder, exist_ok=True)

# === 1. Get Genres ===
genre_url = f"{BASE_URL}/genre/movie/list?language={LANG}&api_key={API_KEY}"
genres = requests.get(genre_url).json()["genres"]
genre_df = pd.DataFrame(genres)
genre_df.to_csv(f"{output_folder}/genres.csv", index=False)

# === 2. Get Popular Movies ===
movies = []
for page in tqdm(range(1, NUM_PAGES + 1), desc="Fetching movies"):
    url = f"{BASE_URL}/movie/popular?language={LANG}&page={page}&api_key={API_KEY}"
    res = requests.get(url).json()
    for movie in res["results"]:
        movies.append({
            "movie_id": movie["id"],
            "title": movie["title"],
            "release_date": movie["release_date"],
            "vote_average": movie["vote_average"],
            "vote_count": movie["vote_count"],
            "genre_ids": movie["genre_ids"],
            "overview": movie["overview"],
            "popularity": movie["popularity"],
            "original_language": movie["original_language"]
        })

movie_df = pd.DataFrame(movies)
movie_df.to_csv(f"{output_folder}/movies.csv", index=False)

# === 3. Get Cast (top 3) for each movie ===
cast_records = []
for movie in tqdm(movies, desc="Fetching cast"):
    cast_url = f"{BASE_URL}/movie/{movie['movie_id']}/credits?api_key={API_KEY}"
    res = requests.get(cast_url).json()

    for person in res.get("cast", [])[:3]:  # Top 3 billed
        cast_records.append({
            "movie_id": movie["movie_id"],
            "actor_id": person["id"],
            "actor_name": person["name"],
            "character": person["character"],
            "order": person["order"]
        })

cast_df = pd.DataFrame(cast_records)
cast_df.to_csv(f"{output_folder}/cast.csv", index=False)

print("✅ Data saved to:", output_folder)


import os

API_KEY = ""  # Insert your TMDB API key
BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
LANG = "en-US"

output_folder = "data"
os.makedirs(output_folder, exist_ok=True)



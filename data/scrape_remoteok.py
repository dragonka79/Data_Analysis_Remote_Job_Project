import requests
import pandas as pd

# API endpoint
url = "https://remoteok.com/api"

# Get the JSON response
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

# Parse response
data = response.json()

# First element is metadata, skip it
job_data = data[1:]

# Convert to DataFrame
df = pd.DataFrame(job_data)

# Preview relevant columns
df = df[["id", "company", "position", "location", "tags", "salary_min", "salary_max", "url", "date"]]

# Clean column names
df.columns = [col.lower() for col in df.columns]

# Convert tags list to string
df["tags"] = df["tags"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

# Save to CSV for backup
df.to_csv("remoteok_jobs.csv", index=False)

print(f"Scraped {len(df)} jobs from RemoteOK.")

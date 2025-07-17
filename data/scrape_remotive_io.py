import requests
import pandas as pd

# API endpoint
url = "https://remotive.io/api/remote-jobs"

# Optional: filter by category, e.g. 'software-dev', 'marketing', etc.
params = {
    "category": "software-dev"  # you can remove this line for all categories
}

# Send GET request
response = requests.get(url, params=params)

# Check if request was successful
if response.status_code != 200:
    print("Failed to fetch data from Remotive API")
    exit()

# Parse JSON response
data = response.json()

# Extract job list
jobs = data.get("jobs", [])

# Create DataFrame
df = pd.DataFrame(jobs)

# Optional: select and rename relevant columns
columns_of_interest = [
    "id", "title", "company_name", "category", "job_type", "candidate_required_location",
    "salary", "url", "publication_date", "tags"
]

# Add missing columns as NaN if needed
for col in columns_of_interest:
    if col not in df.columns:
        df[col] = pd.NA

df = df[columns_of_interest]

# Convert tags list to comma-separated string
df["tags"] = df["tags"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

# Save to CSV
csv_filename = "remotive_jobs.csv"
df.to_csv(csv_filename, index=False)

print(f"Scraped {len(df)} jobs from Remotive.io and saved to '{csv_filename}'.")

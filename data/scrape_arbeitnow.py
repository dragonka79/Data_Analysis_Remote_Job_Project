import requests
import pandas as pd

# Base API endpoint
base_url = "https://www.arbeitnow.com/api/job-board-api"

# Container for all jobs
all_jobs = []

# Fetch multiple pages (set max_pages to what you need)
max_pages = 3

for page in range(1, max_pages + 1):
    response = requests.get(f"{base_url}?page={page}")
    
    if response.status_code != 200:
        print(f"Failed to fetch page {page}. Status code: {response.status_code}")
        break

    data = response.json()
    
    jobs = data.get("data", [])
    if not jobs:
        print(f"No jobs found on page {page}. Ending pagination.")
        break

    all_jobs.extend(jobs)
    print(f"Page {page}: {len(jobs)} jobs added.")

# Convert to DataFrame
df = pd.DataFrame(all_jobs)

# Select and rename useful columns
columns_of_interest = [
    "slug", "company_name", "title", "location", "remote", "url", "created_at", "tags", "job_types", "salary"
]

# Add missing columns as NaN (just in case)
for col in columns_of_interest:
    if col not in df.columns:
        df[col] = pd.NA

df = df[columns_of_interest]

# Convert list fields to comma-separated strings
for col in ["tags", "job_types"]:
    df[col] = df[col].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

# Save to CSV
csv_filename = "./Data_Analysis_Remote_Job_Project/data/arbeitnow_jobs.csv"
df.to_csv(csv_filename, index=False)

print(f"✅ Scraped {len(df)} jobs from Arbeitnow and saved to '{csv_filename}'.")

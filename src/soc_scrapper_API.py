import os
import pandas as pd
import re
import time
import serpapi
import json
from datetime import datetime


def serpapi_google_jobs_search(query, location="United States", max_pages=50):
    """
    Fetch multiple pages of Google Jobs results using SerpApi with proper token-based pagination.
    
    Args:
        query (str): Job search query.
        location (str): Job location.
        max_pages (int): Maximum number of pages to fetch.
    
    Returns:
        List of jobs (dicts)
    """
    all_jobs = []

    # Check if API key is available
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        print("Error: SERPAPI_KEY environment variable is not set.")
        return all_jobs

    # Initial search parameters
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "hl": "en",
        "api_key": api_key
    }

    next_page_token = None
    current_page = 0

    print(f"\n--- Starting search for query: '{query}' ---")
    while current_page < max_pages:
        try:
            # Add next_page_token if available
            if next_page_token:
                params["next_page_token"] = next_page_token

            search = serpapi.GoogleSearch(params)
            results = search.get_dict()

            # Check for errors in API response
            if "error" in results:
                print(f"API Error: {results['error']}")
                break

            jobs_results = results.get("jobs_results", [])

            if not jobs_results:
                print(f"No more results found on page {current_page + 1}. Stopping.")
                break

            all_jobs.extend(jobs_results)
            print(f"Page {current_page + 1}: Retrieved {len(jobs_results)} jobs")

            # Check for next page token
            next_page_token = results.get("serpapi_pagination", {}).get("next_page_token")
            if not next_page_token:
                print("No more pages available.")
                break

            time.sleep(1)  # Polite delay between requests
            current_page += 1

        except Exception as e:
            print(f"Error fetching page {current_page + 1}: {e}")
            break

    return all_jobs


def extract_responsibilities(description_text):
    """
    Extract the 'Responsibilities' section from a job description with improved pattern matching.
    """
    if not description_text or not isinstance(description_text, str):
        return ""

    # Look for responsibilities section with various patterns
    # This list can be expanded with more variations as you find them.
    patterns = [
        r"responsibilities[:\s]*(.*?)(?=qualifications|requirements|skills|education|experience|benefits|about you|$)",
        r"what you'll do[:\s]*(.*?)(?=what you'll need|qualifications|requirements|skills|education|experience|benefits|$)",
        r"key responsibilities[:\s]*(.*?)(?=qualifications|requirements|skills|education|experience|benefits|$)",
        r"your role[:\s]*(.*?)(?=qualifications|requirements|skills|education|experience|benefits|$)",
    ]

    responsibilities = ""
    for pattern in patterns:
        # Use original text to preserve casing, but search case-insensitively
        match = re.search(pattern, description_text, re.IGNORECASE | re.DOTALL)
        if match:
            responsibilities = match.group(1).strip()
            break

    # Clean up the extracted text
    if responsibilities:
        # Remove extra spaces
        responsibilities = re.sub(r'[\n\r\t]+', '\n', responsibilities).strip()

    return responsibilities.strip()


def main():
    # --- Configuration ---
    # Use multiple queries to capture more variations of the job title
    search_queries = [
        "SOC Analyst Tier 1",
        "Security Operations Center Analyst Tier 1",
        "Junior SOC Analyst",
        "Cyber Defense Analyst Tier 1",
        "Intrusion Analyst"
    ]
    location = "United States"
    max_pages = 50
    all_jobs_raw = []

    print("Starting job scraping via SerpApi...")
    for query in search_queries:
        jobs_for_query = serpapi_google_jobs_search(query, location, max_pages)
        all_jobs_raw.extend(jobs_for_query)
        time.sleep(2) # Add a delay between different search queries

    if not all_jobs_raw:
        print("No jobs found or error occurred during scraping.")
        return

    # De-duplicate raw results based on a unique identifier if available (e.g., job_id)
    unique_jobs = {job['job_id']: job for job in all_jobs_raw}.values()
    print(f"\nFound {len(all_jobs_raw)} total jobs, with {len(unique_jobs)} unique jobs after de-duplication.")

    # Save full raw JSON for backup with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_filename = f"soc_jobs_raw_{timestamp}.json"
    with open(raw_filename, "w", encoding="utf-8") as f:
        json.dump(list(unique_jobs), f, ensure_ascii=False, indent=4)
    print(f"Saved raw JSON: {raw_filename} ({len(unique_jobs)} jobs)")

    # Process and save data (your existing code here)
    jobs_flattened = []
    for job in unique_jobs:
        jobs_flattened.append({
            "Title": job.get("title", "N/A"),
            "Company": job.get("company_name", "N/A"),
            "Location": job.get("location", "N/A"),
            "Responsibilities": extract_responsibilities(job.get("description", ""))
        })

    df = pd.DataFrame(jobs_flattened)
    df.to_csv(f"soc_jobs_flattened_{timestamp}.csv", index=False)
    print(f"Saved flattened CSV: soc_jobs_flattened_{timestamp}.csv ({len(jobs_flattened)} jobs)")

if __name__ == "__main__":
    main()
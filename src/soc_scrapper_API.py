import os
import pandas as pd
import re
import time
import serpapi
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file (support UTF-8 BOM if present)
# using utf-8-sig will strip BOM if the file was saved with one
load_dotenv(encoding="utf-8-sig")


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


def get_quarter_folder():
    """Calculate current quarter folder (e.g., 2025-Q1)"""
    now = datetime.now()
    quarter = (now.month - 1) // 3 + 1
    return f"{now.year}-Q{quarter}"


def setup_raw_folders(source="serpapi"):
    """Create folder structure: data/raw/{source}/{quarter}/run_{timestamp}/"""
    base_raw = "data/raw"
    quarter = get_quarter_folder()
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_folder = os.path.join(base_raw, source, quarter, f"run_{run_timestamp}")
    
    os.makedirs(run_folder, exist_ok=True)
    return run_folder, run_timestamp


def setup_processed_folders(source="serpapi"):
    """Create folder structure: data/processed/{source}_{quarter}/"""
    base_processed = "data/processed"
    quarter = get_quarter_folder()
    processed_folder = os.path.join(base_processed, f"{source}_{quarter}")
    
    os.makedirs(processed_folder, exist_ok=True)
    return processed_folder


def update_runs_log(run_info):
    """Append run metadata to data/raw/runs_log.json"""
    log_file = "data/raw/runs_log.json"
    
    # Initialize log if it doesn't exist
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            runs = json.load(f)
    else:
        runs = []
    
    runs.append(run_info)
    
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(runs, f, ensure_ascii=False, indent=2)
    
    print(f"Updated runs_log.json (total runs: {len(runs)})")


def update_changelog(summary):
    """Create/update data/processed/CHANGELOG.md with run summary"""
    changelog_file = "data/processed/CHANGELOG.md"
    
    if not os.path.exists(changelog_file):
        with open(changelog_file, "w", encoding="utf-8") as f:
            f.write("# Scraping Changelog\n\n")
    
    with open(changelog_file, "a", encoding="utf-8") as f:
        f.write(f"## {summary['timestamp_display']}\n")
        f.write(f"- **Source**: {summary['source']}\n")
        f.write(f"- **Queries**: {', '.join(summary['queries'])}\n")
        f.write(f"- **Total Jobs**: {summary['total_jobs']} (unique: {summary['unique_jobs']})\n")
        f.write(f"- **Raw File**: {summary['raw_file']}\n")
        f.write(f"- **Processed File**: {summary['processed_file']}\n")
        f.write(f"\n")


def main():
    # --- Configuration ---
    source = "serpapi"
    
    # Comprehensive search queries inspired by NIST NICE, O*NET, and industry standards
    search_queries = [
        # Standard Industry Titles
        "SOC Analyst Tier 1",
        "SOC Analyst Level 1",
        "Junior SOC Analyst",
        "Associate SOC Analyst",
        "T1 SOC Analyst",
        "L1 SOC Analyst",
        
        # NIST NICE Framework (Cyber Defense Analyst - PR-CDA-001)
        "Cyber Defense Analyst Junior",
        "Cyber Defense Analyst Entry",
        "Cyber Defense Analyst I",
        
        # O*NET (Information Security Analyst - 15-1212.00)
        "Information Security Analyst Junior",
        "Information Security Analyst Entry",
        "Information Security Analyst Associate",
        
        # Specialized Tier 1 Roles
        "Security Triage Analyst",
        "Intrusion Analyst Junior",
        "SOC Monitor",
        "Security Operations Center Analyst I"
    ]
    
    location = "United States"
    max_pages = 50 # Max pages per query (10 results per page)
    # WARNING: Each (query * page) combination can consume SerpAPI credits.
    # 16 queries * 50 pages = up to 800 requests. 
    # For free tier (100 searches/month), consider reducing max_pages to 2-5.
    all_jobs_raw = []

    print("Starting job scraping via SerpApi...")
    run_start_time = datetime.now()
    
    for query in search_queries:
        jobs_for_query = serpapi_google_jobs_search(query, location, max_pages)
        all_jobs_raw.extend(jobs_for_query)
        time.sleep(2)

    if not all_jobs_raw:
        print("No jobs found or error occurred during scraping.")
        return

    # De-duplicate raw results
    unique_dict = {}
    skipped = 0
    for job in all_jobs_raw:
        jid = job.get("job_id")
        if jid:
            unique_dict[jid] = job
        else:
            skipped += 1
    if skipped:
        print(f"Warning: skipped {skipped} job(s) without a job_id field")
    unique_jobs = list(unique_dict.values())
    print(f"\nFound {len(all_jobs_raw)} total jobs, with {len(unique_jobs)} unique jobs after de-duplication.")

    # Setup folders and get paths
    raw_folder, run_timestamp = setup_raw_folders(source)
    processed_folder = setup_processed_folders(source)

    # Save raw JSON
    raw_filename = f"soc_jobs_raw_{run_timestamp}.json"
    raw_filepath = os.path.join(raw_folder, raw_filename)
    with open(raw_filepath, "w", encoding="utf-8") as f:
        json.dump(unique_jobs, f, ensure_ascii=False, indent=4)
    print(f"Saved raw JSON: {raw_filepath}")

    # Save run metadata
    run_duration = (datetime.now() - run_start_time).total_seconds()
    metadata = {
        "timestamp": run_timestamp,
        "source": source,
        "queries": search_queries,
        "location": location,
        "total_jobs_raw": len(all_jobs_raw),
        "unique_jobs": len(unique_jobs),
        "skipped": skipped,
        "duration_seconds": run_duration,
        "raw_file": raw_filepath
    }
    metadata_filepath = os.path.join(raw_folder, "run_metadata.json")
    with open(metadata_filepath, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    # Update runs log
    update_runs_log(metadata)

    # Process and save data
    jobs_flattened = []
    for job in unique_jobs:
        jobs_flattened.append({
            "Title": job.get("title", "N/A"),
            "Company": job.get("company_name", "N/A"),
            "Location": job.get("location", "N/A"),
            "Responsibilities": extract_responsibilities(job.get("description", ""))
        })

    df = pd.DataFrame(jobs_flattened)
    processed_filename = f"soc_jobs_flattened_{run_timestamp}.csv"
    processed_filepath = os.path.join(processed_folder, processed_filename)
    df.to_csv(processed_filepath, index=False)
    print(f"Saved flattened CSV: {processed_filepath}")

    # Update changelog
    update_changelog({
        "timestamp_display": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,
        "queries": search_queries,
        "total_jobs": len(all_jobs_raw),
        "unique_jobs": len(unique_jobs),
        "raw_file": raw_filepath,
        "processed_file": processed_filepath
    })

if __name__ == "__main__":
    main()
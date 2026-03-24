"""
job_feeds_extractor.py
- Indeed (RSS) + ZipRecruiter (public API) extractor
- Template function for LinkedIn via an external scraping API (SerpApi / Scrapingdog)
Outputs combined JSON and CSV with exact title and Responsibilities (if found).
"""

import requests
import feedparser
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from urllib.parse import quote_plus

# -------------------------
# Helper: extract 'Responsibilities' section from description text
# -------------------------
STOP_WORDS = ["Qualifications", "Requirements", "Description", "About the Role", "What you'll do", "Who you are"]

def extract_responsibilities(full_text: str) -> str:
    """
    Find 'Responsibilities' (case-insensitive) and slice out until the next stop word.
    Returns empty string if not found.
    """
    if not full_text:
        return ""
    lowered = full_text.lower()
    key = "responsibilities"
    if key not in lowered:
        # also accept 'your responsibilities' or 'key responsibilities'
        for alt in ["your responsibilities", "key responsibilities"]:
            if alt in lowered:
                key = alt
                break
        else:
            return ""

    # find index in original text to preserve casing
    idx = lowered.find(key)
    # take substring starting at the end of the header token
    start = idx + len(key)
    snippet = full_text[start:].strip()

    # cut at the first stop word occurrence
    for stop in STOP_WORDS:
        # search case-insensitive
        pos = snippet.lower().find(stop.lower())
        if pos != -1:
            snippet = snippet[:pos].strip()
            break

    # cleanup: remove leading punctuation/colon/newlines
    snippet = snippet.lstrip(":-\n\r\t ")
    return snippet.strip()

# -------------------------
# Indeed RSS
# -------------------------
def fetch_indeed_rss(query: str, location: str = ""):
    """
    Query Indeed's RSS feed and return list of {title, link, description_html}
    Example RSS URL: https://rss.indeed.com/rss?q=Information+Security+Analyst&l=
    (Indeed uses rss.indeed.com)
    """
    q = quote_plus(query)
    l = quote_plus(location) if location else ""
    rss_url = f"https://rss.indeed.com/rss?q={q}&l={l}"
    print("Fetching Indeed RSS:", rss_url)
    feed = feedparser.parse(rss_url)
    results = []
    for entry in feed.entries:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        # description is usually HTML snippet; may contain full or partial job details
        desc_html = entry.get("description", "") or entry.get("summary", "")
        results.append({"source": "indeed", "title": title, "link": link, "description_html": desc_html})
    return results

# -------------------------
# ZipRecruiter API (public)
# -------------------------
def fetch_ziprecruiter(query: str, api_key: str, location: str = "", pages: int = 1):
    """
    Uses ZipRecruiter public API.
    Docs: partner/job endpoints — you must register for an API key.
    Example endpoint for searches (public): https://api.ziprecruiter.com/jobs/v1?search=...&location=...&api_key=KEY
    """
    out = []
    base = "https://api.ziprecruiter.com/jobs/v1"
    for page in range(1, pages + 1):
        params = {
            "search": query,
            "location": location,
            "page": page,
            "api_key": api_key
        }
        print("ZipRecruiter request:", base, params)
        r = requests.get(base, params=params, timeout=15)
        if r.status_code != 200:
            print("ZipRecruiter returned:", r.status_code, r.text[:200])
            break
        j = r.json()
        jobs = j.get("jobs") or []
        for job in jobs:
            # job fields vary; we try to pull the canonical title and the full description (if present)
            title = job.get("name") or job.get("title") or job.get("job_title") or ""
            link = job.get("url") or job.get("job_url") or job.get("apply_url") or ""
            snippet = job.get("snippet") or job.get("description") or ""
            out.append({"source": "ziprecruiter", "title": title.strip(), "link": link.strip(), "description_html": snippet})
        time.sleep(0.5)
    return out

# -------------------------
# LinkedIn via commercial scraping API (template)
# -------------------------
def fetch_linkedin_via_api(query: str, api_key: str, provider: str = "serpapi", pages: int = 1):
    """
    Template: choose provider = 'serpapi' or 'scrapingdog' or 'scrapingdog' (or other).
    These providers typically require you to sign up and supply API keys.
    They return JSON with parsed job text. This function shows example for SerpApi and Scrapingdog.
    NOTE: You must sign up and replace 'api_key' with your key.
    """
    out = []
    if provider == "serpapi":
        # SerpApi Google Jobs or LinkedIn scraping requires different engine names.
        # For LinkedIn public search, SerpApi has LinkedIn endpoints; for Google Jobs use engine=google_jobs.
        # Example (SerpApi Google Jobs):
        base = "https://serpapi.com/search.json"
        for page in range(pages):
            params = {
                "engine": "google_jobs",   # or 'linkedin' variant if using their LinkedIn engine
                "q": query,
                "api_key": api_key,
                "start": page * 10
            }
            print("SerpApi request:", params)
            r = requests.get(base, params=params, timeout=20)
            if r.status_code != 200:
                print("SerpApi error:", r.status_code, r.text[:400])
                break
            j = r.json()
            # SerpApi returns job results in j.get('jobs_results') or similar for google_jobs
            jobs = j.get("jobs_results") or j.get("job_results") or []
            for job in jobs:
                title = job.get("title") or job.get("job_title") or ""
                link = job.get("link") or job.get("redirect") or job.get("job_link") or ""
                # SerpApi often delivers a structured 'items' list including titles like "Responsibilities"
                description = ""
                if "description" in job:
                    description = job.get("description")
                else:
                    # try to reconstruct from 'items'
                    items = job.get("items") or job.get("snippets") or []
                    description = "\n".join(items) if isinstance(items, list) else job.get("snippet", "")
                out.append({"source": "serpapi", "title": title.strip(), "link": link, "description_html": description})
            time.sleep(1)
    elif provider == "scrapingdog":
        # Example Scrapingdog endpoint for LinkedIn Jobs (replace with real provider docs)
        base = "https://api.scrapingdog.com/linkedinjobs"
        for page in range(1, pages + 1):
            params = {"api_key": api_key, "field": query, "page": page}
            print("Scrapingdog request:", params)
            r = requests.get(base, params=params, timeout=20)
            if r.status_code != 200:
                print("Scrapingdog error:", r.status_code, r.text[:400])
                break
            j = r.json()
            jobs = j.get("jobs") or []
            for job in jobs:
                out.append({"source": "scrapingdog", "title": job.get("title", "").strip(), "link": job.get("url", ""), "description_html": job.get("description", "")})
            time.sleep(1)
    else:
        raise ValueError("Unknown provider. Use 'serpapi' or 'scrapingdog'.")
    return out

# -------------------------
# Parsing HTML descriptions into plain text and extracting responsibilities
# -------------------------
def html_to_text(html):
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    # remove script/style tags
    for s in soup(["script", "style"]):
        s.decompose()
    return soup.get_text(separator="\n").strip()

# -------------------------
# Orchestration
# -------------------------
def run_pipeline(search_query, zip_api_key=None, linkedin_api_key=None, linkedin_provider="serpapi", location=""):
    all_results = []

    # Indeed RSS
    indeed = fetch_indeed_rss(search_query, location)
    for item in indeed:
        text = html_to_text(item["description_html"])
        resp = extract_responsibilities(text)
        all_results.append({
            "source": item["source"],
            "title": item["title"],
            "link": item["link"],
            "responsibilities": resp,
            "raw_description": text
        })

    # ZipRecruiter
    if zip_api_key:
        zr = fetch_ziprecruiter(search_query, zip_api_key, location, pages=1)
        for item in zr:
            text = html_to_text(item["description_html"])
            resp = extract_responsibilities(text)
            all_results.append({
                "source": item["source"],
                "title": item["title"],
                "link": item["link"],
                "responsibilities": resp,
                "raw_description": text
            })
    else:
        print("ZipRecruiter API key not provided; skipping ZipRecruiter fetch.")

    # LinkedIn via commercial scraper (optional)
    if linkedin_api_key:
        li = fetch_linkedin_via_api(search_query, linkedin_api_key, provider=linkedin_provider, pages=1)
        for item in li:
            text = html_to_text(item.get("description_html", "") or item.get("raw_html",""))
            resp = extract_responsibilities(text)
            all_results.append({
                "source": item["source"],
                "title": item["title"],
                "link": item.get("link", ""),
                "responsibilities": resp,
                "raw_description": text
            })
    else:
        print("LinkedIn API key not provided; skipping LinkedIn fetch.")

    # Save outputs
    df = pd.DataFrame(all_results)
    df.to_csv("jobs_combined.csv", index=False, encoding="utf-8")
    with open("jobs_combined.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_results)} records to jobs_combined.csv / jobs_combined.json")
    return all_results

# -------------------------
# Example usage (fill keys where needed)
# -------------------------
if __name__ == "__main__":
    SEARCH_QUERY = "SOC ANALYST TIER 1"
    ZIP_API_KEY = None          # <-- put your ZipRecruiter API key here
    LINKEDIN_API_KEY = None     # <-- put your SerpApi / Scrapingdog key here (optional)
    LINKEDIN_PROVIDER = "serpapi"  # or "scrapingdog"

    results = run_pipeline(SEARCH_QUERY, zip_api_key=ZIP_API_KEY, linkedin_api_key=LINKEDIN_API_KEY, linkedin_provider=LINKEDIN_PROVIDER, location="")
    # quick print of first results:
    for r in results[:10]:
        print("----")
        print(r["source"], "-", r["title"])
        print("Responsibilities:", (r["responsibilities"][:400] + "...") if r["responsibilities"] else "Not found")

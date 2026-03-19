import pandas as pd
import re
import json
import argparse
import os
import sys

def load_rules(filepath):
    """Loads classification rules from a JSON file."""
    try:
        with open(filepath, 'r') as f:
            rules = json.load(f)
        # Convert lists of strings to sets for efficient lookup
        for rule in rules:
            if 'must_contain' in rule:
                rule['must_contain'] = [set(word_list) for word_list in rule['must_contain']]
            if 'must_not_contain' in rule:
                rule['must_not_contain'] = [set(word_list) for word_list in rule['must_not_contain']]
        return rules
    except FileNotFoundError:
        print(f"Error: Rules file not found at '{filepath}'")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filepath}'")
        return None


def classify_title(title, rules):
    """Classifies a job title into a standardized category using a set of rules."""
    if not isinstance(title, str):
        return "Unclassified"

    # 1. Pre-processing: standardize the title for analysis
    processed_title = title.lower()
    # Standardize roman numerals
    processed_title = re.sub(r'\biii\b', '3', processed_title)
    processed_title = re.sub(r'\bii\b', '2', processed_title)
    processed_title = re.sub(r'\bi\b', '1', processed_title)
    # Remove content in parentheses and punctuation
    processed_title = re.sub(r'\(.*\)', '', processed_title)
    # Handle slashes between numbers, e.g., "1/2" -> "1 2"
    processed_title = re.sub(r'(\d)\s*/\s*(\d)', r'\1 \2', processed_title)
    processed_title = re.sub(r'[^\w\s]', '', processed_title)

    # Tokenize into a set for efficient keyword lookup
    title_words = set(processed_title.split())

    # 2. Apply rules to the title
    for rule in rules:
        # If the title contains any excluded word, skip to the next rule
        if any(title_words.intersection(word_set) for word_set in rule.get('must_not_contain', [])):
            continue

        # If the title contains at least one word from each required group, it's a match
        if all(title_words.intersection(word_set) for word_set in rule.get('must_contain', [])):
            return rule['name']

    return "Other / Unclassified" # Default category if no rules match


def analyze_job_data(df, rules_filepath):
    """
    Analyzes a DataFrame of job data.
    1. Classifies job titles.
    2. Filters for 'SOC Analyst Tier 1' and 'Other / Unclassified' jobs.
    3. Performs word count analysis on the filtered Tier 1 jobs.

    Returns:
        tuple: A tuple containing (soc_tier1_df, unclassified_df, stats_dict).
    """
    # --- 1. Classify all job titles ---
    print(f"Classifying titles using rules from '{rules_filepath}'...", file=sys.stderr)
    rules = load_rules(rules_filepath)
    if not rules:
        print("Could not load classification rules. Aborting analysis.", file=sys.stderr)
        return None, None, None

    if 'Title' not in df.columns:
        print("Error: 'Title' column not found in the DataFrame.", file=sys.stderr)
        return None, None, None

    df['Job Group'] = df['Title'].apply(lambda title: classify_title(title, rules))

    # --- 2. Filter for SOC Tier 1 and Unclassified jobs ---
    print("Filtering for 'SOC Analyst Tier 1' jobs...", file=sys.stderr)
    soc_tier1_df = df[df['Job Group'] == 'SOC Analyst Tier 1'].copy()
    unclassified_df = df[df['Job Group'] == 'Other / Unclassified'].copy()

    # --- 3. Perform word count analysis on SOC Tier 1 jobs ---
    if not soc_tier1_df.empty:
        print("Analyzing word counts for SOC Tier 1 jobs...", file=sys.stderr)
        if 'Responsibilities' in soc_tier1_df.columns:
            soc_tier1_df['Responsibilities'] = soc_tier1_df['Responsibilities'].fillna('')

            def get_word_counts(description):
                words = re.findall(r'\b\w+\b', str(description).lower())
                return len(words), len(set(words))

            counts = soc_tier1_df['Responsibilities'].apply(get_word_counts)
            soc_tier1_df[['Word Count', 'Unique Word Count']] = pd.DataFrame(
                counts.tolist(), index=soc_tier1_df.index
            )
        else:
            print("Warning: 'Responsibilities' column not found. Skipping word count analysis.", file=sys.stderr)
            soc_tier1_df[['Word Count', 'Unique Word Count']] = (0, 0)

    # --- 4. Prepare statistics ---
    stats = {
        "soc_tier1_count": len(soc_tier1_df),
        "unclassified_count": len(unclassified_df),
    }

    return soc_tier1_df, unclassified_df, stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Consolidate, de-duplicate, and analyze job data from CSV files."
    )
    parser.add_argument(
        "csv_files",
        nargs='+',
        help="Path(s) to the input CSV file(s) containing job data."
    )
    parser.add_argument(
        "rules_file",
        help="Path to the JSON file containing classification rules."
    )
    args = parser.parse_args()
    
    # --- 1. Ingestion & Consolidation ---
    print(f"Loading and consolidating {len(args.csv_files)} file(s)...")
    all_dfs = []
    for f in args.csv_files:
        try:
            all_dfs.append(pd.read_csv(f, encoding='latin1'))
        except FileNotFoundError:
            print(f"Warning: File not found at '{f}'. Skipping.", file=sys.stderr)
    
    if not all_dfs:
        print("No valid data files found. Aborting.", file=sys.stderr)
        sys.exit(1)

    master_df = pd.concat(all_dfs, ignore_index=True)
    total_jobs_before_dedup = len(master_df)
    print(f"Consolidated {total_jobs_before_dedup} total job listings.")

    # --- 2. De-duplication ---
    print("De-duplicating job listings...")
    unique_jobs_df = master_df.drop_duplicates(
        subset=['Title', 'Company', 'Location'], keep='first'
    ).copy()
    total_jobs_after_dedup = len(unique_jobs_df)
    print(f"Found {total_jobs_after_dedup} unique job listings.")

    # --- 3. Analysis ---
    soc1_df, unclassified_df, analysis_stats = analyze_job_data(
        unique_jobs_df, args.rules_file
    )

    # --- 4. Reporting and Saving ---
    if soc1_df is not None and unclassified_df is not None:
        # Prepare summary report
        summary_report = {
            "files_processed": args.csv_files,
            "total_listings_before_deduplication": total_jobs_before_dedup,
            "total_listings_after_deduplication": total_jobs_after_dedup,
            "filtered_soc_tier1_count": analysis_stats['soc_tier1_count'],
            "unclassified_count": analysis_stats['unclassified_count']
        }

        # Generate a base filename from the first input file
        base, _ = os.path.splitext(args.csv_files[0])
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        
        # Save summary
        summary_filepath = f"{base}_{timestamp}_summary.json"
        with open(summary_filepath, 'w', encoding='utf-8') as f:
            json.dump(summary_report, f, indent=2)
        print(f"\nAnalysis summary saved to '{summary_filepath}'")
        print(json.dumps(summary_report, indent=2))

        # Save SOC Tier 1 analysis
        if not soc1_df.empty:
            soc1_filepath = f"{base}_{timestamp}_soc_tier1_analysis.csv"
            soc1_df.to_csv(soc1_filepath, index=False)
            print(f"SOC Tier 1 analysis saved to '{soc1_filepath}'")

        # Save Unclassified jobs
        if not unclassified_df.empty:
            unclassified_filepath = f"{base}_{timestamp}_unclassified.csv"
            unclassified_df.to_csv(unclassified_filepath, index=False)
            print(f"Unclassified jobs saved to '{unclassified_filepath}'")

    print("Analysis complete.")

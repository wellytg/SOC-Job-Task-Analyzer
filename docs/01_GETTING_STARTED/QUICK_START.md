# Quick Start Tutorial

## Welcome to SOC Job Task Analyzer

This tutorial will get you up and running with the SOC Job Task Analyzer in under 15 minutes. By the end, you'll have collected, processed, and analyzed SOC job postings to identify key cybersecurity tasks and competencies.

## Prerequisites Check

Before starting, ensure you have:

- ✅ Python 3.10+ installed
- ✅ Virtual environment created and activated
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ SerpAPI key configured in `.env` file

If not, follow the [ENVIRONMENT.md](ENVIRONMENT.md) guide first.

## Step 1: Verify Your Setup

Let's make sure everything is working correctly.

```bash
# 1. Check Python version
python --version
# Should show: Python 3.10.x or higher

# 2. Verify virtual environment
which python
# Should point to your venv directory

# 3. Test imports
python -c "import pandas, requests, fuzzywuzzy; print('Dependencies OK')"

# 4. Check API key
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key:', 'Loaded' if os.getenv('SERPAPI_KEY') else 'Missing')"
```

## Step 2: Run Your First Data Collection

Let's collect some SOC job data from Google Jobs.

```bash
# Navigate to project directory (if not already there)
cd SOC-Job-Task-Analyzer

# Run data collection
python src/soc_scrapper_API.py
```

**What happens:**
- Queries Google Jobs API for SOC-related positions
- Saves raw data to `data/raw/serpapi/YYYY-Q#/run_*/`
- Extracts job responsibilities automatically
- Shows progress and completion status

**Expected output:**
```
Starting SOC job data collection...
Found 50 jobs for query: SOC Analyst
Processing page 1/2...
Extracted 25 job responsibilities
Saved to: data/raw/serpapi/2024-Q4/run_001/
Collection completed successfully
```

## Step 3: Classify Jobs

Now let's filter for SOC-specific roles and extract structured data.

```bash
# Run job classification
python src/data_analyzer.py
```

**What happens:**
- Reads raw job data from latest collection
- Applies classification rules from `configs/rules.json`
- Filters for SOC Tier 1 Analyst positions
- Saves processed CSV to `data/processed/`

**Expected output:**
```
Loading classification rules...
Processing 50 raw jobs...
Classified 35 SOC Tier 1 positions
Filtered out 15 non-SOC roles
Saved: data/processed/soc_jobs_flattened_20241201_120000_soc_tier1_analysis.csv
Classification completed
```

## Step 4: Aggregate Tasks

Combine all historical job data into a unified task lexicon.

```bash
# Run task aggregation
python src/task_aggregator.py
```

**What happens:**
- Reads all processed CSV files
- Extracts individual tasks from job descriptions
- Performs fuzzy deduplication (88% similarity threshold)
- Generates frequency analysis

**Expected output:**
```
Loading historical job data...
Found 5 processed CSV files
Extracted 1059 raw tasks
After deduplication: 291 unique tasks (72.5% reduction)
Saved consolidated tasks to: data/processed/task_lexicon/consolidated_tasks.json
Aggregation completed
```

## Step 5: Cluster Tasks by Theme

Group tasks into functional themes for LLM analysis.

```bash
# Run thematic clustering
python src/task_thematic_clusterer.py
```

**What happens:**
- Loads consolidated task lexicon
- Matches tasks to 10 predefined themes using keywords
- Calculates confidence scores for each assignment
- Generates clustering report

**Expected output:**
```
Loading task lexicon...
Clustering 291 tasks into themes...
Theme: threat_detection - 45 tasks (confidence: 0.92)
Theme: incident_response - 38 tasks (confidence: 0.89)
...
Clustering coverage: 82.8% (241/291 tasks)
Saved clustered tasks to: data/processed/task_lexicon/tasks_with_candidate_themes.json
Clustering completed
```

## Step 6: Run the Complete Pipeline

For future runs, use the orchestrator script for the full pipeline.

```bash
# Run complete analysis pipeline
python src/job_run.py
```

**What happens:**
- Executes all stages in sequence
- Provides progress updates and timing
- Generates comprehensive summary report
- Handles errors gracefully

**Expected output:**
```
SOC Job Task Analyzer - Pipeline Execution
==========================================

Stage 1/4: Data Collection... ✓ (45s)
Stage 2/4: Job Classification... ✓ (12s)
Stage 3/4: Task Aggregation... ✓ (8s)
Stage 4/4: Thematic Clustering... ✓ (3s)

Total execution time: 68 seconds

Results Summary:
- Jobs collected: 50
- SOC positions classified: 35
- Unique tasks identified: 291
- Tasks clustered: 241 (82.8%)

Pipeline completed successfully
```

## Step 7: Explore Your Results

Let's examine the outputs from your analysis.

### View Task Lexicon

```bash
# Check the consolidated tasks
python -c "
import json
with open('data/processed/task_lexicon/consolidated_tasks.json', 'r') as f:
    data = json.load(f)
    print(f'Total unique tasks: {len(data)}')
    print('Sample tasks:')
    for i, task in enumerate(data[:3]):
        print(f'{i+1}. {task[\"task_text\"]}')
"
```

### View Thematic Clusters

```bash
# Check clustering results
python -c "
import json
with open('data/processed/task_lexicon/tasks_with_candidate_themes.json', 'r') as f:
    data = json.load(f)
    print('Tasks by theme:')
    for theme, tasks in data.items():
        print(f'{theme}: {len(tasks)} tasks')
"
```

### View Pipeline Summary

```bash
# Check execution summary
python -c "
import json
with open('data/processed/pipeline_summary.json', 'r') as f:
    summary = json.load(f)
    print('Pipeline Summary:')
    print(f'Execution time: {summary[\"total_time_seconds\"]} seconds')
    print(f'Stages completed: {len(summary[\"stages\"])}')
    print(f'Data quality score: {summary[\"data_quality_score\"]}')
"
```

## Understanding Your Results

### Task Lexicon Structure

Each task in `consolidated_tasks.json` contains:

```json
{
  "task_id": "task_001",
  "task_text": "Monitor security alerts and investigate potential threats",
  "frequency": 15,
  "source_jobs": 12,
  "first_seen": "2024-10-01",
  "last_seen": "2024-12-01",
  "confidence_score": 0.95
}
```

### Thematic Clusters Structure

Tasks are grouped by functional themes:

```json
{
  "threat_detection": [
    {
      "task_id": "task_001",
      "task_text": "Monitor security alerts...",
      "confidence": 0.92,
      "keywords_matched": ["monitor", "alerts", "threats"]
    }
  ],
  "incident_response": [...],
  ...
}
```

## Common Next Steps

### Customize Classification Rules

Edit `configs/rules.json` to modify SOC role criteria:

```bash
# Open rules file
code configs/rules.json
```

### Run Pipeline with Options

```bash
# Skip data collection (use existing data)
python src/job_run.py --skip-raw

# Only run clustering (skip earlier stages)
python src/job_run.py --cluster-only

# Get help on all options
python src/job_run.py --help
```

### Visualize Results

Create simple visualizations of your data:

```python
# Quick analysis script
import pandas as pd
import json

# Load clustered tasks
with open('data/processed/task_lexicon/tasks_with_candidate_themes.json', 'r') as f:
    themes = json.load(f)

# Count tasks per theme
theme_counts = {theme: len(tasks) for theme, tasks in themes.items()}
print("Tasks per theme:")
for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{theme}: {count}")
```

## Troubleshooting Quick Fixes

### "API Key Not Found" Error
```bash
# Check .env file
cat .env
# Should contain: SERPAPI_KEY=your_key_here

# Test loading
python -c "from dotenv import load_dotenv, find_dotenv; print('Env file found:', find_dotenv())"
```

### "No Jobs Found" Error
```bash
# Check API key validity
python -c "
import requests
api_key = 'your_key_here'  # Replace with actual key
response = requests.get(f'https://serpapi.com/search?engine=google_jobs&q=SOC+Analyst&api_key={api_key}')
print('API Status:', response.status_code)
"
```

### "Import Error" Issues
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python path
python -c "import sys; print(sys.path)"
```

## Advanced Usage Examples

### Custom Data Collection

```python
# Modify search parameters in soc_scrapper_API.py
search_params = {
    'q': 'SOC Analyst',  # Change search query
    'location': 'United States',  # Add location filter
    'chips': 'date_posted:week'  # Filter by recency
}
```

### Batch Processing

```bash
# Run multiple times with different parameters
for location in "New York" "San Francisco" "Chicago"; do
    echo "Processing $location..."
    python src/soc_scrapper_API.py --location "$location"
done
```

### Integration with LLM Analysis

```python
# Load clustered data for LLM processing
import json

with open('data/processed/task_lexicon/tasks_with_candidate_themes.json', 'r') as f:
    clustered_data = json.load(f)

# Prepare for LLM analysis
for theme, tasks in clustered_data.items():
    print(f"Theme: {theme}")
    print(f"Tasks to analyze: {len(tasks)}")
    # Send to your preferred LLM for semantic analysis
```

## Performance Tips

- **API Limits**: SerpAPI free tier allows 100 searches/month
- **Processing Speed**: Full pipeline completes in ~14 seconds for typical datasets
- **Memory Usage**: Peak usage ~200MB for 1000+ jobs
- **Storage**: Plan for ~50MB per 1000 raw jobs collected

## Getting Help

If you encounter issues:

1. Check the [COMMON_ISSUES.md](../05_TROUBLESHOOTING/COMMON_ISSUES.md) guide
2. Review error messages carefully
3. Verify your environment setup
4. Check GitHub issues for similar problems

## What's Next?

Congratulations! You've successfully run the complete SOC Job Task Analyzer pipeline. Your results are now ready for:

- **Research Analysis**: Use the clustered tasks for academic studies
- **Curriculum Development**: Identify key SOC competencies
- **Industry Benchmarking**: Compare requirements across organizations
- **LLM Integration**: Feed the structured data to language models for deeper insights

Explore the full documentation for advanced features and customization options.

---

**Last Updated:** December 2024
**Version:** 1.0.0
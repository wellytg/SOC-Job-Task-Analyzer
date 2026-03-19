# Data Collection Module Reference

## Overview

The data collection module (`soc_scrapper_API.py`) is responsible for automated retrieval of SOC job postings from Google Jobs API via SerpAPI. This module handles API authentication, pagination, data extraction, deduplication, and quarter-based file organization for temporal analysis.

## Module Architecture

### Core Components

```python
class SOCJobScraper:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('SERPAPI_KEY')
        self.base_url = 'https://serpapi.com/search'
        self.processed_job_ids = set()

    def serpapi_google_jobs_search(self, query, **kwargs):
        """Main search method with pagination support"""

    def extract_responsibilities(self, job_description):
        """Parse job responsibilities from text"""

    def save_job_data(self, jobs_data, output_dir):
        """Save structured data with metadata"""
```

### Dependencies

**Required Packages**:
- `requests`: HTTP client for API calls
- `python-dotenv`: Environment variable loading
- `json`: Data serialization
- `os`: File system operations
- `datetime`: Timestamp handling

**Environment Variables**:
- `SERPAPI_KEY`: API authentication token (required)

## API Integration

### SerpAPI Configuration

**Base Parameters**:
```python
search_params = {
    'engine': 'google_jobs',
    'q': 'SOC Analyst',  # Search query
    'location': 'United States',  # Geographic filter
    'chips': 'date_posted:month',  # Time filter
    'api_key': self.api_key
}
```

**Optional Parameters**:
```python
extended_params = {
    'hl': 'en',  # Language
    'gl': 'us',  # Country
    'start': 0,  # Pagination offset
    'num': 10,  # Results per page
    'no_cache': True  # Force fresh results
}
```

### Rate Limiting & Error Handling

**Rate Limit Management**:
```python
def make_api_request(self, params, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            # Check for rate limit headers
            remaining = response.headers.get('X-RateLimit-Remaining')
            if remaining and int(remaining) < 10:
                time.sleep(60)  # Back off for rate limiting

            return response.json()

        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(2 ** attempt)  # Exponential backoff
```

**Error Types Handled**:
- `429 Too Many Requests`: Rate limit exceeded
- `401 Unauthorized`: Invalid API key
- `500 Internal Server Error`: SerpAPI service issues
- Network timeouts and connection errors

## Data Extraction Logic

### Job Data Parsing

**Raw API Response Structure**:
```json
{
  "jobs_results": [
    {
      "job_id": "unique_job_identifier",
      "title": "SOC Analyst",
      "company_name": "TechCorp Inc.",
      "location": "New York, NY",
      "description": "We are looking for a SOC Analyst to monitor...",
      "job_highlights": [
        {"title": "Responsibilities", "items": ["Monitor alerts", "Investigate incidents"]},
        {"title": "Requirements", "items": ["SIEM experience", "Security certifications"]}
      ],
      "extensions": ["Full-time", "3 days ago"],
      "detected_extensions": {
        "posted_at": "3 days ago",
        "schedule_type": "Full-time",
        "salary": "$80,000 - $100,000 a year"
      },
      "related_links": [
        {"text": "Apply on company site", "link": "https://..."}
      ]
    }
  ],
  "serpapi_pagination": {
    "next": "https://serpapi.com/search?engine=google_jobs&start=10...",
    "other_pages": {
      "2": "https://serpapi.com/search?engine=google_jobs&start=10...",
      "3": "https://serpapi.com/search?engine=google_jobs&start=20..."
    }
  }
}
```

### Responsibility Extraction

**Multi-Source Parsing**:
```python
def extract_responsibilities(self, job_data):
    responsibilities = []

    # Method 1: Structured highlights
    if 'job_highlights' in job_data:
        for highlight in job_data['job_highlights']:
            if highlight.get('title', '').lower() == 'responsibilities':
                responsibilities.extend(highlight.get('items', []))

    # Method 2: Description text parsing
    if 'description' in job_data:
        desc_responsibilities = self.parse_description_text(job_data['description'])
        responsibilities.extend(desc_responsibilities)

    # Method 3: Bullet point detection
    if responsibilities:
        responsibilities = self.clean_and_deduplicate(responsibilities)

    return responsibilities
```

**Text Parsing Patterns**:
```python
def parse_description_text(self, description):
    responsibilities = []

    # Split by common bullet markers
    lines = description.split('\n')
    for line in lines:
        line = line.strip()
        if self.is_responsibility_line(line):
            # Clean and normalize
            clean_line = self.clean_responsibility_text(line)
            if len(clean_line) > 10:  # Minimum length filter
                responsibilities.append(clean_line)

    return responsibilities

def is_responsibility_line(self, line):
    # Detect responsibility patterns
    responsibility_indicators = [
        line.startswith(('•', '-', '*')),  # Bullet points
        line.lower().startswith(('responsibilities', 'duties', 'you will')),
        any(keyword in line.lower() for keyword in [
            'monitor', 'analyze', 'respond', 'investigate',
            'maintain', 'configure', 'report', 'document'
        ])
    ]
    return any(responsibility_indicators)
```

## Deduplication Strategy

### Job-Level Deduplication

**ID-Based Tracking**:
```python
def is_duplicate_job(self, job_data):
    job_id = job_data.get('job_id')
    if not job_id:
        # Generate hash-based ID for jobs without explicit ID
        job_id = self.generate_job_hash(job_data)

    if job_id in self.processed_job_ids:
        return True

    self.processed_job_ids.add(job_id)
    return False

def generate_job_hash(self, job_data):
    # Create deterministic hash from key fields
    key_data = f"{job_data.get('title', '')}|{job_data.get('company_name', '')}|{job_data.get('location', '')}"
    return hashlib.md5(key_data.encode()).hexdigest()
```

### Responsibility Deduplication

**Within-Job Deduplication**:
```python
def clean_and_deduplicate(self, responsibilities):
    cleaned = []
    seen = set()

    for resp in responsibilities:
        # Normalize text
        normalized = self.normalize_text(resp)

        # Skip if already seen
        if normalized not in seen:
            seen.add(normalized)
            cleaned.append(resp)  # Keep original formatting

    return cleaned
```

## File Organization

### Quarter-Based Structure

**Directory Hierarchy**:
```
data/raw/serpapi/
├── 2024-Q4/
│   ├── run_001/
│   │   ├── jobs_20241201_120000.json
│   │   ├── metadata.json
│   │   └── responsibilities_extracted.json
│   └── runs_log.json
├── 2024-Q3/
│   └── ...
└── 2023-Q4/
    └── ...
```

**Naming Convention**:
- **Directory**: `{YYYY}-Q{Q}` (year-quarter format)
- **Run**: `run_{NNN}` (sequential run number)
- **Files**: `{type}_{timestamp}.json` (ISO format timestamp)

### Metadata Tracking

**Run Metadata** (`metadata.json`):
```json
{
  "run_info": {
    "run_id": "run_001",
    "timestamp": "2024-12-01T12:00:00Z",
    "quarter": "2024-Q4",
    "search_query": "SOC Analyst",
    "search_location": "United States"
  },
  "api_info": {
    "calls_made": 3,
    "rate_limit_remaining": 97,
    "serpapi_version": "2024.11.15"
  },
  "data_stats": {
    "jobs_found": 45,
    "jobs_processed": 42,
    "duplicates_removed": 3,
    "responsibilities_extracted": 128,
    "avg_responsibilities_per_job": 3.05
  },
  "processing_stats": {
    "start_time": "2024-12-01T12:00:00Z",
    "end_time": "2024-12-01T12:00:45Z",
    "duration_seconds": 45.2,
    "memory_peak_mb": 45
  }
}
```

**Quarter Log** (`runs_log.json`):
```json
{
  "quarter": "2024-Q4",
  "runs": [
    {
      "run_id": "run_001",
      "timestamp": "2024-12-01T12:00:00Z",
      "jobs_collected": 45,
      "status": "completed"
    }
  ],
  "quarter_stats": {
    "total_runs": 1,
    "total_jobs": 45,
    "date_range": {
      "first_run": "2024-12-01T12:00:00Z",
      "last_run": "2024-12-01T12:00:00Z"
    }
  }
}
```

## Data Quality Assurance

### Validation Checks

**Job Data Validation**:
```python
def validate_job_data(self, job_data):
    required_fields = ['title', 'company_name', 'description']
    missing_fields = []

    for field in required_fields:
        if not job_data.get(field):
            missing_fields.append(field)

    if missing_fields:
        self.logger.warning(f"Job missing fields: {missing_fields}")
        return False

    return True
```

**Data Quality Metrics**:
- **Completeness**: Percentage of jobs with all required fields
- **Validity**: Jobs passing basic validation checks
- **Consistency**: Data format adherence across runs
- **Timeliness**: Age of collected job postings

### Error Recovery

**Graceful Degradation**:
```python
def process_job_safely(self, job_data):
    try:
        # Validate data structure
        if not self.validate_job_data(job_data):
            self.stats['invalid_jobs'] += 1
            return None

        # Extract responsibilities
        responsibilities = self.extract_responsibilities(job_data)

        # Create structured output
        processed_job = {
            'job_id': job_data.get('job_id'),
            'title': job_data.get('title'),
            'company': job_data.get('company_name'),
            'location': job_data.get('location'),
            'responsibilities': responsibilities,
            'metadata': {
                'extracted_at': datetime.now().isoformat(),
                'responsibility_count': len(responsibilities),
                'data_quality_score': self.calculate_quality_score(job_data)
            }
        }

        return processed_job

    except Exception as e:
        self.logger.error(f"Error processing job: {e}")
        self.stats['processing_errors'] += 1
        return None
```

## Performance Optimization

### Memory Management

**Streaming Processing**:
```python
def process_large_result_set(self, all_jobs):
    # Process in batches to manage memory
    batch_size = 50
    processed_jobs = []

    for i in range(0, len(all_jobs), batch_size):
        batch = all_jobs[i:i + batch_size]
        batch_processed = [self.process_job_safely(job) for job in batch]
        processed_jobs.extend([j for j in batch_processed if j])

        # Optional: Save intermediate results
        if len(processed_jobs) % 100 == 0:
            self.save_intermediate_results(processed_jobs)

    return processed_jobs
```

### API Optimization

**Request Batching**:
- Single API call per page (SerpAPI limitation)
- Parallel processing of independent pages (future enhancement)
- Intelligent pagination to avoid redundant calls

**Caching Strategy**:
- No caching by default (fresh data requirement)
- Optional caching for development/testing
- Cache invalidation based on time windows

## Configuration Options

### Search Customization

**Query Variations**:
```python
# Different SOC role queries
queries = [
    'SOC Analyst',
    'Security Operations Center Analyst',
    'Cybersecurity SOC',
    'Threat Detection Analyst'
]
```

**Geographic Targeting**:
```python
locations = [
    'United States',
    'New York, NY',
    'San Francisco, CA',
    'Remote'
]
```

**Time Filters**:
```python
time_filters = [
    'date_posted:day',    # Last 24 hours
    'date_posted:week',   # Last week
    'date_posted:month',  # Last month
    None                  # No time filter
]
```

### Output Customization

**Data Format Options**:
- **JSON**: Full structured data with metadata
- **CSV**: Flattened format for spreadsheet analysis
- **Compressed**: Gzip compression for large datasets

**File Organization**:
- **Quarter-based**: Temporal organization
- **Run-based**: Execution session grouping
- **Flat structure**: Simple directory layout

## Monitoring and Logging

### Execution Logging

**Structured Logging**:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('soc_scraper')
```

**Log Categories**:
- **INFO**: Normal execution progress
- **WARNING**: Recoverable issues (missing fields, API slowdowns)
- **ERROR**: Critical failures requiring attention
- **DEBUG**: Detailed execution tracing

### Metrics Collection

**Performance Metrics**:
- API call count and success rate
- Processing time per job
- Memory usage patterns
- Error frequency by type

**Data Quality Metrics**:
- Job completeness percentage
- Responsibility extraction success rate
- Deduplication efficiency
- Data validation pass rate

## Integration Points

### Downstream Modules

**Data Handover**:
```python
# Prepare data for classification module
def prepare_for_classification(self, processed_jobs):
    # Convert to expected format
    classification_input = []
    for job in processed_jobs:
        for responsibility in job['responsibilities']:
            classification_input.append({
                'job_id': job['job_id'],
                'title': job['title'],
                'company': job['company'],
                'location': job['location'],
                'responsibility': responsibility,
                'source': 'serpapi_collection'
            })
    return classification_input
```

### Pipeline Integration

**Orchestrator Interface**:
```python
# Integration with job_run.py
def run_data_collection():
    scraper = SOCJobScraper()
    jobs_data = scraper.serpapi_google_jobs_search('SOC Analyst')

    # Validate collection success
    if not jobs_data:
        raise PipelineError("Data collection failed")

    # Prepare for next stage
    processed_data = scraper.prepare_for_classification(jobs_data)

    return processed_data
```

## Troubleshooting Guide

### Common Issues

**API Key Problems**:
```
Error: 401 Unauthorized
Solution: Verify SERPAPI_KEY in .env file
```

**Rate Limiting**:
```
Error: 429 Too Many Requests
Solution: Implement delays, reduce query frequency
```

**Empty Results**:
```
Issue: No jobs returned
Solution: Check query parameters, try different location/time filters
```

**Memory Issues**:
```
Error: Out of memory
Solution: Process in smaller batches, increase system RAM
```

### Diagnostic Tools

**API Testing**:
```bash
# Test API connectivity
curl "https://serpapi.com/search?engine=google_jobs&q=SOC+Analyst&api_key=YOUR_KEY"
```

**Data Validation**:
```python
# Validate collected data
import json
with open('data/raw/serpapi/2024-Q4/run_001/jobs_20241201_120000.json', 'r') as f:
    data = json.load(f)
    print(f"Jobs collected: {len(data)}")
    print(f"Sample job: {data[0] if data else 'None'}")
```

This module provides robust, scalable data collection capabilities with comprehensive error handling, quality assurance, and integration support for the complete SOC job analysis pipeline.

---

**Last Updated:** December 2024
**Version:** 1.0.0
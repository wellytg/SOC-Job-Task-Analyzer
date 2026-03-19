# Raw Data Schema Reference

## Overview

This document defines the structure and format of raw data collected from the SerpAPI Google Jobs integration. Understanding these schemas is essential for data validation, processing pipeline development, and ensuring data quality throughout the SOC Job Task Analyzer system.

## SerpAPI Response Structure

### Base API Response

**Top-Level Response Structure**:
```json
{
  "search_metadata": {
    "id": "67890...",
    "status": "Success",
    "json_endpoint": "https://serpapi.com/searches/...",
    "created_at": "2024-12-01 12:00:00 UTC",
    "processed_at": "2024-12-01 12:00:01 UTC",
    "google_jobs_url": "https://www.google.com/search?q=SOC+Analyst...",
    "raw_html_file": "https://serpapi.com/searches/.../raw_html",
    "total_time_taken": 1.23
  },
  "search_parameters": {
    "engine": "google_jobs",
    "q": "SOC Analyst",
    "location": "United States",
    "chips": "date_posted:month"
  },
  "jobs_results": [
    // Array of job objects
  ],
  "serpapi_pagination": {
    // Pagination information
  }
}
```

### Job Object Schema

**Complete Job Structure**:
```json
{
  "job_id": "eyJqb2JfdGl0bGUiOi...",
  "title": "SOC Analyst",
  "company_name": "TechCorp Inc.",
  "location": "New York, NY",
  "via": "via LinkedIn",
  "description": "We are looking for a SOC Analyst to monitor security alerts...",
  "job_highlights": [
    {
      "title": "Responsibilities",
      "items": [
        "Monitor security alerts and investigate potential threats",
        "Respond to security incidents within SLA timelines",
        "Document incident response activities"
      ]
    },
    {
      "title": "Requirements",
      "items": [
        "3+ years of SOC experience",
        "Experience with SIEM tools",
        "Security certifications preferred"
      ]
    }
  ],
  "extensions": [
    "Full-time",
    "3 days ago"
  ],
  "detected_extensions": {
    "posted_at": "3 days ago",
    "work_from_home": false,
    "schedule_type": "Full-time",
    "salary": "$80,000 - $100,000 a year"
  },
  "related_links": [
    {
      "text": "Apply on company site",
      "link": "https://example.com/careers/soc-analyst"
    }
  ],
  "thumbnail": "https://encrypted-tbn0.gstatic.com/..."
}
```

## Field Definitions

### Core Job Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `job_id` | string | Yes | Unique Google Jobs identifier | `"eyJqb2JfdGl0bGUiOi..."` |
| `title` | string | Yes | Job title | `"SOC Analyst"` |
| `company_name` | string | Yes | Company name | `"TechCorp Inc."` |
| `location` | string | No | Job location | `"New York, NY"` |
| `description` | string | Yes | Full job description | `"We are looking for..."` |
| `via` | string | No | Application source | `"via LinkedIn"` |

### Job Highlights Structure

**Highlights Array**:
```json
"job_highlights": [
  {
    "title": "Responsibilities",
    "items": [
      "Monitor security alerts and investigate potential threats",
      "Respond to security incidents within SLA timelines"
    ]
  },
  {
    "title": "Requirements",
    "items": [
      "3+ years of SOC experience",
      "Experience with SIEM tools"
    ]
  },
  {
    "title": "Benefits",
    "items": [
      "Competitive salary",
      "Health insurance"
    ]
  }
]
```

**Common Highlight Titles**:
- `Responsibilities` / `Duties` / `What You'll Do`
- `Requirements` / `Qualifications` / `What You Need`
- `Benefits` / `What We Offer`
- `About Us` / `Company Overview`

### Extensions and Metadata

**Extensions Array**:
```json
"extensions": [
  "Full-time",
  "3 days ago",
  "No degree required",
  "$80,000 - $100,000 a year"
]
```

**Detected Extensions Object**:
```json
"detected_extensions": {
  "posted_at": "3 days ago",
  "work_from_home": false,
  "schedule_type": "Full-time",
  "salary": "$80,000 - $100,000 a year",
  "contract_type": "Permanent"
}
```

### Related Links

**Links Array**:
```json
"related_links": [
  {
    "text": "Apply on company site",
    "link": "https://example.com/careers/soc-analyst"
  },
  {
    "text": "View job",
    "link": "https://www.google.com/search?q=job&job_id=..."
  }
]
```

## Pagination Structure

### SerpAPI Pagination

**Pagination Object**:
```json
"serpapi_pagination": {
  "next": "https://serpapi.com/search?engine=google_jobs&q=SOC+Analyst&start=10",
  "next_page_token": "CAoQC...",
  "other_pages": {
    "2": "https://serpapi.com/search?engine=google_jobs&q=SOC+Analyst&start=10",
    "3": "https://serpapi.com/search?engine=google_jobs&q=SOC+Analyst&start=20",
    "4": "https://serpapi.com/search?engine=google_jobs&q=SOC+Analyst&start=30"
  }
}
```

**Pagination Parameters**:
- `start`: Result offset (0, 10, 20, etc.)
- `next_page_token`: Google's pagination token
- `num`: Results per page (default: 10)

## Data Quality Considerations

### Field Completeness

**Required vs Optional Fields**:
- **Always Present**: `job_id`, `title`, `company_name`, `description`
- **Usually Present**: `location`, `extensions`
- **Sometimes Present**: `job_highlights`, `detected_extensions`, `related_links`
- **Rarely Present**: `thumbnail`, `via`

### Data Consistency Issues

**Common Inconsistencies**:
- Location formats vary (`"New York, NY"`, `"Remote"`, `"United States"`)
- Salary formats differ (`"$80,000 - $100,000 a year"`, `"$25/hour"`)
- Date formats vary (`"3 days ago"`, `"2024-12-01"`)
- Company names may have variations (`"Google Inc."`, `"Google"`)

### Missing Data Patterns

**Typical Missing Fields**:
- `location`: ~15% of jobs
- `job_highlights`: ~30% of jobs
- `detected_extensions`: ~40% of jobs
- `salary`: ~70% of jobs
- `thumbnail`: ~80% of jobs

## Processed Raw Data Format

### Internal Storage Structure

**Processed Job Object**:
```json
{
  "job_id": "eyJqb2JfdGl0bGUiOi...",
  "title": "SOC Analyst",
  "company": "TechCorp Inc.",
  "location": "New York, NY",
  "description": "We are looking for a SOC Analyst to monitor security alerts...",
  "responsibilities": [
    "Monitor security alerts and investigate potential threats",
    "Respond to security incidents within SLA timelines",
    "Document incident response activities"
  ],
  "requirements": [
    "3+ years of SOC experience",
    "Experience with SIEM tools"
  ],
  "metadata": {
    "posted_date": "2024-11-28",
    "schedule_type": "Full-time",
    "salary_range": "$80,000 - $100,000",
    "source_url": "https://example.com/careers/soc-analyst",
    "collected_at": "2024-12-01T12:00:00Z",
    "data_quality_score": 0.95
  }
}
```

### Data Extraction Logic

**Responsibility Extraction**:
```python
def extract_responsibilities(job_data):
    responsibilities = []

    # Method 1: Structured highlights
    if 'job_highlights' in job_data:
        for highlight in job_data['job_highlights']:
            if highlight['title'].lower() in ['responsibilities', 'duties', 'what you\'ll do']:
                responsibilities.extend(highlight['items'])

    # Method 2: Description text parsing
    if 'description' in job_data:
        desc_responsibilities = parse_description_for_tasks(job_data['description'])
        responsibilities.extend(desc_responsibilities)

    return responsibilities
```

**Metadata Extraction**:
```python
def extract_metadata(job_data):
    metadata = {
        'collected_at': datetime.now().isoformat(),
        'data_quality_score': calculate_quality_score(job_data)
    }

    # Posted date
    if 'detected_extensions' in job_data and 'posted_at' in job_data['detected_extensions']:
        metadata['posted_date'] = parse_relative_date(job_data['detected_extensions']['posted_at'])

    # Schedule type
    if 'detected_extensions' in job_data and 'schedule_type' in job_data['detected_extensions']:
        metadata['schedule_type'] = job_data['detected_extensions']['schedule_type']

    # Salary
    if 'detected_extensions' in job_data and 'salary' in job_data['detected_extensions']:
        metadata['salary_range'] = job_data['detected_extensions']['salary']

    return metadata
```

## File Organization

### Raw Data Storage Structure

```
data/raw/serpapi/
├── 2024-Q4/
│   ├── run_001/
│   │   ├── jobs_20241201_120000.json
│   │   ├── metadata.json
│   │   └── responsibilities_extracted.json
│   └── runs_log.json
└── 2024-Q3/
    └── ...
```

**Run Metadata File** (`metadata.json`):
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
    "responsibilities_extracted": 128,
    "avg_responsibilities_per_job": 3.05
  }
}
```

**Quarter Runs Log** (`runs_log.json`):
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

## Data Validation Rules

### Schema Validation

**JSON Schema Definition**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["job_id", "title", "company_name", "description"],
  "properties": {
    "job_id": {
      "type": "string",
      "minLength": 10
    },
    "title": {
      "type": "string",
      "minLength": 3
    },
    "company_name": {
      "type": "string",
      "minLength": 2
    },
    "location": {
      "type": "string"
    },
    "description": {
      "type": "string",
      "minLength": 50
    },
    "job_highlights": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["title", "items"],
        "properties": {
          "title": {"type": "string"},
          "items": {
            "type": "array",
            "items": {"type": "string"}
          }
        }
      }
    }
  }
}
```

### Quality Scoring

**Data Quality Metrics**:
```python
def calculate_quality_score(job_data):
    score = 0
    max_score = 10

    # Required fields present (4 points)
    required_fields = ['job_id', 'title', 'company_name', 'description']
    score += sum(1 for field in required_fields if job_data.get(field)) * 1

    # Location present (1 point)
    if job_data.get('location'):
        score += 1

    # Job highlights present (2 points)
    if job_data.get('job_highlights'):
        score += 2

    # Detected extensions present (2 points)
    if job_data.get('detected_extensions'):
        score += 2

    # Related links present (1 point)
    if job_data.get('related_links'):
        score += 1

    return score / max_score
```

## Error Handling

### API Error Responses

**Common Error Codes**:
- `401 Unauthorized`: Invalid API key
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: SerpAPI service issues
- `400 Bad Request`: Invalid search parameters

**Error Response Structure**:
```json
{
  "error": "Invalid API key. Please check your SerpAPI credentials.",
  "status": 401
}
```

### Data Processing Errors

**Handling Missing Fields**:
```python
def safe_extract_field(job_data, field_path, default=None):
    """Safely extract nested field values"""
    try:
        keys = field_path.split('.')
        value = job_data
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default
```

**Logging Data Issues**:
```python
def log_data_quality_issue(job_data, issue_type, details):
    """Log data quality problems for analysis"""
    quality_log = {
        'job_id': job_data.get('job_id', 'unknown'),
        'issue_type': issue_type,
        'details': details,
        'timestamp': datetime.now().isoformat(),
        'job_title': job_data.get('title', ''),
        'company': job_data.get('company_name', '')
    }

    # Append to quality issues log
    with open('logs/data_quality_issues.jsonl', 'a') as f:
        json.dump(quality_log, f)
        f.write('\n')
```

## Version Compatibility

### SerpAPI Version Changes

**Version 2024.11.15** (Current):
- Added `detected_extensions` field
- Improved job highlights parsing
- Enhanced pagination tokens

**Migration Notes**:
- Older versions may lack `detected_extensions`
- Job ID formats have changed over time
- Description field length limits vary

### Backward Compatibility

**Handling Version Differences**:
```python
def normalize_api_response(response_data, api_version):
    """Normalize response format across API versions"""
    if api_version >= "2024.11.15":
        # Current format
        return response_data
    elif api_version >= "2024.08.01":
        # Add detected_extensions if missing
        for job in response_data.get('jobs_results', []):
            if 'detected_extensions' not in job:
                job['detected_extensions'] = extract_legacy_extensions(job)
        return response_data
    else:
        # Legacy format conversion
        return convert_legacy_format(response_data)
```

This schema documentation ensures consistent data handling, validation, and processing throughout the SOC Job Task Analyzer pipeline, supporting reliable research data collection and analysis.

---

**Last Updated:** December 2024
**Version:** 1.0.0
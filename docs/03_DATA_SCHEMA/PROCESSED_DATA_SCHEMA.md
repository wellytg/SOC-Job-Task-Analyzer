# Processed Data Schema Reference

## Overview

This document defines the structure and format of intermediate and processed data generated during the SOC Job Task Analyzer pipeline. These schemas represent the transformation from raw API responses to structured, analysis-ready datasets suitable for research and LLM integration.

## Classification Output Schema

### SOC Tier 1 Analysis CSV

**File Location**: `data/processed/soc_jobs_flattened_*.csv`

**CSV Structure**:
```csv
job_id,title,company,location,responsibility,posted_date,job_url,source
123456789,SOC Analyst,TechCorp Inc.,New York NY,Monitor security alerts and investigate potential threats,2024-11-28,https://example.com/job/123,serpapi
123456789,SOC Analyst,TechCorp Inc.,New York NY,Respond to security incidents within SLA timelines,2024-11-28,https://example.com/job/123,serpapi
```

**Field Definitions**:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `job_id` | string | Yes | Unique job identifier | `"123456789"` |
| `title` | string | Yes | Normalized job title | `"SOC Analyst"` |
| `company` | string | Yes | Company name | `"TechCorp Inc."` |
| `location` | string | No | Job location | `"New York NY"` |
| `responsibility` | string | Yes | Individual job responsibility | `"Monitor security alerts..."` |
| `posted_date` | string | No | Job posting date (ISO format) | `"2024-11-28"` |
| `job_url` | string | No | Original job posting URL | `"https://example.com/job/123"` |
| `source` | string | Yes | Data source identifier | `"serpapi"` |

**Data Characteristics**:
- **Granularity**: One row per responsibility per job
- **Deduplication**: No deduplication at this stage
- **Normalization**: Basic text cleaning applied
- **Volume**: Typically 2-5 rows per job

## Task Lexicon Schema

### Consolidated Tasks JSON

**File Location**: `data/processed/task_lexicon/consolidated_tasks.json`

**JSON Structure**:
```json
[
  {
    "task_id": "task_001",
    "task_text": "Monitor security alerts and investigate potential threats",
    "frequency": 15,
    "source_jobs": ["job_123", "job_456", "job_789"],
    "first_seen": "2024-10-01T00:00:00Z",
    "last_seen": "2024-12-01T00:00:00Z",
    "source_files": [
      "soc_jobs_flattened_20241001_soc_tier1_analysis.csv",
      "soc_jobs_flattened_20241101_soc_tier1_analysis.csv"
    ],
    "confidence_score": 0.95,
    "cluster_size": 12
  }
]
```

**Field Definitions**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `task_id` | string | Yes | Unique task identifier (`task_NNN`) |
| `task_text` | string | Yes | Consolidated task description |
| `frequency` | integer | Yes | Number of occurrences across all jobs |
| `source_jobs` | array | Yes | List of job IDs containing this task |
| `first_seen` | string | Yes | Earliest occurrence date (ISO format) |
| `last_seen` | string | Yes | Latest occurrence date (ISO format) |
| `source_files` | array | Yes | CSV files where task was found |
| `confidence_score` | float | Yes | Deduplication confidence (0.0-1.0) |
| `cluster_size` | integer | Yes | Number of similar tasks merged |

### Task Frequency Report

**File Location**: `data/processed/task_lexicon/task_frequency_report.json`

**JSON Structure**:
```json
{
  "summary": {
    "total_raw_tasks": 1059,
    "unique_tasks": 291,
    "deduplication_rate": 0.725,
    "average_frequency": 3.6,
    "max_frequency": 28,
    "date_range": {
      "earliest": "2024-10-01",
      "latest": "2024-12-01"
    }
  },
  "frequency_distribution": {
    "1_occurrence": 45,
    "2_5_occurrences": 156,
    "6_10_occurrences": 68,
    "11_plus_occurrences": 22
  },
  "top_tasks": [
    {
      "task_text": "Monitor security alerts and investigate potential threats",
      "frequency": 28,
      "percentage": 2.6
    }
  ],
  "temporal_analysis": {
    "tasks_by_month": {
      "2024-10": 145,
      "2024-11": 98,
      "2024-12": 48
    }
  }
}
```

## Thematic Clustering Schema

### Clustered Tasks JSON

**File Location**: `data/processed/task_lexicon/tasks_with_candidate_themes.json`

**JSON Structure**:
```json
{
  "threat_detection": [
    {
      "task_id": "task_001",
      "task_text": "Monitor security alerts and investigate potential threats",
      "theme": "threat_detection",
      "confidence": 0.92,
      "keywords_matched": ["monitor", "alert", "threat"],
      "frequency": 28,
      "source_jobs": ["job_123", "job_456"],
      "all_theme_scores": {
        "threat_detection": {"score": 0.92, "matched_keywords": ["monitor", "alert", "threat"]},
        "incident_response": {"score": 0.45, "matched_keywords": ["investigate"]},
        "threat_hunting": {"score": 0.23, "matched_keywords": []}
      }
    }
  ],
  "unassigned": [
    {
      "task_id": "task_089",
      "task_text": "Perform general administrative duties as assigned",
      "theme": "unassigned",
      "confidence": 0.05,
      "keywords_matched": [],
      "frequency": 3,
      "source_jobs": ["job_999"]
    }
  ]
}
```

**Theme Structure**:
- **Keys**: Theme names (10 predefined + "unassigned")
- **Values**: Array of task objects with clustering metadata

### Clustering Validation Report

**File Location**: `data/processed/task_lexicon/clustering_validation.json`

**JSON Structure**:
```json
{
  "clustering_summary": {
    "total_tasks": 291,
    "assigned_tasks": 241,
    "unassigned_tasks": 50,
    "coverage_percentage": 82.8,
    "average_confidence": 0.76
  },
  "theme_distribution": {
    "threat_detection": 45,
    "incident_response": 38,
    "log_analysis": 32,
    "security_monitoring": 29,
    "vulnerability_management": 25,
    "communication": 22,
    "tool_configuration": 18,
    "threat_hunting": 15,
    "forensic_analysis": 12,
    "compliance_reporting": 5
  },
  "confidence_distribution": {
    "high_confidence_0.8_1.0": 189,
    "medium_confidence_0.5_0.8": 42,
    "low_confidence_0.1_0.5": 10,
    "unassigned_0_0.1": 50
  },
  "quality_metrics": {
    "theme_balance_score": 0.72,
    "confidence_consistency": 0.85,
    "keyword_match_accuracy": 0.91
  }
}
```

## Pipeline Summary Schema

### Execution Summary JSON

**File Location**: `data/processed/pipeline_summary.json`

**JSON Structure**:
```json
{
  "execution_info": {
    "start_time": "2024-12-01T12:00:00Z",
    "end_time": "2024-12-01T12:01:09Z",
    "total_time_seconds": 69.4,
    "success": true
  },
  "stages": [
    {
      "name": "data_collection",
      "duration_seconds": 45.2,
      "status": "completed",
      "metrics": {
        "jobs_collected": 45,
        "api_calls": 3,
        "data_quality": 0.96
      }
    },
    {
      "name": "job_classification",
      "duration_seconds": 12.3,
      "status": "completed",
      "metrics": {
        "jobs_processed": 45,
        "jobs_classified": 35,
        "classification_rate": 0.778
      }
    },
    {
      "name": "task_aggregation",
      "duration_seconds": 8.7,
      "status": "completed",
      "metrics": {
        "raw_tasks": 1059,
        "unique_tasks": 291,
        "deduplication_rate": 0.725
      }
    },
    {
      "name": "thematic_clustering",
      "duration_seconds": 3.2,
      "status": "completed",
      "metrics": {
        "tasks_clustered": 241,
        "coverage_rate": 0.828,
        "average_confidence": 0.76
      }
    }
  ],
  "overall_metrics": {
    "data_quality_score": 0.89,
    "files_generated": 6,
    "peak_memory_mb": 185,
    "error_count": 0
  }
}
```

## Data Transformation Flow

### Stage-by-Stage Evolution

**1. Raw API Response → Classification CSV**:
```
{
  "job_id": "123",
  "title": "SOC Analyst",
  "description": "...",
  "job_highlights": [{"items": ["Task 1", "Task 2"]}]
}
```
↓
```
job_id,title,responsibility
123,SOC Analyst,Task 1
123,SOC Analyst,Task 2
```

**2. Classification CSV → Consolidated Tasks**:
```
Multiple CSV rows with similar responsibilities
```
↓
```
{
  "task_id": "task_001",
  "task_text": "Consolidated task description",
  "frequency": 15,
  "source_jobs": ["job_123", "job_456"]
}
```

**3. Consolidated Tasks → Thematic Clusters**:
```
Array of task objects
```
↓
```
{
  "threat_detection": [
    {
      "task_id": "task_001",
      "theme": "threat_detection",
      "confidence": 0.92
    }
  ]
}
```

## Data Quality Metrics

### Validation Rules

**Completeness Checks**:
```python
def validate_processed_data(data, schema_type):
    """Validate processed data against schema requirements"""

    if schema_type == "consolidated_tasks":
        required_fields = ['task_id', 'task_text', 'frequency', 'source_jobs']
        for task in data:
            missing = [f for f in required_fields if f not in task]
            if missing:
                raise ValueError(f"Task missing fields: {missing}")

    elif schema_type == "clustered_tasks":
        # Validate theme structure
        expected_themes = {'threat_detection', 'incident_response', ...}  # All 10 themes
        if not all(theme in data for theme in expected_themes):
            raise ValueError("Missing expected themes")

    return True
```

### Quality Scoring

**Data Quality Dimensions**:
- **Completeness**: All required fields present
- **Consistency**: Data types and formats correct
- **Accuracy**: Values within expected ranges
- **Validity**: References to other data exist

**Quality Score Calculation**:
```python
def calculate_data_quality_score(data, schema_type):
    """Calculate overall data quality score"""

    scores = {
        'completeness': check_completeness(data),
        'consistency': check_consistency(data),
        'accuracy': check_accuracy(data),
        'validity': check_validity(data)
    }

    # Weighted average
    weights = {'completeness': 0.4, 'consistency': 0.3, 'accuracy': 0.2, 'validity': 0.1}
    overall_score = sum(scores[metric] * weights[metric] for metric in scores)

    return overall_score, scores
```

## File Organization

### Processed Data Directory Structure

```
data/processed/
├── soc_jobs_flattened_*.csv          # Classification outputs
├── task_lexicon/                     # Aggregation and clustering results
│   ├── consolidated_tasks.json       # Deduplicated task lexicon
│   ├── task_frequency_report.json    # Frequency analysis
│   ├── tasks_with_candidate_themes.json  # Thematic clustering
│   └── clustering_validation.json    # Clustering quality metrics
├── pipeline_logs/                    # Execution tracking
│   ├── pipeline_summary.json         # Complete execution summary
│   └── stage_logs/                   # Individual stage logs
└── archives/                         # Historical processed data
```

### Naming Conventions

**File Naming Patterns**:
- **Classification CSVs**: `soc_jobs_flattened_{timestamp}_soc_tier1_analysis.csv`
- **Task Lexicon**: `consolidated_tasks.json`
- **Reports**: `{report_type}_report.json` or `{analysis_type}_validation.json`
- **Summaries**: `pipeline_summary.json`

**Timestamp Format**: `YYYYMMDD_HHMMSS` (e.g., `20241201_120000`)

## Version Control and Provenance

### Data Lineage Tracking

**Provenance Metadata**:
```json
{
  "data_lineage": {
    "source_files": ["raw/serpapi/2024-Q4/run_001/jobs_20241201_120000.json"],
    "processing_stages": [
      {
        "stage": "classification",
        "script": "data_analyzer.py",
        "version": "1.0.0",
        "timestamp": "2024-12-01T12:00:15Z",
        "parameters": {"rules_file": "configs/rules.json"}
      },
      {
        "stage": "aggregation",
        "script": "task_aggregator.py",
        "version": "1.0.0",
        "timestamp": "2024-12-01T12:00:25Z",
        "parameters": {"similarity_threshold": 0.88}
      }
    ],
    "data_quality_scores": {
      "raw_data": 0.96,
      "processed_data": 0.89,
      "final_output": 0.85
    }
  }
}
```

### Change Tracking

**Version Metadata**:
- **Schema Version**: Tracks structural changes
- **Processing Version**: Links to code versions
- **Data Version**: Identifies dataset generations
- **Quality Version**: Associates with validation runs

## Integration Schemas

### LLM Input Format

**Prepared for Language Models**:
```json
{
  "themes": [
    {
      "name": "threat_detection",
      "description": "Tasks related to identifying and monitoring security threats",
      "tasks": [
        {
          "text": "Monitor security alerts and investigate potential threats",
          "confidence": 0.92,
          "frequency": 28
        }
      ],
      "summary_stats": {
        "total_tasks": 45,
        "high_confidence_tasks": 38,
        "average_frequency": 12.5
      }
    }
  ],
  "metadata": {
    "total_themes": 10,
    "total_tasks": 241,
    "processing_date": "2024-12-01",
    "quality_score": 0.85
  }
}
```

### Research Export Format

**Academic Research Format**:
```json
{
  "dataset_info": {
    "name": "SOC Job Task Analysis Dataset",
    "version": "1.0.0",
    "creation_date": "2024-12-01",
    "data_period": "2024-Q1 to 2024-Q4",
    "total_jobs_analyzed": 1250,
    "unique_tasks_identified": 291
  },
  "task_lexicon": [...],
  "thematic_analysis": {...},
  "methodology": {
    "data_collection": "SerpAPI Google Jobs",
    "classification": "Rule-based SOC filtering",
    "deduplication": "Fuzzy string matching (88% threshold)",
    "clustering": "Keyword-based thematic grouping"
  }
}
```

This schema documentation ensures consistent data processing, validation, and integration across all pipeline stages, supporting reliable research workflows and LLM applications.

---

**Last Updated:** December 2024
**Version:** 1.0.0
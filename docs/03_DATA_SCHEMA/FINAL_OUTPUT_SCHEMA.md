# Final Output Schema Reference

## Overview

This document defines the structure and format of final outputs from the SOC Job Task Analyzer pipeline. These schemas are optimized for LLM integration, research analysis, and academic presentation, providing structured, validated data ready for advanced computational analysis.

## LLM-Ready Data Formats

### Thematic Task Clusters

**File Location**: `data/processed/task_lexicon/tasks_with_candidate_themes.json`

**Purpose**: Structured input for large language models to perform semantic analysis, theme validation, and advanced task categorization.

**JSON Structure**:
```json
{
  "threat_detection": [
    {
      "task_id": "task_001",
      "task_text": "Monitor security alerts and investigate potential threats",
      "confidence": 0.92,
      "keywords_matched": ["monitor", "alert", "threat"],
      "frequency": 28,
      "source_jobs": 25,
      "temporal_distribution": {
        "2024-Q1": 5,
        "2024-Q2": 8,
        "2024-Q3": 10,
        "2024-Q4": 5
      },
      "llm_analysis_ready": true
    }
  ],
  "incident_response": [...],
  "unassigned": [...]
}
```

**LLM Integration Fields**:

| Field | Type | Purpose | Example |
|-------|------|---------|---------|
| `task_id` | string | Unique identifier for traceability | `"task_001"` |
| `task_text` | string | Clean task description for analysis | `"Monitor security alerts..."` |
| `confidence` | float | Keyword matching confidence (0.0-1.0) | `0.92` |
| `keywords_matched` | array | Matched thematic keywords | `["monitor", "alert"]` |
| `frequency` | integer | Occurrence count across jobs | `28` |
| `source_jobs` | integer | Number of unique jobs | `25` |
| `temporal_distribution` | object | Quarterly frequency breakdown | `{"2024-Q1": 5, ...}` |
| `llm_analysis_ready` | boolean | Validation flag for LLM processing | `true` |

### Consolidated Task Lexicon

**File Location**: `data/processed/task_lexicon/consolidated_tasks.json`

**Purpose**: Complete task repository with deduplication metadata for comprehensive analysis.

**JSON Structure**:
```json
[
  {
    "task_id": "task_001",
    "task_text": "Monitor security alerts and investigate potential threats",
    "frequency": 28,
    "source_jobs": ["job_123", "job_456", "job_789"],
    "first_seen": "2024-01-15T00:00:00Z",
    "last_seen": "2024-12-01T00:00:00Z",
    "source_files": ["202401.csv", "202402.csv"],
    "confidence_score": 0.95,
    "cluster_size": 12,
    "semantic_metadata": {
      "primary_action": "monitor",
      "target": "security_alerts",
      "outcome": "investigation",
      "complexity_score": 0.7
    }
  }
]
```

## Research Analysis Formats

### Task Frequency Analysis

**File Location**: `data/processed/task_lexicon/task_frequency_report.json`

**Purpose**: Statistical analysis of task prevalence for research insights and curriculum development.

**JSON Structure**:
```json
{
  "summary_statistics": {
    "total_raw_tasks": 1059,
    "unique_tasks": 291,
    "deduplication_rate": 0.725,
    "average_frequency": 3.6,
    "max_frequency": 28,
    "date_range": {
      "earliest": "2024-01-01",
      "latest": "2024-12-01"
    }
  },
  "frequency_distribution": {
    "singleton_tasks": 45,
    "low_frequency_2_5": 156,
    "medium_frequency_6_10": 68,
    "high_frequency_11_plus": 22
  },
  "top_tasks_by_frequency": [
    {
      "rank": 1,
      "task_text": "Monitor security alerts and investigate potential threats",
      "frequency": 28,
      "percentage_of_total": 2.64,
      "trend": "stable"
    }
  ],
  "temporal_patterns": {
    "tasks_by_quarter": {
      "2024-Q1": {"total_tasks": 145, "new_tasks": 89},
      "2024-Q2": {"total_tasks": 167, "new_tasks": 34},
      "2024-Q3": {"total_tasks": 189, "new_tasks": 22},
      "2024-Q4": {"total_tasks": 198, "new_tasks": 9}
    },
    "emerging_trends": [
      {
        "task_pattern": "AI-powered threat detection",
        "first_appearance": "2024-Q3",
        "growth_rate": 0.45
      }
    ]
  }
}
```

### Thematic Clustering Validation

**File Location**: `data/processed/task_lexicon/clustering_validation.json`

**Purpose**: Quality metrics and validation data for clustering methodology assessment.

**JSON Structure**:
```json
{
  "clustering_performance": {
    "total_tasks_processed": 291,
    "tasks_successfully_clustered": 241,
    "clustering_coverage": 0.828,
    "average_confidence_score": 0.76,
    "unassigned_tasks": 50
  },
  "theme_distribution_analysis": {
    "theme_sizes": {
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
    "distribution_metrics": {
      "balance_score": 0.72,
      "entropy": 2.15,
      "gini_coefficient": 0.18
    }
  },
  "confidence_analysis": {
    "confidence_bands": {
      "very_high_0.9_1.0": 189,
      "high_0.8_0.9": 32,
      "medium_0.6_0.8": 15,
      "low_0.3_0.6": 5,
      "very_low_0_0.3": 0
    },
    "confidence_trends": {
      "threat_detection": {"average": 0.87, "std_dev": 0.08},
      "compliance_reporting": {"average": 0.65, "std_dev": 0.12}
    }
  },
  "quality_assessment": {
    "keyword_match_accuracy": 0.91,
    "semantic_coherence_score": 0.84,
    "manual_validation_sample": [
      {
        "task_id": "task_001",
        "assigned_theme": "threat_detection",
        "manual_assessment": "correct",
        "confidence_alignment": "good"
      }
    ]
  }
}
```

## Pipeline Execution Records

### Comprehensive Pipeline Summary

**File Location**: `data/processed/pipeline_summary.json`

**Purpose**: Complete execution audit trail for reproducibility and performance analysis.

**JSON Structure**:
```json
{
  "execution_metadata": {
    "pipeline_version": "1.0.0",
    "execution_id": "exec_20241201_120000",
    "start_timestamp": "2024-12-01T12:00:00Z",
    "end_timestamp": "2024-12-01T12:01:09Z",
    "total_duration_seconds": 69.4,
    "execution_status": "completed",
    "environment": {
      "python_version": "3.11.0",
      "platform": "Windows-10-10.0.19045-SP0",
      "working_directory": "C:\\Core_Workspace\\02_Projects\\SOC-Job-Task-Analyzer"
    }
  },
  "stage_execution_details": [
    {
      "stage_name": "data_collection",
      "stage_version": "1.0.0",
      "start_time": "2024-12-01T12:00:00Z",
      "duration_seconds": 45.2,
      "status": "completed",
      "performance_metrics": {
        "cpu_usage_percent": 15.2,
        "memory_peak_mb": 145,
        "api_calls_made": 3,
        "data_processed_mb": 2.3
      },
      "output_metrics": {
        "jobs_collected": 45,
        "responsibilities_extracted": 128,
        "data_quality_score": 0.96
      },
      "error_log": []
    },
    {
      "stage_name": "job_classification",
      "stage_version": "1.0.0",
      "start_time": "2024-12-01T12:00:45Z",
      "duration_seconds": 12.3,
      "status": "completed",
      "performance_metrics": {
        "cpu_usage_percent": 8.7,
        "memory_peak_mb": 89,
        "rules_processed": 15,
        "jobs_filtered": 10
      },
      "output_metrics": {
        "jobs_processed": 45,
        "soc_jobs_identified": 35,
        "classification_accuracy": 0.956
      }
    },
    {
      "stage_name": "task_aggregation",
      "stage_version": "1.0.0",
      "start_time": "2024-12-01T12:00:57Z",
      "duration_seconds": 8.7,
      "status": "completed",
      "performance_metrics": {
        "similarity_computations": 543391,
        "memory_peak_mb": 156,
        "clusters_created": 291
      },
      "output_metrics": {
        "raw_tasks_input": 1059,
        "unique_tasks_output": 291,
        "deduplication_efficiency": 0.725
      }
    },
    {
      "stage_name": "thematic_clustering",
      "stage_version": "1.0.0",
      "start_time": "2024-12-01T12:01:06Z",
      "duration_seconds": 3.2,
      "status": "completed",
      "performance_metrics": {
        "keyword_matches_attempted": 8730,
        "themes_evaluated": 2910,
        "memory_peak_mb": 78
      },
      "output_metrics": {
        "tasks_clustered": 241,
        "clustering_coverage": 0.828,
        "average_theme_confidence": 0.76
      }
    }
  ],
  "data_quality_assessment": {
    "overall_data_quality_score": 0.89,
    "stage_quality_scores": {
      "data_collection": 0.96,
      "job_classification": 0.94,
      "task_aggregation": 0.91,
      "thematic_clustering": 0.87
    },
    "data_integrity_checks": {
      "schema_validation": "passed",
      "reference_integrity": "passed",
      "temporal_consistency": "passed"
    }
  },
  "output_file_inventory": [
    {
      "file_path": "data/processed/soc_jobs_flattened_20241201_120000_soc_tier1_analysis.csv",
      "file_size_bytes": 245760,
      "record_count": 128,
      "creation_timestamp": "2024-12-01T12:00:57Z",
      "data_integrity_hash": "a1b2c3d4..."
    },
    {
      "file_path": "data/processed/task_lexicon/consolidated_tasks.json",
      "file_size_bytes": 184320,
      "record_count": 291,
      "creation_timestamp": "2024-12-01T12:01:06Z",
      "data_integrity_hash": "e5f6g7h8..."
    }
  ],
  "reproducibility_info": {
    "git_commit_hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "dependency_versions": {
      "pandas": "2.1.3",
      "difflib": "built-in",
      "python-dotenv": "1.0.0"
    },
    "configuration_files": {
      "rules.json": "hash_abc123",
      "pipeline_config.json": "hash_def456"
    },
    "random_seed_used": null
  }
}
```

## Specialized Export Formats

### Academic Research Dataset

**Purpose**: Structured dataset for PhD research, publications, and academic presentations.

**JSON Structure**:
```json
{
  "dataset_metadata": {
    "title": "SOC Job Task Analysis Dataset v1.0.0",
    "description": "Comprehensive analysis of SOC job requirements from Google Jobs API",
    "creation_date": "2024-12-01",
    "data_collection_period": "2024-Q1 to 2024-Q4",
    "total_jobs_analyzed": 1250,
    "unique_tasks_identified": 291,
    "research_institution": "University Name",
    "researcher": "Dr. Researcher Name",
    "publication_doi": "10.1234/dataset.doi",
    "license": "CC-BY-4.0"
  },
  "methodology_documentation": {
    "data_collection_method": "SerpAPI Google Jobs API integration",
    "classification_approach": "Rule-based SOC role identification",
    "deduplication_algorithm": "Fuzzy string matching with 88% similarity threshold",
    "thematic_clustering": "Keyword-based grouping with confidence scoring",
    "quality_assurance": "Multi-stage validation with manual review sampling",
    "reproducibility_measures": "Version-controlled code, dependency pinning, execution logging"
  },
  "data_files": {
    "task_lexicon": "consolidated_tasks.json",
    "thematic_clusters": "tasks_with_candidate_themes.json",
    "frequency_analysis": "task_frequency_report.json",
    "clustering_validation": "clustering_validation.json",
    "pipeline_audit": "pipeline_summary.json"
  },
  "codebook": {
    "variables_explanation": {
      "task_id": "Unique identifier for each consolidated task",
      "task_text": "Normalized task description",
      "frequency": "Number of job postings containing this task",
      "confidence_score": "Deduplication confidence (0.0-1.0)",
      "theme": "Assigned functional category",
      "theme_confidence": "Clustering confidence score"
    },
    "thematic_categories": {
      "threat_detection": "Tasks related to identifying and monitoring security threats",
      "incident_response": "Tasks involving response to security incidents",
      "log_analysis": "Tasks focused on log review and correlation",
      "security_monitoring": "Continuous security surveillance activities",
      "vulnerability_management": "Vulnerability assessment and remediation",
      "threat_hunting": "Proactive threat discovery activities",
      "forensic_analysis": "Digital forensic investigation tasks",
      "compliance_reporting": "Regulatory compliance and reporting",
      "tool_configuration": "Security tool setup and maintenance",
      "communication": "Stakeholder communication and coordination"
    }
  },
  "usage_guidelines": {
    "intended_use": "Academic research, curriculum development, industry analysis",
    "citation_requirements": "Please cite the dataset DOI in all publications",
    "contact_information": "researcher@university.edu",
    "update_policy": "Quarterly updates with new job data",
    "data_limitations": "Limited to English-language SOC positions from Google Jobs"
  }
}
```

### Visualization-Ready Format

**Purpose**: Pre-processed data for charts, graphs, and interactive dashboards.

**JSON Structure**:
```json
{
  "visualization_data": {
    "theme_distribution_chart": {
      "type": "bar_chart",
      "title": "SOC Tasks by Functional Theme",
      "data": [
        {"theme": "threat_detection", "task_count": 45, "percentage": 18.7},
        {"theme": "incident_response", "task_count": 38, "percentage": 15.8}
      ],
      "metadata": {
        "total_tasks": 241,
        "unassigned_tasks": 50,
        "last_updated": "2024-12-01"
      }
    },
    "frequency_distribution_chart": {
      "type": "histogram",
      "title": "Task Frequency Distribution",
      "bins": ["1", "2-5", "6-10", "11+"],
      "values": [45, 156, 68, 22],
      "metadata": {
        "total_unique_tasks": 291,
        "average_frequency": 3.6
      }
    },
    "temporal_trends_chart": {
      "type": "line_chart",
      "title": "Task Emergence Over Time",
      "time_series": {
        "2024-Q1": {"total_tasks": 145, "new_tasks": 89},
        "2024-Q2": {"total_tasks": 167, "new_tasks": 34}
      }
    },
    "confidence_heatmap": {
      "type": "heatmap",
      "title": "Theme-Task Confidence Matrix",
      "matrix": {
        "threat_detection": {"high": 38, "medium": 7, "low": 0},
        "incident_response": {"high": 32, "medium": 5, "low": 1}
      }
    }
  },
  "dashboard_metadata": {
    "generated_at": "2024-12-01T12:01:09Z",
    "data_freshness": "real-time",
    "interactive_features": ["theme_filtering", "temporal_zoom", "confidence_thresholding"],
    "export_formats": ["PNG", "SVG", "PDF", "JSON"]
  }
}
```

## Data Validation and Integrity

### Schema Validation Rules

**Automated Validation**:
```python
def validate_final_output_schemas(data, output_type):
    """Validate final output against schema requirements"""

    schema_validators = {
        'llm_ready_clusters': validate_clustered_tasks_schema,
        'research_dataset': validate_academic_dataset_schema,
        'pipeline_summary': validate_execution_summary_schema,
        'visualization_data': validate_dashboard_data_schema
    }

    if output_type not in schema_validators:
        raise ValueError(f"Unknown output type: {output_type}")

    validator = schema_validators[output_type]
    return validator(data)
```

### Data Integrity Checks

**Hash-Based Verification**:
```python
def generate_data_integrity_hashes(outputs):
    """Generate cryptographic hashes for data integrity verification"""

    integrity_hashes = {}

    for output_file, data in outputs.items():
        # Create deterministic JSON representation
        canonical_json = json.dumps(data, sort_keys=True, separators=(',', ':'))

        # Generate SHA-256 hash
        import hashlib
        file_hash = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

        integrity_hashes[output_file] = {
            'sha256_hash': file_hash,
            'file_size_bytes': len(canonical_json),
            'record_count': len(data) if isinstance(data, list) else sum(len(v) for v in data.values()) if isinstance(data, dict) else 1,
            'generation_timestamp': datetime.now().isoformat()
        }

    return integrity_hashes
```

### Quality Assurance Metadata

**Comprehensive Quality Report**:
```json
{
  "quality_assurance_summary": {
    "overall_quality_score": 0.89,
    "validation_timestamp": "2024-12-01T12:01:10Z",
    "validation_checks_performed": 15,
    "checks_passed": 14,
    "checks_failed": 1,
    "critical_issues": 0,
    "warnings": 1
  },
  "detailed_validation_results": [
    {
      "check_name": "schema_compliance",
      "status": "passed",
      "details": "All output files conform to defined schemas"
    },
    {
      "check_name": "data_integrity",
      "status": "passed",
      "details": "Cryptographic hashes match expected values"
    },
    {
      "check_name": "reference_integrity",
      "status": "warning",
      "details": "2 task references could not be resolved"
    }
  ],
  "recommendations": [
    "Review unresolved task references in clustering output",
    "Consider regenerating data with updated job sources"
  ]
}
```

This schema documentation ensures that final outputs are structured, validated, and optimized for their intended research and analytical purposes, supporting reproducible academic workflows and advanced computational analysis.

---

**Last Updated:** December 2024
**Version:** 1.0.0
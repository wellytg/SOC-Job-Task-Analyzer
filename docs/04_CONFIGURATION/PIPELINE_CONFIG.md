# Pipeline Configuration Guide

## Overview

The SOC Job Task Analyzer pipeline is highly configurable, allowing researchers and practitioners to customize data collection, processing, and analysis parameters. This document details all configuration options and their impact on pipeline behavior.

## Configuration Architecture

### Configuration Hierarchy

**Primary Configuration Files**:

1. **Pipeline Config**: `configs/pipeline_config.json` - Core pipeline settings
2. **Rules Config**: `configs/rules.json` - Classification rules (detailed in RULES_ENGINE.md)
3. **Environment Variables**: `.env` file - API keys and secrets
4. **Runtime Parameters**: Command-line arguments - Execution-time overrides

**Configuration Loading Priority** (highest to lowest):
1. Command-line arguments
2. Environment variables
3. Pipeline config file
4. Default values

### Pipeline Configuration Schema

**File Location**: `configs/pipeline_config.json`

**Complete Schema**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "pipeline": {
      "type": "object",
      "properties": {
        "version": {
          "type": "string",
          "description": "Pipeline version for reproducibility"
        },
        "name": {
          "type": "string",
          "description": "Human-readable pipeline name"
        },
        "description": {
          "type": "string",
          "description": "Pipeline purpose and scope description"
        },
        "stages": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["data_collection", "job_classification", "task_aggregation", "thematic_clustering"]
          },
          "description": "Pipeline stages to execute"
        },
        "fail_fast": {
          "type": "boolean",
          "default": true,
          "description": "Stop pipeline on first stage failure"
        },
        "continue_on_error": {
          "type": "boolean",
          "default": false,
          "description": "Continue processing despite non-critical errors"
        }
      },
      "required": ["version", "stages"]
    },
    "data_collection": {
      "type": "object",
      "properties": {
        "api_provider": {
          "type": "string",
          "enum": ["serpapi", "google_jobs_api", "mock"],
          "default": "serpapi",
          "description": "Job data source provider"
        },
        "search_queries": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "query": {"type": "string"},
              "location": {"type": "string", "default": "United States"},
              "max_results": {"type": "integer", "minimum": 1, "maximum": 100, "default": 50}
            },
            "required": ["query"]
          },
          "description": "Search queries for job data collection"
        },
        "rate_limiting": {
          "type": "object",
          "properties": {
            "requests_per_minute": {"type": "integer", "minimum": 1, "default": 30},
            "burst_limit": {"type": "integer", "minimum": 1, "default": 10},
            "backoff_multiplier": {"type": "number", "minimum": 1.0, "default": 2.0}
          }
        },
        "data_quality_filters": {
          "type": "object",
          "properties": {
            "min_description_length": {"type": "integer", "minimum": 50, "default": 100},
            "require_responsibilities": {"type": "boolean", "default": true},
            "exclude_no_salary": {"type": "boolean", "default": false},
            "max_age_days": {"type": "integer", "minimum": 1, "default": 30}
          }
        }
      }
    },
    "job_classification": {
      "type": "object",
      "properties": {
        "rules_file": {
          "type": "string",
          "default": "configs/rules.json",
          "description": "Path to classification rules file"
        },
        "classification_threshold": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0,
          "default": 0.7,
          "description": "Minimum confidence for job classification"
        },
        "output_format": {
          "type": "string",
          "enum": ["csv", "json", "both"],
          "default": "both",
          "description": "Classification output format"
        },
        "include_unclassified": {
          "type": "boolean",
          "default": true,
          "description": "Include unclassified jobs in output"
        }
      }
    },
    "task_aggregation": {
      "type": "object",
      "properties": {
        "deduplication_method": {
          "type": "string",
          "enum": ["fuzzy", "exact", "semantic"],
          "default": "fuzzy",
          "description": "Task deduplication approach"
        },
        "similarity_threshold": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0,
          "default": 0.88,
          "description": "Similarity threshold for fuzzy matching"
        },
        "clustering_algorithm": {
          "type": "string",
          "enum": ["single_linkage", "complete_linkage", "average_linkage"],
          "default": "average_linkage",
          "description": "Hierarchical clustering method"
        },
        "max_cluster_size": {
          "type": "integer",
          "minimum": 2,
          "default": 10,
          "description": "Maximum tasks per cluster"
        },
        "processing_batch_size": {
          "type": "integer",
          "minimum": 100,
          "maximum": 10000,
          "default": 1000,
          "description": "Batch size for similarity computation"
        }
      }
    },
    "thematic_clustering": {
      "type": "object",
      "properties": {
        "themes_file": {
          "type": "string",
          "default": "configs/themes.json",
          "description": "Path to thematic categories definition"
        },
        "clustering_method": {
          "type": "string",
          "enum": ["keyword_matching", "semantic_similarity", "hybrid"],
          "default": "keyword_matching",
          "description": "Thematic clustering approach"
        },
        "confidence_threshold": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0,
          "default": 0.6,
          "description": "Minimum confidence for theme assignment"
        },
        "allow_multiple_themes": {
          "type": "boolean",
          "default": false,
          "description": "Allow tasks to belong to multiple themes"
        },
        "unassigned_handling": {
          "type": "string",
          "enum": ["separate_category", "discard", "manual_review"],
          "default": "separate_category",
          "description": "How to handle unassigned tasks"
        }
      }
    },
    "output": {
      "type": "object",
      "properties": {
        "base_directory": {
          "type": "string",
          "default": "data/processed",
          "description": "Base directory for output files"
        },
        "timestamp_format": {
          "type": "string",
          "default": "%Y%m%d_%H%M%S",
          "description": "Timestamp format for file naming"
        },
        "compression": {
          "type": "string",
          "enum": ["none", "gzip", "bz2", "xz"],
          "default": "none",
          "description": "Output file compression"
        },
        "file_format": {
          "type": "object",
          "properties": {
            "csv_delimiter": {"type": "string", "default": ","},
            "json_indent": {"type": "integer", "minimum": 0, "default": 2},
            "include_metadata": {"type": "boolean", "default": true}
          }
        }
      }
    },
    "performance": {
      "type": "object",
      "properties": {
        "parallel_processing": {
          "type": "boolean",
          "default": true,
          "description": "Enable parallel processing where possible"
        },
        "max_workers": {
          "type": "integer",
          "minimum": 1,
          "default": 4,
          "description": "Maximum number of worker processes"
        },
        "memory_limit_mb": {
          "type": "integer",
          "minimum": 512,
          "default": 2048,
          "description": "Memory limit per process"
        },
        "timeout_seconds": {
          "type": "integer",
          "minimum": 60,
          "default": 3600,
          "description": "Maximum execution time per stage"
        }
      }
    },
    "logging": {
      "type": "object",
      "properties": {
        "level": {
          "type": "string",
          "enum": ["DEBUG", "INFO", "WARNING", "ERROR"],
          "default": "INFO",
          "description": "Logging verbosity level"
        },
        "format": {
          "type": "string",
          "default": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
          "description": "Log message format"
        },
        "file_logging": {
          "type": "boolean",
          "default": true,
          "description": "Enable file logging"
        },
        "console_logging": {
          "type": "boolean",
          "default": true,
          "description": "Enable console logging"
        },
        "log_directory": {
          "type": "string",
          "default": "logs",
          "description": "Directory for log files"
        }
      }
    },
    "monitoring": {
      "type": "object",
      "properties": {
        "enable_metrics": {
          "type": "boolean",
          "default": true,
          "description": "Enable performance metrics collection"
        },
        "metrics_interval_seconds": {
          "type": "integer",
          "minimum": 10,
          "default": 60,
          "description": "Metrics collection interval"
        },
        "alerts": {
          "type": "object",
          "properties": {
            "enable_email_alerts": {"type": "boolean", "default": false},
            "alert_email": {"type": "string", "format": "email"},
            "alert_on_failure": {"type": "boolean", "default": true},
            "alert_on_performance_degradation": {"type": "boolean", "default": true}
          }
        }
      }
    }
  },
  "required": ["pipeline"]
}
```

## Current Configuration

### Default Pipeline Configuration

**File**: `configs/pipeline_config.json`

```json
{
  "pipeline": {
    "version": "1.0.0",
    "name": "SOC Job Task Analyzer",
    "description": "Comprehensive analysis of SOC job requirements and task patterns",
    "stages": [
      "data_collection",
      "job_classification",
      "task_aggregation",
      "thematic_clustering"
    ],
    "fail_fast": true,
    "continue_on_error": false
  },
  "data_collection": {
    "api_provider": "serpapi",
    "search_queries": [
      {
        "query": "SOC Analyst",
        "location": "United States",
        "max_results": 50
      },
      {
        "query": "Security Operations Center Analyst",
        "location": "United States",
        "max_results": 50
      },
      {
        "query": "Cybersecurity Analyst SOC",
        "location": "United States",
        "max_results": 50
      }
    ],
    "rate_limiting": {
      "requests_per_minute": 30,
      "burst_limit": 10,
      "backoff_multiplier": 2.0
    },
    "data_quality_filters": {
      "min_description_length": 100,
      "require_responsibilities": true,
      "exclude_no_salary": false,
      "max_age_days": 30
    }
  },
  "job_classification": {
    "rules_file": "configs/rules.json",
    "classification_threshold": 0.7,
    "output_format": "both",
    "include_unclassified": true
  },
  "task_aggregation": {
    "deduplication_method": "fuzzy",
    "similarity_threshold": 0.88,
    "clustering_algorithm": "average_linkage",
    "max_cluster_size": 10,
    "processing_batch_size": 1000
  },
  "thematic_clustering": {
    "themes_file": "configs/themes.json",
    "clustering_method": "keyword_matching",
    "confidence_threshold": 0.6,
    "allow_multiple_themes": false,
    "unassigned_handling": "separate_category"
  },
  "output": {
    "base_directory": "data/processed",
    "timestamp_format": "%Y%m%d_%H%M%S",
    "compression": "none",
    "file_format": {
      "csv_delimiter": ",",
      "json_indent": 2,
      "include_metadata": true
    }
  },
  "performance": {
    "parallel_processing": true,
    "max_workers": 4,
    "memory_limit_mb": 2048,
    "timeout_seconds": 3600
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file_logging": true,
    "console_logging": true,
    "log_directory": "logs"
  },
  "monitoring": {
    "enable_metrics": true,
    "metrics_interval_seconds": 60,
    "alerts": {
      "enable_email_alerts": false,
      "alert_on_failure": true,
      "alert_on_performance_degradation": true
    }
  }
}
```

## Environment Variables

### Required Environment Variables

**File**: `.env`

```bash
# API Keys
SERPAPI_KEY=your_serpapi_key_here

# Optional: Database Configuration (for future extensions)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=soc_jobs
DB_USER=analyst
DB_PASSWORD=secure_password

# Optional: External Service URLs
REDIS_URL=redis://localhost:6379
METRICS_URL=http://localhost:9090

# Optional: Email Configuration for Alerts
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
ALERT_EMAIL_RECIPIENT=admin@organization.com
```

### Environment Variable Loading

**Code Example**:
```python
from dotenv import load_dotenv
import os

def load_environment_config():
    """Load configuration from environment variables"""

    load_dotenv()  # Load .env file

    config = {
        'api_keys': {
            'serpapi': os.getenv('SERPAPI_KEY'),
        },
        'database': {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'name': os.getenv('DB_NAME', 'soc_jobs'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
        },
        'services': {
            'redis_url': os.getenv('REDIS_URL'),
            'metrics_url': os.getenv('METRICS_URL'),
        },
        'alerts': {
            'smtp_server': os.getenv('SMTP_SERVER'),
            'smtp_port': int(os.getenv('SMTP_PORT', 587)),
            'smtp_username': os.getenv('SMTP_USERNAME'),
            'smtp_password': os.getenv('SMTP_PASSWORD'),
            'alert_email': os.getenv('ALERT_EMAIL_RECIPIENT'),
        }
    }

    # Validate required variables
    if not config['api_keys']['serpapi']:
        raise ValueError("SERPAPI_KEY environment variable is required")

    return config
```

## Command-Line Configuration

### Pipeline Execution Options

**Basic Usage**:
```bash
# Run full pipeline with default config
python src/job_run.py

# Run specific stages only
python src/job_run.py --stages data_collection job_classification

# Override configuration values
python src/job_run.py --config.classification_threshold 0.8 --config.max_workers 8

# Use custom config file
python src/job_run.py --config-file configs/custom_config.json
```

### Command-Line Arguments Schema

**Available Options**:
```python
import argparse

def parse_arguments():
    """Parse command-line arguments for pipeline configuration"""

    parser = argparse.ArgumentParser(description='SOC Job Task Analyzer Pipeline')

    # Configuration files
    parser.add_argument('--config-file', type=str, default='configs/pipeline_config.json',
                       help='Path to pipeline configuration file')
    parser.add_argument('--rules-file', type=str, default='configs/rules.json',
                       help='Path to classification rules file')
    parser.add_argument('--env-file', type=str, default='.env',
                       help='Path to environment variables file')

    # Stage control
    parser.add_argument('--stages', nargs='+',
                       choices=['data_collection', 'job_classification', 'task_aggregation', 'thematic_clustering'],
                       help='Pipeline stages to execute')
    parser.add_argument('--skip-stages', nargs='+',
                       choices=['data_collection', 'job_classification', 'task_aggregation', 'thematic_clustering'],
                       help='Pipeline stages to skip')

    # Runtime overrides
    parser.add_argument('--max-results', type=int,
                       help='Maximum results per search query')
    parser.add_argument('--similarity-threshold', type=float,
                       help='Task deduplication similarity threshold')
    parser.add_argument('--classification-threshold', type=float,
                       help='Job classification confidence threshold')
    parser.add_argument('--max-workers', type=int,
                       help='Maximum number of worker processes')

    # Output control
    parser.add_argument('--output-dir', type=str,
                       help='Base output directory')
    parser.add_argument('--no-compression', action='store_true',
                       help='Disable output compression')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')

    # Special modes
    parser.add_argument('--dry-run', action='store_true',
                       help='Validate configuration without execution')
    parser.add_argument('--validate-only', action='store_true',
                       help='Validate input data and configuration only')

    return parser.parse_args()
```

## Configuration Validation

### Schema Validation

**Configuration Validator**:
```python
import jsonschema
from jsonschema import validate, ValidationError

def validate_pipeline_config(config):
    """Validate pipeline configuration against schema"""

    schema = {
        # Schema definition from earlier
        # ... (full schema as shown above)
    }

    try:
        validate(instance=config, schema=schema)
        return {'valid': True, 'errors': []}
    except ValidationError as e:
        return {
            'valid': False,
            'errors': [{
                'field': '.'.join(str(x) for x in e.absolute_path),
                'message': e.message,
                'value': e.instance
            }]
        }

def validate_configuration_files():
    """Validate all configuration files"""

    validations = {}

    # Validate pipeline config
    try:
        with open('configs/pipeline_config.json', 'r') as f:
            pipeline_config = json.load(f)
        validations['pipeline_config'] = validate_pipeline_config(pipeline_config)
    except Exception as e:
        validations['pipeline_config'] = {'valid': False, 'errors': [str(e)]}

    # Validate rules config
    try:
        with open('configs/rules.json', 'r') as f:
            rules_config = json.load(f)
        validations['rules_config'] = validate_rules_config(rules_config)
    except Exception as e:
        validations['rules_config'] = {'valid': False, 'errors': [str(e)]}

    # Validate environment
    validations['environment'] = validate_environment_variables()

    return validations
```

### Configuration Testing

**Dry Run Mode**:
```python
def execute_dry_run(config):
    """Execute configuration validation without data processing"""

    print("🔍 SOC Job Task Analyzer - Configuration Dry Run")
    print("=" * 60)

    # Validate configuration
    validations = validate_configuration_files()

    all_valid = all(v['valid'] for v in validations.values())

    if all_valid:
        print("✅ All configurations are valid")
    else:
        print("❌ Configuration validation failed:")
        for config_name, result in validations.items():
            if not result['valid']:
                print(f"  - {config_name}:")
                for error in result['errors']:
                    print(f"    {error}")

    # Simulate pipeline execution
    print("\n📋 Pipeline Execution Simulation:")
    for stage in config['pipeline']['stages']:
        stage_config = config.get(stage, {})
        print(f"  - {stage}: {summarize_stage_config(stage_config)}")

    # Estimate resource requirements
    print("\n💾 Resource Estimation:")
    estimation = estimate_pipeline_resources(config)
    for resource, value in estimation.items():
        print(f"  - {resource}: {value}")

    return all_valid
```

## Advanced Configuration Patterns

### Profile-Based Configuration

**Configuration Profiles**:
```json
{
  "profiles": {
    "development": {
      "data_collection": {
        "search_queries": [
          {"query": "SOC Analyst", "max_results": 10}
        ]
      },
      "performance": {
        "max_workers": 2,
        "memory_limit_mb": 1024
      },
      "logging": {
        "level": "DEBUG"
      }
    },
    "production": {
      "data_collection": {
        "search_queries": [
          {"query": "SOC Analyst", "max_results": 100},
          {"query": "Security Operations Center Analyst", "max_results": 100}
        ]
      },
      "performance": {
        "max_workers": 8,
        "memory_limit_mb": 4096
      },
      "monitoring": {
        "enable_metrics": true,
        "alerts": {
          "enable_email_alerts": true
        }
      }
    },
    "research": {
      "data_collection": {
        "max_age_days": 90
      },
      "task_aggregation": {
        "similarity_threshold": 0.95
      },
      "output": {
        "include_metadata": true,
        "compression": "gzip"
      }
    }
  }
}
```

### Dynamic Configuration Updates

**Runtime Configuration Updates**:
```python
def update_configuration_dynamically(config, updates):
    """Apply dynamic configuration updates"""

    def deep_update(base_dict, update_dict):
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict:
                deep_update(base_dict[key], value)
            else:
                base_dict[key] = value

    # Create configuration copy
    updated_config = copy.deepcopy(config)

    # Apply updates
    deep_update(updated_config, updates)

    # Re-validate configuration
    validation = validate_pipeline_config(updated_config)
    if not validation['valid']:
        raise ValueError(f"Configuration update invalid: {validation['errors']}")

    return updated_config
```

This comprehensive configuration system enables flexible pipeline customization while maintaining validation, reproducibility, and performance optimization for diverse research and operational use cases.

---

**Last Updated:** December 2024
**Version:** 1.0.0
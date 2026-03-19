# Environment Variables Reference

## Overview

Environment variables provide runtime configuration for the SOC Job Task Analyzer, including API credentials, database connections, and operational settings. This document details all supported environment variables and their usage.

## Core API Configuration

### SerpAPI Integration

**SERPAPI_KEY** (Required)
- **Description**: API key for SerpAPI Google Jobs integration
- **Type**: String
- **Default**: None (required)
- **Example**: `SERPAPI_KEY=your_32_character_api_key_here`
- **Security**: Store in `.env` file, never commit to version control
- **Validation**: Must be 32+ characters, alphanumeric

**SERPAPI_TIMEOUT**
- **Description**: Timeout for SerpAPI requests in seconds
- **Type**: Integer
- **Default**: 30
- **Example**: `SERPAPI_TIMEOUT=60`
- **Range**: 10-300 seconds

**SERPAPI_MAX_RETRIES**
- **Description**: Maximum retry attempts for failed API requests
- **Type**: Integer
- **Default**: 3
- **Example**: `SERPAPI_MAX_RETRIES=5`
- **Range**: 0-10 retries

### Alternative Data Sources

**GOOGLE_JOBS_API_KEY**
- **Description**: Google Jobs API key (alternative to SerpAPI)
- **Type**: String
- **Default**: None
- **Example**: `GOOGLE_JOBS_API_KEY=your_google_api_key`
- **Note**: Requires additional configuration for OAuth flow

**MOCK_DATA_MODE**
- **Description**: Enable mock data mode for testing without API calls
- **Type**: Boolean
- **Default**: false
- **Example**: `MOCK_DATA_MODE=true`
- **Usage**: Set to `true` for development/testing

## Database Configuration

### PostgreSQL Database

**DB_HOST**
- **Description**: Database server hostname or IP address
- **Type**: String
- **Default**: localhost
- **Example**: `DB_HOST=db.example.com`

**DB_PORT**
- **Description**: Database server port
- **Type**: Integer
- **Default**: 5432
- **Example**: `DB_PORT=5432`
- **Range**: 1024-65535

**DB_NAME**
- **Description**: Database name for SOC jobs data
- **Type**: String
- **Default**: soc_jobs
- **Example**: `DB_NAME=soc_jobs_prod`

**DB_USER**
- **Description**: Database username
- **Type**: String
- **Default**: analyst
- **Example**: `DB_USER=soc_analyst`

**DB_PASSWORD**
- **Description**: Database password
- **Type**: String
- **Default**: None (required if using database)
- **Example**: `DB_PASSWORD=secure_password_123`
- **Security**: Use strong passwords, consider password managers

**DB_SSL_MODE**
- **Description**: SSL connection mode for database
- **Type**: String
- **Default**: require
- **Options**: disable, allow, prefer, require, verify-ca, verify-full
- **Example**: `DB_SSL_MODE=verify-full`

**DB_CONNECTION_POOL_SIZE**
- **Description**: Maximum number of database connections in pool
- **Type**: Integer
- **Default**: 10
- **Example**: `DB_CONNECTION_POOL_SIZE=20`
- **Range**: 1-100

### Redis Cache (Optional)

**REDIS_URL**
- **Description**: Redis connection URL for caching and session storage
- **Type**: String
- **Default**: None
- **Example**: `REDIS_URL=redis://localhost:6379/0`
- **Format**: redis://[username:password@]host:port/db

**REDIS_TTL_SECONDS**
- **Description**: Default TTL for cached data in seconds
- **Type**: Integer
- **Default**: 3600 (1 hour)
- **Example**: `REDIS_TTL_SECONDS=7200`

## Performance and Resource Management

### Processing Configuration

**MAX_WORKERS**
- **Description**: Maximum number of worker processes for parallel processing
- **Type**: Integer
- **Default**: 4
- **Example**: `MAX_WORKERS=8`
- **Range**: 1-32 (based on CPU cores)

**MEMORY_LIMIT_MB**
- **Description**: Memory limit per worker process in MB
- **Type**: Integer
- **Default**: 2048
- **Example**: `MEMORY_LIMIT_MB=4096`
- **Range**: 512-16384 MB

**BATCH_SIZE**
- **Description**: Processing batch size for large datasets
- **Type**: Integer
- **Default**: 1000
- **Example**: `BATCH_SIZE=5000`
- **Range**: 100-10000

**PIPELINE_TIMEOUT_SECONDS**
- **Description**: Maximum execution time for entire pipeline
- **Type**: Integer
- **Default**: 3600 (1 hour)
- **Example**: `PIPELINE_TIMEOUT_SECONDS=7200`
- **Range**: 300-86400 seconds

### Rate Limiting

**API_RATE_LIMIT_RPM**
- **Description**: API requests per minute limit
- **Type**: Integer
- **Default**: 30
- **Example**: `API_RATE_LIMIT_RPM=60`
- **Note**: Respect API provider limits

**BURST_LIMIT**
- **Description**: Maximum burst requests allowed
- **Type**: Integer
- **Default**: 10
- **Example**: `BURST_LIMIT=20`

## Logging and Monitoring

### Logging Configuration

**LOG_LEVEL**
- **Description**: Logging verbosity level
- **Type**: String
- **Default**: INFO
- **Options**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Example**: `LOG_LEVEL=DEBUG`

**LOG_FORMAT**
- **Description**: Log message format string
- **Type**: String
- **Default**: %(asctime)s - %(name)s - %(levelname)s - %(message)s
- **Example**: `LOG_FORMAT=%(levelname)s:%(name)s:%(message)s`

**LOG_FILE_PATH**
- **Description**: Path for log file output
- **Type**: String
- **Default**: logs/pipeline.log
- **Example**: `LOG_FILE_PATH=/var/log/soc_analyzer.log`

**LOG_MAX_SIZE_MB**
- **Description**: Maximum log file size before rotation
- **Type**: Integer
- **Default**: 100
- **Example**: `LOG_MAX_SIZE_MB=500`
- **Range**: 10-1000 MB

**LOG_BACKUP_COUNT**
- **Description**: Number of backup log files to keep
- **Type**: Integer
- **Default**: 5
- **Example**: `LOG_BACKUP_COUNT=10`
- **Range**: 1-50

### Metrics and Monitoring

**METRICS_ENABLED**
- **Description**: Enable performance metrics collection
- **Type**: Boolean
- **Default**: true
- **Example**: `METRICS_ENABLED=false`

**METRICS_PORT**
- **Description**: Port for metrics HTTP server
- **Type**: Integer
- **Default**: 9090
- **Example**: `METRICS_PORT=8080`
- **Range**: 1024-65535

**METRICS_INTERVAL_SECONDS**
- **Description**: Metrics collection interval
- **Type**: Integer
- **Default**: 60
- **Example**: `METRICS_INTERVAL_SECONDS=30`
- **Range**: 10-3600

## Alerting and Notifications

### Email Alerts

**SMTP_SERVER**
- **Description**: SMTP server hostname
- **Type**: String
- **Default**: None
- **Example**: `SMTP_SERVER=smtp.gmail.com`

**SMTP_PORT**
- **Description**: SMTP server port
- **Type**: Integer
- **Default**: 587
- **Example**: `SMTP_PORT=465`
- **Options**: 587 (TLS), 465 (SSL), 25 (plain)

**SMTP_USERNAME**
- **Description**: SMTP authentication username
- **Type**: String
- **Default**: None
- **Example**: `SMTP_USERNAME=alerts@organization.com`

**SMTP_PASSWORD**
- **Description**: SMTP authentication password
- **Type**: String
- **Default**: None
- **Example**: `SMTP_PASSWORD=app_password_here`
- **Security**: Use app passwords for Gmail, never use main password

**SMTP_USE_TLS**
- **Description**: Enable TLS encryption for SMTP
- **Type**: Boolean
- **Default**: true
- **Example**: `SMTP_USE_TLS=false`

**ALERT_EMAIL_RECIPIENT**
- **Description**: Email address for pipeline alerts
- **Type**: String
- **Default**: None
- **Example**: `ALERT_EMAIL_RECIPIENT=admin@organization.com`

**ALERT_ON_FAILURE**
- **Description**: Send alerts on pipeline failures
- **Type**: Boolean
- **Default**: true
- **Example**: `ALERT_ON_FAILURE=false`

**ALERT_ON_SUCCESS**
- **Description**: Send alerts on successful pipeline completion
- **Type**: Boolean
- **Default**: false
- **Example**: `ALERT_ON_SUCCESS=true`

## Data Quality and Validation

### Data Filtering

**MIN_JOB_DESCRIPTION_LENGTH**
- **Description**: Minimum job description length to process
- **Type**: Integer
- **Default**: 100
- **Example**: `MIN_JOB_DESCRIPTION_LENGTH=200`
- **Range**: 50-1000

**MAX_JOB_AGE_DAYS**
- **Description**: Maximum age of job postings to consider
- **Type**: Integer
- **Default**: 30
- **Example**: `MAX_JOB_AGE_DAYS=90`
- **Range**: 1-365

**EXCLUDE_JOBS_WITHOUT_SALARY**
- **Description**: Skip jobs without salary information
- **Type**: Boolean
- **Default**: false
- **Example**: `EXCLUDE_JOBS_WITHOUT_SALARY=true`

**REQUIRE_RESPONSIBILITIES_SECTION**
- **Description**: Only process jobs with responsibilities section
- **Type**: Boolean
- **Default**: true
- **Example**: `REQUIRE_RESPONSIBILITIES_SECTION=false`

### Quality Thresholds

**CLASSIFICATION_THRESHOLD**
- **Description**: Minimum confidence for job classification
- **Type**: Float
- **Default**: 0.7
- **Example**: `CLASSIFICATION_THRESHOLD=0.8`
- **Range**: 0.0-1.0

**SIMILARITY_THRESHOLD**
- **Description**: Similarity threshold for task deduplication
- **Type**: Float
- **Default**: 0.88
- **Example**: `SIMILARITY_THRESHOLD=0.9`
- **Range**: 0.5-1.0

**THEME_CONFIDENCE_THRESHOLD**
- **Description**: Minimum confidence for theme assignment
- **Type**: Float
- **Default**: 0.6
- **Example**: `THEME_CONFIDENCE_THRESHOLD=0.7`
- **Range**: 0.0-1.0

## Output Configuration

### File Output Settings

**OUTPUT_BASE_DIR**
- **Description**: Base directory for output files
- **Type**: String
- **Default**: data/processed
- **Example**: `OUTPUT_BASE_DIR=/data/soc_analysis`

**OUTPUT_COMPRESSION**
- **Description**: Output file compression format
- **Type**: String
- **Default**: none
- **Options**: none, gzip, bz2, xz
- **Example**: `OUTPUT_COMPRESSION=gzip`

**CSV_DELIMITER**
- **Description**: CSV field delimiter character
- **Type**: String
- **Default**: ,
- **Example**: `CSV_DELIMITER=;`

**JSON_INDENT**
- **Description**: JSON indentation spaces
- **Type**: Integer
- **Default**: 2
- **Example**: `JSON_INDENT=4`
- **Options**: 0 (compact), 2, 4

## Development and Testing

### Development Mode

**DEBUG_MODE**
- **Description**: Enable debug mode with additional logging
- **Type**: Boolean
- **Default**: false
- **Example**: `DEBUG_MODE=true`

**DEVELOPMENT_DATABASE**
- **Description**: Use development database instead of production
- **Type**: Boolean
- **Default**: false
- **Example**: `DEVELOPMENT_DATABASE=true`

**SKIP_VALIDATION**
- **Description**: Skip data validation checks (use with caution)
- **Type**: Boolean
- **Default**: false
- **Example**: `SKIP_VALIDATION=true`

### Testing Configuration

**TEST_DATA_PATH**
- **Description**: Path to test data directory
- **Type**: String
- **Default**: data/test
- **Example**: `TEST_DATA_PATH=test/fixtures`

**MOCK_EXTERNAL_APIS**
- **Description**: Mock all external API calls during testing
- **Type**: Boolean
- **Default**: false
- **Example**: `MOCK_EXTERNAL_APIS=true`

## Security Configuration

### API Security

**API_KEY_ROTATION_DAYS**
- **Description**: Days before API key rotation reminder
- **Type**: Integer
- **Default**: 30
- **Example**: `API_KEY_ROTATION_DAYS=60`

**ENCRYPT_SENSITIVE_DATA**
- **Description**: Encrypt sensitive data in output files
- **Type**: Boolean
- **Default**: false
- **Example**: `ENCRYPT_SENSITIVE_DATA=true`

**ENCRYPTION_KEY**
- **Description**: Encryption key for sensitive data
- **Type**: String
- **Default**: None
- **Example**: `ENCRYPTION_KEY=your_32_byte_key_here`
- **Security**: Generate strong random keys

### Access Control

**ALLOWED_IPS**
- **Description**: Comma-separated list of allowed IP addresses
- **Type**: String
- **Default**: None (allow all)
- **Example**: `ALLOWED_IPS=192.168.1.0/24,10.0.0.1`

**REQUIRE_AUTHENTICATION**
- **Description**: Require authentication for API endpoints
- **Type**: Boolean
- **Default**: false
- **Example**: `REQUIRE_AUTHENTICATION=true`

## Environment File Template

### Complete .env Template

```bash
# Core API Configuration
SERPAPI_KEY=your_serpapi_key_here
SERPAPI_TIMEOUT=30
SERPAPI_MAX_RETRIES=3

# Alternative Data Sources
GOOGLE_JOBS_API_KEY=
MOCK_DATA_MODE=false

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=soc_jobs
DB_USER=analyst
DB_PASSWORD=secure_password_here
DB_SSL_MODE=require
DB_CONNECTION_POOL_SIZE=10

# Redis Cache
REDIS_URL=redis://localhost:6379/0
REDIS_TTL_SECONDS=3600

# Performance Settings
MAX_WORKERS=4
MEMORY_LIMIT_MB=2048
BATCH_SIZE=1000
PIPELINE_TIMEOUT_SECONDS=3600

# Rate Limiting
API_RATE_LIMIT_RPM=30
BURST_LIMIT=10

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_FILE_PATH=logs/pipeline.log
LOG_MAX_SIZE_MB=100
LOG_BACKUP_COUNT=5

# Metrics and Monitoring
METRICS_ENABLED=true
METRICS_PORT=9090
METRICS_INTERVAL_SECONDS=60

# Email Alerts
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=alerts@organization.com
SMTP_PASSWORD=app_password_here
SMTP_USE_TLS=true
ALERT_EMAIL_RECIPIENT=admin@organization.com
ALERT_ON_FAILURE=true
ALERT_ON_SUCCESS=false

# Data Quality Settings
MIN_JOB_DESCRIPTION_LENGTH=100
MAX_JOB_AGE_DAYS=30
EXCLUDE_JOBS_WITHOUT_SALARY=false
REQUIRE_RESPONSIBILITIES_SECTION=true

# Quality Thresholds
CLASSIFICATION_THRESHOLD=0.7
SIMILARITY_THRESHOLD=0.88
THEME_CONFIDENCE_THRESHOLD=0.6

# Output Configuration
OUTPUT_BASE_DIR=data/processed
OUTPUT_COMPRESSION=none
CSV_DELIMITER=,
JSON_INDENT=2

# Development Settings
DEBUG_MODE=false
DEVELOPMENT_DATABASE=false
SKIP_VALIDATION=false

# Testing Configuration
TEST_DATA_PATH=data/test
MOCK_EXTERNAL_APIS=false

# Security Settings
API_KEY_ROTATION_DAYS=30
ENCRYPT_SENSITIVE_DATA=false
ENCRYPTION_KEY=
ALLOWED_IPS=
REQUIRE_AUTHENTICATION=false
```

## Environment Variable Validation

### Validation Script

```python
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

def validate_environment_variables() -> Dict[str, Any]:
    """Validate all environment variables and return validation results"""

    load_dotenv()

    validation_results = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'validated_variables': {}
    }

    # Required variables
    required_vars = {
        'SERPAPI_KEY': {
            'validator': lambda x: len(x) >= 32 and x.replace('_', '').replace('-', '').isalnum(),
            'error_msg': 'SERPAPI_KEY must be at least 32 characters and contain only alphanumeric characters, underscores, and hyphens'
        }
    }

    # Optional variables with validation
    optional_vars = {
        'DB_PASSWORD': {
            'required_if': 'DB_HOST',
            'validator': lambda x: len(x) >= 8,
            'error_msg': 'DB_PASSWORD must be at least 8 characters when database is configured'
        },
        'SMTP_PASSWORD': {
            'required_if': 'SMTP_USERNAME',
            'validator': lambda x: len(x) > 0,
            'error_msg': 'SMTP_PASSWORD is required when SMTP_USERNAME is set'
        },
        'MAX_WORKERS': {
            'validator': lambda x: 1 <= int(x) <= 32,
            'error_msg': 'MAX_WORKERS must be between 1 and 32'
        },
        'MEMORY_LIMIT_MB': {
            'validator': lambda x: 512 <= int(x) <= 16384,
            'error_msg': 'MEMORY_LIMIT_MB must be between 512 and 16384'
        }
    }

    # Validate required variables
    for var_name, config in required_vars.items():
        value = os.getenv(var_name)
        if not value:
            validation_results['errors'].append(f"Required variable {var_name} is not set")
            validation_results['valid'] = False
        elif not config['validator'](value):
            validation_results['errors'].append(config['error_msg'])
            validation_results['valid'] = False
        else:
            validation_results['validated_variables'][var_name] = value

    # Validate optional variables
    for var_name, config in optional_vars.items():
        value = os.getenv(var_name)
        if value:
            # Check conditional requirements
            if 'required_if' in config:
                required_if_var = os.getenv(config['required_if'])
                if required_if_var and not value:
                    validation_results['errors'].append(f"{var_name} is required when {config['required_if']} is set")
                    validation_results['valid'] = False
                    continue

            # Validate value
            try:
                if not config['validator'](value):
                    validation_results['errors'].append(config['error_msg'])
                    validation_results['valid'] = False
                else:
                    validation_results['validated_variables'][var_name] = value
            except (ValueError, TypeError):
                validation_results['errors'].append(f"{var_name} has invalid value: {value}")
                validation_results['valid'] = False

    # Check for deprecated variables
    deprecated_vars = ['OLD_API_KEY', 'LEGACY_DB_CONFIG']
    for var in deprecated_vars:
        if os.getenv(var):
            validation_results['warnings'].append(f"Deprecated variable {var} is set and will be ignored")

    return validation_results

if __name__ == "__main__":
    results = validate_environment_variables()
    print("Environment Variable Validation Results:")
    print(f"Valid: {results['valid']}")
    if results['errors']:
        print("Errors:")
        for error in results['errors']:
            print(f"  - {error}")
    if results['warnings']:
        print("Warnings:")
        for warning in results['warnings']:
            print(f"  - {warning}")
```

This comprehensive environment variable system provides flexible configuration while maintaining security, validation, and operational safety for the SOC Job Task Analyzer pipeline.

---

**Last Updated:** December 2024
**Version:** 1.0.0
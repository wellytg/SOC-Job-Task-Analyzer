# Job Classification Module Reference

## Overview

The job classification module (`data_analyzer.py`) implements intelligent filtering and categorization of cybersecurity job postings. Using a configurable rules engine, it identifies SOC Tier 1 Analyst positions from raw job data and produces structured CSV outputs for downstream task analysis.

## Module Architecture

### Core Components

```python
class SOCJobClassifier:
    def __init__(self, rules_file='configs/rules.json'):
        self.rules = self.load_classification_rules(rules_file)
        self.stats = defaultdict(int)

    def classify_jobs(self, raw_jobs_data):
        """Main classification pipeline"""

    def load_classification_rules(self, rules_file):
        """Load and validate rules configuration"""

    def apply_classification_rules(self, job_data):
        """Apply rules to individual job"""

    def save_classified_data(self, classified_jobs, output_path):
        """Save results in structured format"""
```

### Dependencies

**Required Packages**:
- `pandas`: Data manipulation and CSV operations
- `json`: Rules file parsing
- `re`: Regular expression pattern matching
- `os`: File system operations
- `datetime`: Timestamp handling

**Configuration Files**:
- `configs/rules.json`: Classification rules and criteria

## Rules Engine Design

### Rules File Structure

**Complete Rules Schema** (`configs/rules.json`):
```json
{
  "soc_analyst_tier1": {
    "title_patterns": [
      {
        "type": "contains",
        "value": "soc",
        "case_insensitive": true
      },
      {
        "type": "regex",
        "value": "security operations.?center",
        "case_insensitive": true
      }
    ],
    "exclude_patterns": [
      {
        "type": "contains",
        "value": "senior",
        "case_insensitive": true
      },
      {
        "type": "contains",
        "value": "lead",
        "case_insensitive": true
      }
    ],
    "required_keywords": [
      "monitor",
      "alert",
      "incident",
      "threat"
    ],
    "optional_keywords": [
      "siem",
      "splunk",
      "log",
      "analyze"
    ],
    "company_filters": {
      "exclude_companies": [
        "recruiting",
        "staffing"
      ]
    }
  }
}
```

### Rule Types

**Pattern Matching Rules**:

1. **Contains Rule**:
   ```json
   {
     "type": "contains",
     "value": "soc",
     "case_insensitive": true
   }
   ```

2. **Regex Rule**:
   ```json
   {
     "type": "regex",
     "value": "cyber.?security.*analyst",
     "case_insensitive": true
   }
   ```

3. **Exact Match Rule**:
   ```json
   {
     "type": "exact",
     "value": "SOC Analyst"
   }
   ```

**Keyword Rules**:

- **Required Keywords**: All must be present in job description
- **Optional Keywords**: Bonus points for classification
- **Weighted Keywords**: Different importance levels

### Rule Application Logic

**Multi-Stage Classification**:
```python
def apply_classification_rules(self, job_data):
    # Stage 1: Title pattern matching
    title_score = self.evaluate_title_patterns(job_data['title'])

    # Stage 2: Exclusion pattern check
    if self.check_exclusion_patterns(job_data['title']):
        return False, "excluded_pattern"

    # Stage 3: Required keyword validation
    keyword_score = self.evaluate_keywords(job_data.get('description', ''))

    # Stage 4: Company filtering
    if self.is_excluded_company(job_data.get('company_name', '')):
        return False, "excluded_company"

    # Stage 5: Final scoring
    total_score = title_score + keyword_score
    is_soc_job = total_score >= self.rules['minimum_score']

    return is_soc_job, total_score
```

## Data Processing Pipeline

### Input Data Handling

**Raw Data Loading**:
```python
def load_raw_job_data(self, data_directory):
    """Load most recent job collection"""
    # Find latest run directory
    latest_run = self.find_latest_run(data_directory)

    # Load JSON data
    with open(f"{latest_run}/jobs_*.json", 'r') as f:
        raw_jobs = json.load(f)

    # Validate data structure
    validated_jobs = [job for job in raw_jobs if self.validate_job_structure(job)]

    return validated_jobs
```

**Data Validation**:
```python
def validate_job_structure(self, job_data):
    """Ensure job data has required fields"""
    required_fields = ['title', 'company_name', 'description']
    optional_fields = ['location', 'job_id', 'extensions']

    missing_required = [field for field in required_fields if not job_data.get(field)]

    if missing_required:
        self.logger.warning(f"Job missing required fields: {missing_required}")
        return False

    return True
```

### Text Normalization

**Title Standardization**:
```python
def normalize_job_title(self, title):
    """Standardize job titles for consistent matching"""
    if not title:
        return ""

    # Convert to lowercase
    normalized = title.lower()

    # Remove extra whitespace
    normalized = ' '.join(normalized.split())

    # Handle common abbreviations
    replacements = {
        'jr.': 'junior',
        'sr.': 'senior',
        'asst.': 'assistant',
        'mgr.': 'manager',
        'dir.': 'director'
    }

    for abbr, full in replacements.items():
        normalized = normalized.replace(abbr, full)

    return normalized
```

**Description Cleaning**:
```python
def clean_job_description(self, description):
    """Normalize job description text"""
    if not description:
        return ""

    # Remove HTML tags if present
    import re
    description = re.sub(r'<[^>]+>', '', description)

    # Normalize whitespace
    description = ' '.join(description.split())

    # Convert to lowercase for keyword matching
    return description.lower()
```

## Classification Algorithms

### Title Pattern Matching

**Inclusion Pattern Evaluation**:
```python
def evaluate_title_patterns(self, title):
    """Score title against inclusion patterns"""
    normalized_title = self.normalize_job_title(title)
    score = 0

    for pattern in self.rules['title_patterns']:
        if self.matches_pattern(normalized_title, pattern):
            score += pattern.get('weight', 1.0)

    return score
```

**Pattern Matching Implementation**:
```python
def matches_pattern(self, text, pattern):
    """Apply different pattern matching types"""
    pattern_type = pattern['type']
    value = pattern['value']
    case_insensitive = pattern.get('case_insensitive', False)

    if case_insensitive:
        text = text.lower()
        value = value.lower()

    if pattern_type == 'contains':
        return value in text
    elif pattern_type == 'regex':
        import re
        return bool(re.search(value, text))
    elif pattern_type == 'exact':
        return value == text
    else:
        return False
```

### Keyword Analysis

**Required Keyword Check**:
```python
def evaluate_required_keywords(self, description):
    """Verify all required keywords are present"""
    if not description:
        return 0

    cleaned_desc = self.clean_job_description(description)
    missing_keywords = []

    for keyword in self.rules.get('required_keywords', []):
        if keyword.lower() not in cleaned_desc:
            missing_keywords.append(keyword)

    if missing_keywords:
        return 0  # All required keywords must be present

    return 1.0  # Full score if all present
```

**Optional Keyword Scoring**:
```python
def evaluate_optional_keywords(self, description):
    """Score based on optional keyword presence"""
    if not description:
        return 0

    cleaned_desc = self.clean_job_description(description)
    score = 0
    max_score = len(self.rules.get('optional_keywords', []))

    for keyword in self.rules.get('optional_keywords', []):
        if keyword.lower() in cleaned_desc:
            score += 1.0

    return score / max_score if max_score > 0 else 0
```

### Exclusion Logic

**Exclusion Pattern Check**:
```python
def check_exclusion_patterns(self, title):
    """Check if job should be excluded"""
    normalized_title = self.normalize_job_title(title)

    for pattern in self.rules.get('exclude_patterns', []):
        if self.matches_pattern(normalized_title, pattern):
            return True

    return False
```

**Company Filtering**:
```python
def is_excluded_company(self, company_name):
    """Check if company should be filtered out"""
    if not company_name:
        return False

    excluded_companies = self.rules.get('company_filters', {}).get('exclude_companies', [])
    company_lower = company_name.lower()

    for excluded in excluded_companies:
        if excluded.lower() in company_lower:
            return True

    return False
```

## Output Generation

### CSV Structure Design

**Flattened Data Format**:
```python
def create_flattened_records(self, job_data):
    """Convert job data to CSV records"""
    records = []

    # Extract base job information
    base_info = {
        'job_id': job_data.get('job_id', ''),
        'title': job_data.get('title', ''),
        'company': job_data.get('company_name', ''),
        'location': job_data.get('location', ''),
        'posted_date': self.extract_posted_date(job_data),
        'job_url': job_data.get('related_links', [{}])[0].get('link', ''),
        'source': 'serpapi'
    }

    # Create record for each responsibility
    responsibilities = job_data.get('extracted_responsibilities', [])
    if not responsibilities:
        # Create single record if no responsibilities extracted
        record = base_info.copy()
        record['responsibility'] = job_data.get('description', '')[:200] + '...'
        records.append(record)
    else:
        # Create record per responsibility
        for responsibility in responsibilities:
            record = base_info.copy()
            record['responsibility'] = responsibility
            records.append(record)

    return records
```

**CSV Schema**:
```csv
job_id,title,company,location,responsibility,posted_date,job_url,source
123456789,SOC Analyst,TechCorp Inc.,New York NY,Monitor security alerts and investigate potential threats,2024-11-28,https://example.com/job/123,serpapi
123456789,SOC Analyst,TechCorp Inc.,New York NY,Respond to security incidents within SLA timelines,2024-11-28,https://example.com/job/123,serpapi
```

### Metadata and Statistics

**Classification Report**:
```python
def generate_classification_report(self):
    """Create detailed classification statistics"""
    return {
        'total_jobs_processed': self.stats['total_jobs'],
        'soc_jobs_classified': self.stats['soc_jobs'],
        'filtered_out': self.stats['filtered_jobs'],
        'classification_rate': self.stats['soc_jobs'] / self.stats['total_jobs'] if self.stats['total_jobs'] > 0 else 0,
        'filter_reasons': dict(self.stats['filter_reasons']),
        'data_quality': {
            'jobs_with_complete_data': self.stats['complete_data_jobs'],
            'jobs_missing_location': self.stats['missing_location'],
            'average_responsibilities_per_job': self.stats['total_responsibilities'] / self.stats['soc_jobs'] if self.stats['soc_jobs'] > 0 else 0
        },
        'processing_time_seconds': time.time() - self.start_time
    }
```

## Performance Optimization

### Processing Efficiency

**Batch Processing**:
```python
def process_jobs_batch(self, jobs_data, batch_size=100):
    """Process jobs in batches for memory efficiency"""
    classified_jobs = []

    for i in range(0, len(jobs_data), batch_size):
        batch = jobs_data[i:i + batch_size]
        batch_results = [self.classify_single_job(job) for job in batch]
        classified_jobs.extend([job for job in batch_results if job])

        # Progress reporting
        progress = (i + len(batch)) / len(jobs_data) * 100
        print(f"Classification progress: {progress:.1f}%")

    return classified_jobs
```

### Memory Management

**Streaming CSV Writing**:
```python
def save_classified_data_streaming(self, classified_jobs, output_path):
    """Write CSV data without loading all into memory"""
    import csv

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['job_id', 'title', 'company', 'location',
                     'responsibility', 'posted_date', 'job_url', 'source']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for job in classified_jobs:
            records = self.create_flattened_records(job)
            for record in writerows(records):
                writer.writerow(record)
```

## Quality Assurance

### Validation Checks

**Output Validation**:
```python
def validate_output_data(self, output_path):
    """Verify generated CSV meets requirements"""
    df = pd.read_csv(output_path)

    # Check required columns
    required_cols = ['job_id', 'title', 'company', 'responsibility']
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Check data completeness
    completeness_score = 1 - (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]))

    # Check classification quality
    soc_keywords = ['monitor', 'alert', 'incident', 'threat']
    keyword_coverage = df['responsibility'].str.contains('|'.join(soc_keywords), case=False).mean()

    return {
        'completeness_score': completeness_score,
        'keyword_coverage': keyword_coverage,
        'total_records': len(df),
        'unique_jobs': df['job_id'].nunique()
    }
```

### Error Handling

**Robust Processing**:
```python
def classify_single_job_safe(self, job_data):
    """Classify with comprehensive error handling"""
    try:
        # Validate input
        if not self.validate_job_structure(job_data):
            self.stats['invalid_jobs'] += 1
            return None

        # Apply classification
        is_soc_job, score = self.apply_classification_rules(job_data)

        if is_soc_job:
            self.stats['soc_jobs'] += 1
            return job_data
        else:
            self.stats['filtered_jobs'] += 1
            return None

    except Exception as e:
        self.logger.error(f"Error classifying job {job_data.get('job_id', 'unknown')}: {e}")
        self.stats['classification_errors'] += 1
        return None
```

## Configuration Management

### Rules File Validation

**Schema Validation**:
```python
def validate_rules_schema(self, rules_data):
    """Ensure rules file has correct structure"""
    required_sections = ['title_patterns', 'exclude_patterns', 'required_keywords']

    for section in required_sections:
        if section not in rules_data:
            raise ValueError(f"Missing required section: {section}")

    # Validate pattern structures
    for pattern in rules_data.get('title_patterns', []):
        if 'type' not in pattern or 'value' not in pattern:
            raise ValueError(f"Invalid pattern structure: {pattern}")

    return True
```

### Dynamic Rule Loading

**Runtime Configuration**:
```python
def reload_rules(self, rules_file=None):
    """Reload classification rules at runtime"""
    if rules_file:
        self.rules_file = rules_file

    try:
        new_rules = self.load_classification_rules(self.rules_file)
        self.validate_rules_schema(new_rules)
        self.rules = new_rules
        self.logger.info("Classification rules reloaded successfully")
    except Exception as e:
        self.logger.error(f"Failed to reload rules: {e}")
        raise
```

## Integration and Extensibility

### Pipeline Integration

**Standard Interface**:
```python
# Integration with job_run.py
def run_job_classification():
    classifier = SOCJobClassifier()

    # Load raw data
    raw_jobs = classifier.load_raw_job_data('data/raw/serpapi/')

    # Apply classification
    classified_jobs = classifier.classify_jobs(raw_jobs)

    # Save results
    output_path = classifier.save_classified_data(classified_jobs)

    # Generate report
    report = classifier.generate_classification_report()

    return output_path, report
```

### Extension Points

**Custom Rules**:
```python
def add_custom_rule(self, rule_name, rule_config):
    """Add custom classification rule"""
    self.rules[rule_name] = rule_config
    self.validate_rules_schema(self.rules)
```

**Alternative Classifiers**:
```python
def register_classifier(self, name, classifier_function):
    """Register alternative classification method"""
    self.alternative_classifiers[name] = classifier_function
```

## Monitoring and Debugging

### Detailed Logging

**Classification Tracing**:
```python
def log_classification_decision(self, job_data, decision, score, reason=None):
    """Log detailed classification information"""
    log_entry = {
        'job_id': job_data.get('job_id'),
        'title': job_data.get('title'),
        'decision': 'classified' if decision else 'filtered',
        'score': score,
        'reason': reason,
        'timestamp': datetime.now().isoformat()
    }

    self.classification_log.append(log_entry)
```

### Performance Metrics

**Classification Metrics**:
- Processing speed (jobs/second)
- Memory usage patterns
- Rule application efficiency
- Error rates by category

**Quality Metrics**:
- Classification accuracy (manual validation)
- False positive/negative rates
- Rule coverage effectiveness
- Data completeness scores

## Troubleshooting Guide

### Common Classification Issues

**Over-Filtering**:
```
Problem: Too many jobs filtered out
Solution: Review exclude patterns, check keyword requirements
```

**Under-Filtering**:
```
Problem: Non-SOC jobs classified as SOC
Solution: Add more specific title patterns, increase keyword requirements
```

**Inconsistent Results**:
```
Problem: Same job classified differently on rerun
Solution: Check text normalization, ensure deterministic rule application
```

### Rules Tuning

**Iterative Refinement**:
```python
# Analyze classification results
def analyze_classification_accuracy(self, manual_labels):
    """Compare automated vs manual classification"""
    automated_results = self.classified_jobs
    accuracy_metrics = calculate_precision_recall(automated_results, manual_labels)

    # Identify misclassifications
    false_positives = find_false_positives(automated_results, manual_labels)
    false_negatives = find_false_negatives(automated_results, manual_labels)

    return {
        'accuracy': accuracy_metrics,
        'false_positives': false_positives,
        'false_negatives': false_negatives,
        'suggested_rule_changes': generate_rule_suggestions(false_positives, false_negatives)
    }
```

This module provides a flexible, rule-based classification system that can be easily customized for different cybersecurity job categories and research requirements.

---

**Last Updated:** December 2024
**Version:** 1.0.0
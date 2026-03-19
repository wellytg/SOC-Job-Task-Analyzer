# Task Aggregation Module Reference

## Overview

The task aggregation module (`task_aggregator.py`) consolidates historical SOC job data into a unified task lexicon using fuzzy deduplication algorithms. This module processes multiple CSV files from different time periods, extracts individual job responsibilities, and groups similar tasks to reduce redundancy while preserving semantic meaning.

## Module Architecture

### Core Components

```python
class TaskAggregator:
    def __init__(self, similarity_threshold=0.88):
        self.similarity_threshold = similarity_threshold
        self.stats = defaultdict(int)
        self.task_lexicon = []

    def aggregate_historical_tasks(self, data_directory):
        """Main aggregation pipeline"""

    def extract_tasks_from_csv(self, csv_file):
        """Extract tasks from individual CSV files"""

    def fuzzy_deduplicate_tasks(self, all_tasks):
        """Apply fuzzy matching to consolidate similar tasks"""

    def save_consolidated_lexicon(self, output_path):
        """Save deduplicated task lexicon"""
```

### Dependencies

**Required Packages**:
- `pandas`: CSV data processing and manipulation
- `difflib`: Fuzzy string matching algorithms
- `json`: Data serialization and output formatting
- `os`: File system operations and path handling
- `collections`: Data structure utilities (Counter, defaultdict)
- `datetime`: Timestamp processing and temporal analysis

**Input Data**:
- CSV files from `data/processed/` directory
- Expected format: SOC Tier 1 analysis CSVs with responsibility columns

## Data Ingestion Pipeline

### Historical Data Discovery

**CSV File Scanning**:
```python
def discover_csv_files(self, data_directory):
    """Find all relevant CSV files for aggregation"""
    import glob

    # Pattern for SOC analysis files
    pattern = os.path.join(data_directory, "*_soc_tier1_analysis.csv")

    csv_files = glob.glob(pattern)

    # Sort by modification time (newest first)
    csv_files.sort(key=os.path.getmtime, reverse=True)

    # Validate files exist and are readable
    valid_files = []
    for csv_file in csv_files:
        if self.validate_csv_file(csv_file):
            valid_files.append(csv_file)

    self.logger.info(f"Found {len(valid_files)} valid CSV files")
    return valid_files
```

**File Validation**:
```python
def validate_csv_file(self, csv_path):
    """Ensure CSV file meets requirements"""
    try:
        # Check file exists and is readable
        if not os.path.exists(csv_path):
            return False

        # Quick validation of CSV structure
        df = pd.read_csv(csv_path, nrows=5)  # Sample first 5 rows

        # Check required columns
        required_cols = ['job_id', 'responsibility']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            self.logger.warning(f"CSV {csv_path} missing columns: {missing_cols}")
            return False

        # Check data quality
        if len(df) == 0:
            self.logger.warning(f"CSV {csv_path} is empty")
            return False

        return True

    except Exception as e:
        self.logger.error(f"Error validating CSV {csv_path}: {e}")
        return False
```

### Task Extraction Logic

**CSV Processing**:
```python
def extract_tasks_from_csv(self, csv_path):
    """Extract individual tasks from CSV file"""
    tasks = []

    try:
        df = pd.read_csv(csv_path)

        for _, row in df.iterrows():
            task_data = {
                'task_text': str(row['responsibility']).strip(),
                'job_id': str(row['job_id']),
                'source_file': os.path.basename(csv_path),
                'metadata': {
                    'title': str(row.get('title', '')),
                    'company': str(row.get('company', '')),
                    'location': str(row.get('location', '')),
                    'posted_date': str(row.get('posted_date', ''))
                }
            }

            # Validate task content
            if self.is_valid_task(task_data['task_text']):
                tasks.append(task_data)

    except Exception as e:
        self.logger.error(f"Error processing CSV {csv_path}: {e}")

    self.logger.info(f"Extracted {len(tasks)} tasks from {csv_path}")
    return tasks
```

**Task Validation**:
```python
def is_valid_task(self, task_text):
    """Validate task content quality"""
    if not task_text or len(task_text.strip()) < 10:
        return False

    # Skip generic or irrelevant content
    invalid_patterns = [
        'equal opportunity employer',
        'benefits include',
        'salary range',
        'apply now',
        'click here'
    ]

    task_lower = task_text.lower()
    for pattern in invalid_patterns:
        if pattern in task_lower:
            return False

    # Must contain action-oriented language
    action_words = ['monitor', 'analyze', 'respond', 'investigate',
                   'maintain', 'configure', 'report', 'document']

    has_action = any(word in task_lower for word in action_words)
    if not has_action:
        return False

    return True
```

## Fuzzy Deduplication Algorithm

### Similarity Measurement

**Difflib-Based Matching**:
```python
def calculate_similarity(self, text1, text2):
    """Calculate similarity score between two task texts"""
    # Normalize texts
    norm1 = self.normalize_text(text1)
    norm2 = self.normalize_text(text2)

    # Use difflib for similarity scoring
    matcher = difflib.SequenceMatcher(None, norm1, norm2)
    similarity = matcher.ratio()

    # Boost similarity for tasks with same key terms
    if self.share_key_terms(norm1, norm2):
        similarity = min(1.0, similarity + 0.1)

    return similarity
```

**Text Normalization**:
```python
def normalize_text(self, text):
    """Normalize text for consistent comparison"""
    import re

    # Convert to lowercase
    normalized = text.lower()

    # Remove punctuation
    normalized = re.sub(r'[^\w\s]', ' ', normalized)

    # Normalize whitespace
    normalized = ' '.join(normalized.split())

    # Remove common stop words that don't affect meaning
    stop_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
    words = normalized.split()
    filtered_words = [word for word in words if word not in stop_words]
    normalized = ' '.join(filtered_words)

    return normalized
```

**Key Term Analysis**:
```python
def share_key_terms(self, text1, text2):
    """Check if texts share important security terms"""
    security_terms = [
        'security', 'threat', 'incident', 'alert', 'monitor',
        'analyze', 'respond', 'investigate', 'log', 'siem'
    ]

    words1 = set(text1.split())
    words2 = set(text2.split())

    shared_terms = words1.intersection(words2).intersection(set(security_terms))

    return len(shared_terms) >= 2  # At least 2 shared security terms
```

### Deduplication Process

**Clustering Algorithm**:
```python
def fuzzy_deduplicate_tasks(self, all_tasks):
    """Group similar tasks using fuzzy matching"""
    consolidated_tasks = []
    processed_indices = set()

    # Sort tasks by length (process shorter ones first for better matching)
    sorted_tasks = sorted(all_tasks, key=lambda x: len(x['task_text']))

    for i, current_task in enumerate(sorted_tasks):
        if i in processed_indices:
            continue

        # Start new cluster
        cluster = [current_task]
        processed_indices.add(i)

        # Find similar tasks
        for j, other_task in enumerate(sorted_tasks):
            if j in processed_indices or i == j:
                continue

            similarity = self.calculate_similarity(
                current_task['task_text'],
                other_task['task_text']
            )

            if similarity >= self.similarity_threshold:
                cluster.append(other_task)
                processed_indices.add(j)

        # Create consolidated task from cluster
        consolidated_task = self.consolidate_cluster(cluster)
        consolidated_tasks.append(consolidated_task)

    return consolidated_tasks
```

**Cluster Consolidation**:
```python
def consolidate_cluster(self, task_cluster):
    """Merge similar tasks into single representative task"""
    if len(task_cluster) == 1:
        task = task_cluster[0]
        return {
            'task_id': f"task_{self.task_counter:03d}",
            'task_text': task['task_text'],
            'frequency': 1,
            'source_jobs': [task['job_id']],
            'first_seen': task['metadata']['posted_date'],
            'last_seen': task['metadata']['posted_date'],
            'source_files': [task['source_file']],
            'confidence_score': 1.0,
            'cluster_size': 1
        }

    # Multiple similar tasks - find representative
    texts = [task['task_text'] for task in task_cluster]

    # Use longest text as base (usually most complete)
    representative_text = max(texts, key=len)

    # Collect metadata
    job_ids = list(set(task['job_id'] for task in task_cluster))
    source_files = list(set(task['source_file'] for task in task_cluster))
    dates = [task['metadata']['posted_date'] for task in task_cluster if task['metadata']['posted_date']]

    # Calculate date range
    valid_dates = [d for d in dates if d and d != '']
    if valid_dates:
        first_seen = min(valid_dates)
        last_seen = max(valid_dates)
    else:
        first_seen = last_seen = "unknown"

    # Calculate confidence based on cluster consistency
    avg_similarity = self.calculate_cluster_similarity(texts)
    confidence = min(1.0, avg_similarity + 0.1)  # Boost for larger clusters

    return {
        'task_id': f"task_{self.task_counter:03d}",
        'task_text': representative_text,
        'frequency': len(task_cluster),
        'source_jobs': job_ids,
        'first_seen': first_seen,
        'last_seen': last_seen,
        'source_files': source_files,
        'confidence_score': confidence,
        'cluster_size': len(task_cluster)
    }
```

## Output Generation

### Consolidated Lexicon Format

**JSON Structure**:
```json
[
  {
    "task_id": "task_001",
    "task_text": "Monitor security alerts and investigate potential threats",
    "frequency": 15,
    "source_jobs": ["job_123", "job_456", "job_789"],
    "first_seen": "2024-10-01",
    "last_seen": "2024-12-01",
    "source_files": ["soc_jobs_20241001_soc_tier1_analysis.csv"],
    "confidence_score": 0.95,
    "cluster_size": 12
  }
]
```

**Frequency Report**:
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

### Data Quality Assurance

**Validation Checks**:
```python
def validate_consolidated_lexicon(self, lexicon):
    """Ensure output meets quality standards"""
    validation_results = {
        'total_tasks': len(lexicon),
        'unique_task_ids': len(set(task['task_id'] for task in lexicon)),
        'average_confidence': sum(task['confidence_score'] for task in lexicon) / len(lexicon),
        'data_completeness': 0,
        'issues': []
    }

    # Check data completeness
    required_fields = ['task_id', 'task_text', 'frequency', 'source_jobs']
    complete_tasks = 0

    for task in lexicon:
        missing_fields = [field for field in required_fields if field not in task]
        if not missing_fields:
            complete_tasks += 1
        else:
            validation_results['issues'].append(f"Task {task.get('task_id', 'unknown')} missing: {missing_fields}")

    validation_results['data_completeness'] = complete_tasks / len(lexicon)

    # Check for duplicate task IDs
    task_ids = [task['task_id'] for task in lexicon]
    duplicates = [id for id in task_ids if task_ids.count(id) > 1]
    if duplicates:
        validation_results['issues'].append(f"Duplicate task IDs: {set(duplicates)}")

    return validation_results
```

## Performance Optimization

### Memory-Efficient Processing

**Streaming CSV Reading**:
```python
def process_csv_streaming(self, csv_path):
    """Process large CSV files without loading entirely into memory"""
    tasks = []
    chunk_size = 1000

    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        for _, row in chunk.iterrows():
            task_data = self.extract_task_from_row(row)
            if task_data:
                tasks.append(task_data)

        # Optional: Process chunks incrementally
        if len(tasks) > 5000:
            self.process_task_batch(tasks)
            tasks = []

    return tasks
```

### Algorithm Optimization

**Similarity Caching**:
```python
def __init__(self, similarity_threshold=0.88):
    self.similarity_cache = {}
    # Cache similarity scores to avoid recomputation

def get_cached_similarity(self, text1, text2):
    """Retrieve or calculate similarity with caching"""
    key = hash((text1, text2))  # Create deterministic key

    if key not in self.similarity_cache:
        self.similarity_cache[key] = self.calculate_similarity(text1, text2)

    return self.similarity_cache[key]
```

**Early Termination**:
```python
def find_best_match_optimized(self, target_text, candidate_texts):
    """Find best match with early termination for high similarity"""
    best_score = 0
    best_match = None

    for candidate in candidate_texts:
        score = self.calculate_similarity(target_text, candidate)

        if score >= self.similarity_threshold:
            return candidate, score  # Early exit on good match

        if score > best_score:
            best_score = score
            best_match = candidate

    return best_match, best_score
```

## Configuration and Tuning

### Similarity Threshold Tuning

**Threshold Impact Analysis**:
```python
def analyze_threshold_impact(self, tasks, thresholds=[0.8, 0.85, 0.9, 0.95]):
    """Analyze how different thresholds affect deduplication"""
    results = {}

    for threshold in thresholds:
        self.similarity_threshold = threshold
        deduplicated = self.fuzzy_deduplicate_tasks(tasks)

        results[threshold] = {
            'unique_tasks': len(deduplicated),
            'deduplication_rate': 1 - (len(deduplicated) / len(tasks)),
            'average_cluster_size': sum(task['cluster_size'] for task in deduplicated) / len(deduplicated)
        }

    return results
```

**Optimal Threshold Selection**:
```python
def find_optimal_threshold(self, tasks, validation_pairs):
    """Find threshold that maximizes accuracy on validation set"""
    best_threshold = 0.88
    best_accuracy = 0

    for threshold in [0.8, 0.82, 0.85, 0.88, 0.9, 0.92]:
        predicted_similar = []

        for text1, text2, actual_similar in validation_pairs:
            predicted = self.calculate_similarity(text1, text2) >= threshold
            predicted_similar.append(predicted)

        accuracy = sum(p == a for p, a in zip(predicted_similar, validation_pairs)) / len(validation_pairs)

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_threshold = threshold

    return best_threshold, best_accuracy
```

## Quality Metrics and Validation

### Deduplication Quality Assessment

**Manual Validation Sampling**:
```python
def create_validation_sample(self, original_tasks, deduplicated_tasks, sample_size=50):
    """Create sample for manual quality assessment"""
    validation_sample = []

    for consolidated_task in deduplicated_tasks[:sample_size]:
        # Find original tasks in this cluster
        cluster_tasks = [t for t in original_tasks if t['task_text'] in consolidated_task.get('cluster_texts', [])]

        validation_sample.append({
            'consolidated_task': consolidated_task['task_text'],
            'original_tasks': [t['task_text'] for t in cluster_tasks],
            'cluster_size': len(cluster_tasks),
            'similarity_score': consolidated_task['confidence_score']
        })

    return validation_sample
```

### Statistical Analysis

**Deduplication Statistics**:
```python
def generate_deduplication_stats(self, original_tasks, deduplicated_tasks):
    """Generate comprehensive deduplication statistics"""
    return {
        'input_metrics': {
            'total_original_tasks': len(original_tasks),
            'unique_original_texts': len(set(t['task_text'] for t in original_tasks))
        },
        'output_metrics': {
            'total_consolidated_tasks': len(deduplicated_tasks),
            'average_cluster_size': sum(t['cluster_size'] for t in deduplicated_tasks) / len(deduplicated_tasks),
            'largest_cluster': max(t['cluster_size'] for t in deduplicated_tasks),
            'singletons': sum(1 for t in deduplicated_tasks if t['cluster_size'] == 1)
        },
        'quality_metrics': {
            'deduplication_rate': 1 - (len(deduplicated_tasks) / len(original_tasks)),
            'average_confidence': sum(t['confidence_score'] for t in deduplicated_tasks) / len(deduplicated_tasks),
            'high_confidence_tasks': sum(1 for t in deduplicated_tasks if t['confidence_score'] > 0.9)
        }
    }
```

## Integration and Extensibility

### Pipeline Integration

**Standard Interface**:
```python
# Integration with job_run.py
def run_task_aggregation():
    aggregator = TaskAggregator(similarity_threshold=0.88)

    # Aggregate historical data
    consolidated_lexicon = aggregator.aggregate_historical_tasks('data/processed/')

    # Save results
    output_path = aggregator.save_consolidated_lexicon('data/processed/task_lexicon/consolidated_tasks.json')

    # Generate reports
    frequency_report = aggregator.generate_frequency_report()

    return output_path, frequency_report
```

### Alternative Algorithms

**Plugin Architecture**:
```python
def register_deduplication_algorithm(self, name, algorithm_function):
    """Allow custom deduplication algorithms"""
    self.algorithms[name] = algorithm_function

def apply_algorithm(self, algorithm_name, tasks):
    """Apply registered algorithm"""
    if algorithm_name not in self.algorithms:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")

    return self.algorithms[algorithm_name](tasks)
```

## Monitoring and Debugging

### Execution Logging

**Detailed Progress Tracking**:
```python
def log_aggregation_progress(self, stage, details):
    """Log aggregation progress with context"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'stage': stage,
        'details': details,
        'stats': dict(self.stats)
    }

    self.progress_log.append(log_entry)
    self.logger.info(f"{stage}: {details}")
```

### Error Handling

**Robust Processing**:
```python
def aggregate_with_error_handling(self, data_directory):
    """Aggregation with comprehensive error handling"""
    try:
        # Discover files
        csv_files = self.discover_csv_files(data_directory)

        # Process each file safely
        all_tasks = []
        for csv_file in csv_files:
            try:
                tasks = self.extract_tasks_from_csv(csv_file)
                all_tasks.extend(tasks)
            except Exception as e:
                self.logger.error(f"Failed to process {csv_file}: {e}")
                continue

        # Deduplicate
        consolidated = self.fuzzy_deduplicate_tasks(all_tasks)

        # Validate results
        validation = self.validate_consolidated_lexicon(consolidated)
        if validation['data_completeness'] < 0.9:
            self.logger.warning(f"Low data completeness: {validation['data_completeness']}")

        return consolidated

    except Exception as e:
        self.logger.error(f"Aggregation failed: {e}")
        raise
```

## Troubleshooting Guide

### Common Deduplication Issues

**Over-Deduplication**:
```
Problem: Similar but distinct tasks merged incorrectly
Solution: Increase similarity threshold, review normalization logic
```

**Under-Deduplication**:
```
Problem: Very similar tasks remain separate
Solution: Decrease similarity threshold, improve normalization
```

**Performance Issues**:
```
Problem: Deduplication takes too long
Solution: Implement similarity caching, process in batches
```

### Quality Validation

**Manual Review Process**:
```python
def perform_manual_review(self, deduplicated_tasks, review_sample_size=20):
    """Generate sample for manual quality assessment"""
    import random

    # Sample diverse tasks
    sample = random.sample(deduplicated_tasks, min(review_sample_size, len(deduplicated_tasks)))

    review_data = []
    for task in sample:
        review_data.append({
            'task_id': task['task_id'],
            'task_text': task['task_text'],
            'cluster_size': task['cluster_size'],
            'confidence': task['confidence_score'],
            'review_questions': [
                "Is this task clear and actionable?",
                "Does this task represent a distinct responsibility?",
                "Is the consolidation appropriate?"
            ]
        })

    return review_data
```

This module provides a robust, configurable system for consolidating SOC job task data while preserving semantic meaning and supporting research-quality analysis.

---

**Last Updated:** December 2024
**Version:** 1.0.0
# API Reference

## Core Modules

### soc_scrapper_API.py

#### serpapi_google_jobs_search()

**Function Signature:**
```python
def serpapi_google_jobs_search(
    query: str,
    location: str = "United States",
    num_pages: int = 5,
    api_key: str = None
) -> List[Dict[str, Any]]
```

**Description:**
Searches Google Jobs using SerpAPI and returns structured job data.

**Parameters:**
- `query` (str): Job search query (e.g., "data scientist", "software engineer")
- `location` (str): Geographic location for job search (default: "United States")
- `num_pages` (int): Number of result pages to retrieve (default: 5)
- `api_key` (str): SerpAPI key (uses environment variable if None)

**Returns:**
List of job dictionaries with keys: 'id', 'title', 'company_name', 'location', 'description', 'job_highlights'

**Raises:**
- `ValueError`: If API key is not provided
- `requests.RequestException`: For network/API errors

**Example:**
```python
jobs = serpapi_google_jobs_search(
    query="machine learning engineer",
    location="San Francisco, CA",
    num_pages=3
)
```

#### extract_responsibilities()

**Function Signature:**
```python
def extract_responsibilities(job_description: str) -> List[str]
```

**Description:**
Extracts job responsibilities from job descriptions using regex patterns.

**Parameters:**
- `job_description` (str): Full job description text

**Returns:**
List of extracted responsibility strings

**Example:**
```python
desc = "We are looking for someone who can analyze data and build models..."
responsibilities = extract_responsibilities(desc)
# Returns: ["analyze data", "build models"]
```

### data_analyzer.py

#### apply_classification_rules()

**Function Signature:**
```python
def apply_classification_rules(
    jobs_data: List[Dict[str, Any]],
    rules_file: str = "configs/rules.json"
) -> Dict[str, Any]
```

**Description:**
Applies SOC classification rules to filter and categorize job postings.

**Parameters:**
- `jobs_data` (List[Dict]): List of job dictionaries
- `rules_file` (str): Path to classification rules JSON file

**Returns:**
Dictionary with 'classified_jobs' and 'summary' keys

**Example:**
```python
result = apply_classification_rules(jobs_data)
classified_jobs = result['classified_jobs']
```

#### load_classification_rules()

**Function Signature:**
```python
def load_classification_rules(rules_file: str) -> Dict[str, Any]
```

**Description:**
Loads classification rules from JSON configuration file.

**Parameters:**
- `rules_file` (str): Path to rules file

**Returns:**
Dictionary containing classification rules

### task_aggregator.py

#### fuzzy_deduplicate_tasks()

**Function Signature:**
```python
def fuzzy_deduplicate_tasks(
    tasks: List[str],
    similarity_threshold: float = 0.88
) -> Dict[str, Any]
```

**Description:**
Performs fuzzy deduplication of task descriptions using similarity matching.

**Parameters:**
- `tasks` (List[str]): List of task description strings
- `similarity_threshold` (float): Similarity threshold for deduplication (0.0-1.0)

**Returns:**
Dictionary with 'unique_tasks', 'duplicates_removed', and 'clusters' keys

**Example:**
```python
result = fuzzy_deduplicate_tasks(task_list, similarity_threshold=0.9)
unique_tasks = result['unique_tasks']
```

#### consolidate_cluster()

**Function Signature:**
```python
def consolidate_cluster(cluster: List[str]) -> str
```

**Description:**
Consolidates a cluster of similar tasks into a single representative task.

**Parameters:**
- `cluster` (List[str]): List of similar task strings

**Returns:**
Consolidated task string

### task_thematic_clusterer.py

#### assign_theme_to_task()

**Function Signature:**
```python
def assign_theme_to_task(
    task: str,
    themes_config: Dict[str, List[str]]
) -> Tuple[str, float]
```

**Description:**
Assigns a thematic category to a task based on keyword matching.

**Parameters:**
- `task` (str): Task description string
- `themes_config` (Dict): Dictionary mapping themes to keyword lists

**Returns:**
Tuple of (theme_name, confidence_score)

**Example:**
```python
theme, confidence = assign_theme_to_task(
    "analyze sales data and create reports",
    themes_config
)
```

#### cluster_tasks_batch()

**Function Signature:**
```python
def cluster_tasks_batch(
    tasks: List[str],
    themes_config: Dict[str, List[str]],
    batch_size: int = 100
) -> Dict[str, Any]
```

**Description:**
Performs batch thematic clustering of tasks.

**Parameters:**
- `tasks` (List[str]): List of task descriptions
- `themes_config` (Dict): Theme configuration dictionary
- `batch_size` (int): Processing batch size

**Returns:**
Dictionary with clustering results and statistics

### job_run.py

#### run_pipeline()

**Function Signature:**
```python
def run_pipeline(
    stages: List[str] = None,
    config: Dict[str, Any] = None
) -> Dict[str, Any]
```

**Description:**
Executes the complete SOC job analysis pipeline.

**Parameters:**
- `stages` (List[str]): List of stages to execute (default: all stages)
- `config` (Dict): Pipeline configuration dictionary

**Returns:**
Dictionary with pipeline execution results and metrics

**Example:**
```python
result = run_pipeline(stages=['scraping', 'classification'])
```

#### generate_summary_report()

**Function Signature:**
```python
def generate_summary_report(results: Dict[str, Any]) -> str
```

**Description:**
Generates a human-readable summary report of pipeline execution.

**Parameters:**
- `results` (Dict): Pipeline execution results

**Returns:**
Formatted summary string

## Configuration Classes

### RulesEngine

**Class Overview:**
Handles loading and application of classification rules.

**Methods:**
- `__init__(rules_file: str)`: Initialize with rules file path
- `load_rules() -> Dict`: Load rules from file
- `validate_job(job: Dict) -> bool`: Validate job against rules
- `classify_job(job: Dict) -> str`: Classify job into SOC category

**Example:**
```python
engine = RulesEngine("configs/rules.json")
is_valid = engine.validate_job(job_data)
category = engine.classify_job(job_data)
```

### DataProcessor

**Class Overview:**
Handles data loading, processing, and output generation.

**Methods:**
- `__init__(input_dir: str, output_dir: str)`: Initialize with directories
- `load_raw_data() -> List[Dict]`: Load raw job data
- `process_data(data: List[Dict]) -> Dict`: Process data through pipeline
- `save_results(results: Dict, format: str)`: Save results in specified format

**Example:**
```python
processor = DataProcessor("data/raw", "data/processed")
data = processor.load_raw_data()
results = processor.process_data(data)
processor.save_results(results, "json")
```

## Utility Functions

### File Operations

#### save_to_json()

**Function Signature:**
```python
def save_to_json(data: Any, filepath: str, indent: int = 2) -> None
```

**Description:**
Saves data to JSON file with proper formatting.

**Parameters:**
- `data` (Any): Data to save (must be JSON serializable)
- `filepath` (str): Output file path
- `indent` (int): JSON indentation level

#### load_from_json()

**Function Signature:**
```python
def load_from_json(filepath: str) -> Any
```

**Description:**
Loads data from JSON file.

**Parameters:**
- `filepath` (str): Input file path

**Returns:**
Deserialized JSON data

### Text Processing

#### clean_text()

**Function Signature:**
```python
def clean_text(text: str) -> str
```

**Description:**
Cleans and normalizes text data.

**Parameters:**
- `text` (str): Input text

**Returns:**
Cleaned text string

**Processing Steps:**
- Remove extra whitespace
- Normalize unicode characters
- Remove special characters
- Convert to lowercase

#### tokenize_text()

**Function Signature:**
```python
def tokenize_text(text: str) -> List[str]
```

**Description:**
Tokenizes text into words for analysis.

**Parameters:**
- `text` (str): Input text

**Returns:**
List of word tokens

## Data Structures

### Job Data Format

```python
{
    "id": "unique_job_id",
    "title": "Job Title",
    "company_name": "Company Name",
    "location": "City, State",
    "description": "Full job description text...",
    "job_highlights": ["highlight1", "highlight2"],
    "serpapi_metadata": {
        "search_query": "query_used",
        "search_location": "location_used",
        "retrieved_at": "2024-01-01T00:00:00Z"
    }
}
```

### Task Data Format

```python
{
    "text": "Task description text",
    "job_id": "associated_job_id",
    "confidence": 0.95,
    "source": "responsibilities|requirements|benefits",
    "metadata": {
        "extracted_at": "2024-01-01T00:00:00Z",
        "similarity_score": 0.88
    }
}
```

### Classification Rules Format

```json
{
    "soc_tier1_categories": {
        "11-0000": {
            "name": "Management Occupations",
            "title_patterns": ["manager", "director", "executive"],
            "required_keywords": ["leadership", "strategy"],
            "exclude_patterns": ["assistant", "intern"]
        }
    },
    "validation_rules": {
        "min_title_length": 3,
        "max_title_length": 100,
        "required_fields": ["title", "description"]
    }
}
```

### Pipeline Configuration Format

```python
{
    "scraping": {
        "api_key_env": "SERPAPI_KEY",
        "default_location": "United States",
        "max_pages": 5,
        "rate_limit_delay": 1.0
    },
    "classification": {
        "rules_file": "configs/rules.json",
        "strict_matching": false,
        "case_sensitive": false
    },
    "aggregation": {
        "similarity_threshold": 0.88,
        "min_cluster_size": 2,
        "max_clusters": 1000
    },
    "clustering": {
        "themes_file": "configs/themes.json",
        "confidence_threshold": 0.7,
        "batch_size": 100
    },
    "output": {
        "format": "json",
        "compress_output": true,
        "include_metadata": true
    }
}
```

## Error Handling

### Custom Exceptions

#### PipelineError

**Description:**
Base exception for pipeline-related errors.

**Attributes:**
- `stage` (str): Pipeline stage where error occurred
- `message` (str): Error description
- `data` (Any): Additional error context

#### APIError

**Description:**
Exception for API-related errors.

**Attributes:**
- `api_name` (str): Name of the API (e.g., "SerpAPI")
- `status_code` (int): HTTP status code
- `response` (str): API response content

#### ValidationError

**Description:**
Exception for data validation errors.

**Attributes:**
- `field` (str): Field that failed validation
- `value` (Any): Invalid value
- `reason` (str): Validation failure reason

### Error Handling Patterns

```python
try:
    result = run_pipeline()
except PipelineError as e:
    logger.error(f"Pipeline failed at stage {e.stage}: {e.message}")
    # Handle pipeline error
except APIError as e:
    logger.error(f"API {e.api_name} failed with status {e.status_code}")
    # Handle API error
except ValidationError as e:
    logger.error(f"Validation failed for {e.field}: {e.reason}")
    # Handle validation error
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Handle unexpected errors
```

## Performance Optimization APIs

### MemoryProfiler

**Class Overview:**
Monitors memory usage throughout pipeline execution.

**Methods:**
- `take_snapshot(label: str)`: Take memory usage snapshot
- `get_memory_report()`: Generate memory usage report

### ParallelProcessor

**Class Overview:**
Handles parallel processing of data chunks.

**Methods:**
- `map_function(func, items, chunk_size)`: Map function over items in parallel
- `process_chunk(func, chunk)`: Process single data chunk

### ComputationCache

**Class Overview:**
Caches computation results to disk for reuse.

**Methods:**
- `cache_computation(func)`: Decorator for caching function results
- `clear_cache()`: Clear all cached results

---

**Last Updated:** December 2024
**Version:** 1.0.0
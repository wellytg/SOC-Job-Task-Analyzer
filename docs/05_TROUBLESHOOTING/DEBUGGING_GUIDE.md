# Debugging Guide

## Overview

This guide provides systematic debugging procedures for the SOC Job Task Analyzer pipeline. It covers debugging tools, techniques, and workflows for identifying and resolving issues across all pipeline stages.

## Debugging Infrastructure

### Logging Configuration

**Advanced Logging Setup**:
```python
import logging
import logging.config
from pathlib import Path

def setup_advanced_logging(log_level='DEBUG', log_file='debug.log'):
    """Configure comprehensive logging for debugging"""

    # Create logs directory
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    # Logging configuration
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            },
            'simple': {
                'format': '%(levelname)s - %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'simple',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': log_level,
                'formatter': 'detailed',
                'filename': log_dir / log_file,
                'mode': 'a'
            },
            'debug_file': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'filename': log_dir / 'debug_detailed.log',
                'mode': 'a'
            }
        },
        'loggers': {
            'soc_analyzer': {
                'level': log_level,
                'handlers': ['console', 'file', 'debug_file'],
                'propagate': False
            },
            'data_collection': {
                'level': log_level,
                'handlers': ['console', 'file'],
                'propagate': False
            },
            'classification': {
                'level': log_level,
                'handlers': ['console', 'file'],
                'propagate': False
            },
            'aggregation': {
                'level': log_level,
                'handlers': ['console', 'file'],
                'propagate': False
            },
            'clustering': {
                'level': log_level,
                'handlers': ['console', 'file'],
                'propagate': False
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console']
        }
    }

    logging.config.dictConfig(logging_config)

    # Create logger instances
    loggers = {
        'main': logging.getLogger('soc_analyzer'),
        'data': logging.getLogger('data_collection'),
        'classify': logging.getLogger('classification'),
        'aggregate': logging.getLogger('aggregation'),
        'cluster': logging.getLogger('clustering')
    }

    return loggers
```

### Debug Data Collection

**Pipeline State Capture**:
```python
import pickle
import json
from datetime import datetime
from pathlib import Path

class DebugDataCollector:
    """Collect and persist debug data throughout pipeline execution"""

    def __init__(self, debug_dir='debug_data'):
        self.debug_dir = Path(debug_dir)
        self.debug_dir.mkdir(exist_ok=True)
        self.execution_id = datetime.now().strftime('%Y%m%d_%H%M%S')

    def save_stage_input(self, stage_name, data):
        """Save input data for a pipeline stage"""

        filename = f"{self.execution_id}_{stage_name}_input.pkl"
        filepath = self.debug_dir / filename

        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

        self._log_save(f"Stage input: {stage_name}", filepath)

    def save_stage_output(self, stage_name, data):
        """Save output data for a pipeline stage"""

        filename = f"{self.execution_id}_{stage_name}_output.pkl"
        filepath = self.debug_dir / filename

        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

        self._log_save(f"Stage output: {stage_name}", filepath)

    def save_intermediate_state(self, stage_name, step_name, data):
        """Save intermediate computation state"""

        filename = f"{self.execution_id}_{stage_name}_{step_name}_intermediate.pkl"
        filepath = self.debug_dir / filename

        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

    def save_error_context(self, stage_name, error, context_data):
        """Save error context for debugging"""

        error_data = {
            'timestamp': datetime.now().isoformat(),
            'stage': stage_name,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context_data,
            'stack_trace': self._get_stack_trace()
        }

        filename = f"{self.execution_id}_{stage_name}_error.json"
        filepath = self.debug_dir / filename

        with open(filepath, 'w') as f:
            json.dump(error_data, f, indent=2, default=str)

    def _log_save(self, description, filepath):
        """Log debug data save operation"""

        logger = logging.getLogger('soc_analyzer.debug')
        logger.debug(f"Saved {description} to {filepath}")

    def _get_stack_trace(self):
        """Get current stack trace"""

        import traceback
        return traceback.format_exc()

# Global debug collector instance
debug_collector = DebugDataCollector()
```

## Stage-Specific Debugging

### Data Collection Debugging

**API Request Debugging**:
```python
def debug_api_request(url, params, headers=None, timeout=30):
    """Debug API request with detailed logging"""

    import requests
    import time

    logger = logging.getLogger('data_collection.debug')

    # Log request details
    logger.debug(f"API Request URL: {url}")
    logger.debug(f"Request params: {json.dumps(params, indent=2)}")
    logger.debug(f"Timeout: {timeout}s")

    start_time = time.time()

    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response_time = time.time() - start_time

        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response time: {response_time:.2f}s")
        logger.debug(f"Response headers: {dict(response.headers)}")

        # Log response content (truncated for large responses)
        content_preview = response.text[:500] + "..." if len(response.text) > 500 else response.text
        logger.debug(f"Response content preview: {content_preview}")

        if response.status_code == 200:
            try:
                json_data = response.json()
                logger.debug(f"JSON response keys: {list(json_data.keys()) if isinstance(json_data, dict) else 'Not a dict'}")

                # Save debug data
                debug_collector.save_intermediate_state('data_collection', 'api_response', {
                    'url': url,
                    'params': params,
                    'response_time': response_time,
                    'status_code': response.status_code,
                    'response_size': len(response.text),
                    'json_keys': list(json_data.keys()) if isinstance(json_data, dict) else None
                })

                return json_data

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                debug_collector.save_error_context('data_collection', e, {
                    'response_text': response.text[:1000],
                    'content_type': response.headers.get('content-type')
                })
                raise
        else:
            error_msg = f"API request failed with status {response.status_code}"
            logger.error(error_msg)
            logger.error(f"Response content: {response.text}")

            error = requests.HTTPError(error_msg)
            debug_collector.save_error_context('data_collection', error, {
                'status_code': response.status_code,
                'response_text': response.text,
                'request_params': params
            })
            raise error

    except requests.exceptions.Timeout as e:
        logger.error(f"API request timeout after {timeout}s")
        debug_collector.save_error_context('data_collection', e, {
            'timeout': timeout,
            'url': url,
            'params': params
        })
        raise

    except requests.exceptions.ConnectionError as e:
        logger.error(f"API connection error: {e}")
        debug_collector.save_error_context('data_collection', e, {
            'url': url,
            'connection_error': str(e)
        })
        raise
```

**Data Quality Debugging**:
```python
def debug_data_quality_analysis(jobs_data):
    """Debug analysis of collected job data quality"""

    logger = logging.getLogger('data_collection.debug')

    quality_metrics = {
        'total_jobs': len(jobs_data),
        'jobs_with_descriptions': 0,
        'jobs_with_companies': 0,
        'jobs_with_locations': 0,
        'average_description_length': 0,
        'description_length_distribution': {},
        'missing_fields': {}
    }

    description_lengths = []

    for i, job in enumerate(jobs_data):
        # Check description
        description = job.get('description', '')
        if description and len(description.strip()) > 0:
            quality_metrics['jobs_with_descriptions'] += 1
            desc_len = len(description)
            description_lengths.append(desc_len)

            # Categorize description lengths
            if desc_len < 50:
                quality_metrics['description_length_distribution']['very_short'] = \
                    quality_metrics['description_length_distribution'].get('very_short', 0) + 1
            elif desc_len < 200:
                quality_metrics['description_length_distribution']['short'] = \
                    quality_metrics['description_length_distribution'].get('short', 0) + 1
            elif desc_len < 1000:
                quality_metrics['description_length_distribution']['medium'] = \
                    quality_metrics['description_length_distribution'].get('medium', 0) + 1
            else:
                quality_metrics['description_length_distribution']['long'] = \
                    quality_metrics['description_length_distribution'].get('long', 0) + 1

        # Check company
        if job.get('company_name'):
            quality_metrics['jobs_with_companies'] += 1
        else:
            quality_metrics['missing_fields']['company'] = \
                quality_metrics['missing_fields'].get('company', 0) + 1

        # Check location
        if job.get('location'):
            quality_metrics['jobs_with_locations'] += 1
        else:
            quality_metrics['missing_fields']['location'] = \
                quality_metrics['missing_fields'].get('location', 0) + 1

        # Log problematic jobs
        if not description or len(description.strip()) < 50:
            logger.warning(f"Job {i} has inadequate description: '{description[:100]}...'")
        if not job.get('company_name'):
            logger.warning(f"Job {i} missing company name: {job.get('title', 'Unknown title')}")
        if not job.get('location'):
            logger.warning(f"Job {i} missing location: {job.get('title', 'Unknown title')}")

    # Calculate averages
    if description_lengths:
        quality_metrics['average_description_length'] = sum(description_lengths) / len(description_lengths)

    # Calculate percentages
    for key in ['jobs_with_descriptions', 'jobs_with_companies', 'jobs_with_locations']:
        pct_key = key.replace('jobs_with_', '') + '_percentage'
        quality_metrics[pct_key] = (quality_metrics[key] / quality_metrics['total_jobs']) * 100

    # Log summary
    logger.info("Data Quality Analysis Summary:")
    logger.info(f"  Total jobs: {quality_metrics['total_jobs']}")
    logger.info(f"  Jobs with descriptions: {quality_metrics['jobs_with_descriptions']} ({quality_metrics['description_percentage']:.1f}%)")
    logger.info(f"  Average description length: {quality_metrics['average_description_length']:.1f} characters")
    logger.info(f"  Jobs with companies: {quality_metrics['jobs_with_companies']} ({quality_metrics['company_percentage']:.1f}%)")
    logger.info(f"  Jobs with locations: {quality_metrics['jobs_with_locations']} ({quality_metrics['location_percentage']:.1f}%)")

    if quality_metrics['missing_fields']:
        logger.warning(f"Missing fields: {quality_metrics['missing_fields']}")

    # Save debug data
    debug_collector.save_intermediate_state('data_collection', 'quality_analysis', quality_metrics)

    return quality_metrics
```

### Classification Debugging

**Rule Evaluation Debugging**:
```python
def debug_rule_evaluation(job_data, rules_config):
    """Debug detailed rule evaluation process"""

    logger = logging.getLogger('classification.debug')

    evaluation_results = []

    logger.debug(f"Evaluating job: {job_data.get('title', 'Unknown title')}")
    logger.debug(f"Job description preview: {job_data.get('description', '')[:200]}...")

    for rule in rules_config.get('rules', []):
        rule_id = rule['rule_id']
        logger.debug(f"Evaluating rule: {rule_id}")

        rule_result = {
            'rule_id': rule_id,
            'conditions_evaluated': [],
            'total_score': 0.0,
            'max_possible_score': 0.0,
            'confidence': 0.0,
            'passed': False,
            'exclusions_triggered': []
        }

        # Evaluate each condition
        for i, condition in enumerate(rule.get('conditions', [])):
            condition_result = evaluate_condition_debug(job_data, condition)
            rule_result['conditions_evaluated'].append(condition_result)

            if condition_result['matched']:
                rule_result['total_score'] += condition['weight']
                logger.debug(f"  Condition {i} matched: +{condition['weight']} points")
            else:
                logger.debug(f"  Condition {i} not matched")

            rule_result['max_possible_score'] += condition['weight']

        # Check exclusions
        for exclusion in rule.get('exclusions', []):
            exclusion_result = evaluate_condition_debug(job_data, exclusion)
            if exclusion_result['matched']:
                rule_result['exclusions_triggered'].append(exclusion_result)
                logger.debug(f"  Exclusion triggered: {exclusion.get('reason', 'No reason provided')}")

        # Calculate confidence
        if rule_result['max_possible_score'] > 0:
            rule_result['confidence'] = rule_result['total_score'] / rule_result['max_possible_score']

        rule_result['passed'] = rule_result['confidence'] >= rule['threshold'] and not rule_result['exclusions_triggered']

        evaluation_results.append(rule_result)

        logger.debug(f"Rule {rule_id} result: confidence={rule_result['confidence']:.3f}, threshold={rule['threshold']}, passed={rule_result['passed']}")

    # Determine final classification
    passed_rules = [r for r in evaluation_results if r['passed']]
    final_classification = passed_rules[0]['rule_id'] if passed_rules else 'unclassified'

    logger.info(f"Final classification: {final_classification}")

    # Save debug data
    debug_data = {
        'job_data': job_data,
        'evaluation_results': evaluation_results,
        'final_classification': final_classification
    }
    debug_collector.save_intermediate_state('classification', 'rule_evaluation', debug_data)

    return final_classification, evaluation_results

def evaluate_condition_debug(job_data, condition):
    """Evaluate a single condition with debug information"""

    field = condition['field']
    operator = condition['operator']
    field_value = job_data.get(field, '')

    result = {
        'field': field,
        'operator': operator,
        'field_value': field_value,
        'expected_value': None,
        'matched': False,
        'match_details': {}
    }

    try:
        if operator == 'regex_match':
            import re
            pattern = condition['pattern']
            result['expected_value'] = pattern
            match = re.search(pattern, field_value, re.IGNORECASE)
            result['matched'] = match is not None
            if match:
                result['match_details'] = {'matched_text': match.group()}

        elif operator == 'contains':
            value = condition['value']
            result['expected_value'] = value
            result['matched'] = value.lower() in field_value.lower()

        elif operator == 'contains_any':
            keywords = condition['keywords']
            result['expected_value'] = keywords
            matched_keywords = [kw for kw in keywords if kw.lower() in field_value.lower()]
            result['matched'] = len(matched_keywords) > 0
            result['match_details'] = {'matched_keywords': matched_keywords}

        elif operator == 'exact_match':
            value = condition['value']
            result['expected_value'] = value
            result['matched'] = field_value.lower() == value.lower()

        # Add more operators as needed...

    except Exception as e:
        result['match_details']['error'] = str(e)
        logger = logging.getLogger('classification.debug')
        logger.error(f"Error evaluating condition: {e}")

    return result
```

### Aggregation Debugging

**Similarity Computation Debugging**:
```python
def debug_similarity_computation(tasks_data, sample_size=10):
    """Debug similarity computation with detailed analysis"""

    logger = logging.getLogger('aggregation.debug')

    if len(tasks_data) < 2:
        logger.warning("Need at least 2 tasks for similarity analysis")
        return

    # Sample tasks for detailed analysis
    sample_indices = np.random.choice(len(tasks_data), min(sample_size, len(tasks_data)), replace=False)
    sample_tasks = [tasks_data[i] for i in sample_indices]

    logger.info(f"Analyzing similarities for {len(sample_tasks)} sample tasks")

    similarity_matrix = np.zeros((len(sample_tasks), len(sample_tasks)))

    for i in range(len(sample_tasks)):
        for j in range(i + 1, len(sample_tasks)):
            task1 = sample_tasks[i]
            task2 = sample_tasks[j]

            similarity = calculate_similarity(task1['text'], task2['text'])

            similarity_matrix[i, j] = similarity
            similarity_matrix[j, i] = similarity

            if similarity > 0.5:  # Log significant similarities
                logger.debug(f"High similarity ({similarity:.3f}) between:")
                logger.debug(f"  Task {i}: {task1['text'][:100]}...")
                logger.debug(f"  Task {j}: {task2['text'][:100]}...")

    # Analyze similarity distribution
    similarities = similarity_matrix[np.triu_indices(len(sample_tasks), k=1)]
    similarity_stats = {
        'mean': np.mean(similarities),
        'median': np.median(similarities),
        'std': np.std(similarities),
        'min': np.min(similarities),
        'max': np.max(similarities),
        'percentiles': {
            '25th': np.percentile(similarities, 25),
            '75th': np.percentile(similarities, 75),
            '90th': np.percentile(similarities, 90),
            '95th': np.percentile(similarities, 95)
        }
    }

    logger.info("Similarity Statistics:")
    for stat, value in similarity_stats.items():
        if isinstance(value, dict):
            logger.info(f"  {stat}: {value}")
        else:
            logger.info(f"  {stat}: {value:.3f}")

    # Save debug data
    debug_data = {
        'sample_size': len(sample_tasks),
        'similarity_matrix': similarity_matrix.tolist(),
        'similarity_stats': similarity_stats,
        'sample_task_texts': [task['text'] for task in sample_tasks]
    }
    debug_collector.save_intermediate_state('aggregation', 'similarity_analysis', debug_data)

    return similarity_stats
```

**Clustering Process Debugging**:
```python
def debug_clustering_process(tasks_data, similarity_threshold=0.88):
    """Debug the clustering process step by step"""

    logger = logging.getLogger('aggregation.debug')

    logger.info(f"Starting clustering with {len(tasks_data)} tasks, threshold={similarity_threshold}")

    # Step 1: Compute all pairwise similarities
    logger.info("Step 1: Computing pairwise similarities...")
    similarity_pairs = []

    total_computations = len(tasks_data) * (len(tasks_data) - 1) // 2
    logger.info(f"Total similarity computations needed: {total_computations}")

    computation_count = 0
    for i in range(len(tasks_data)):
        for j in range(i + 1, len(tasks_data)):
            similarity = calculate_similarity(tasks_data[i]['text'], tasks_data[j]['text'])
            computation_count += 1

            if computation_count % 1000 == 0:
                logger.debug(f"Computed {computation_count}/{total_computations} similarities")

            if similarity >= similarity_threshold:
                similarity_pairs.append((i, j, similarity))

    logger.info(f"Found {len(similarity_pairs)} similar pairs above threshold")

    # Step 2: Build clusters
    logger.info("Step 2: Building clusters from similar pairs...")
    clusters = {}

    for pair in similarity_pairs:
        i, j, similarity = pair

        # Find existing clusters for these tasks
        i_cluster = None
        j_cluster = None

        for cluster_id, cluster_tasks in clusters.items():
            if i in cluster_tasks:
                i_cluster = cluster_id
            if j in cluster_tasks:
                j_cluster = cluster_id

        if i_cluster is None and j_cluster is None:
            # Both tasks are new, create new cluster
            new_cluster_id = len(clusters)
            clusters[new_cluster_id] = [i, j]
            logger.debug(f"Created cluster {new_cluster_id} with tasks {i} and {j}")
        elif i_cluster is not None and j_cluster is None:
            # Add j to i's cluster
            clusters[i_cluster].append(j)
            logger.debug(f"Added task {j} to cluster {i_cluster}")
        elif i_cluster is None and j_cluster is not None:
            # Add i to j's cluster
            clusters[j_cluster].append(i)
            logger.debug(f"Added task {i} to cluster {j_cluster}")
        elif i_cluster != j_cluster:
            # Merge clusters
            clusters[i_cluster].extend(clusters[j_cluster])
            del clusters[j_cluster]
            logger.debug(f"Merged cluster {j_cluster} into cluster {i_cluster}")

    # Step 3: Create singleton clusters for unclustered tasks
    logger.info("Step 3: Creating singleton clusters...")
    clustered_tasks = set()
    for cluster_tasks in clusters.values():
        clustered_tasks.update(cluster_tasks)

    singleton_count = 0
    for i in range(len(tasks_data)):
        if i not in clustered_tasks:
            new_cluster_id = len(clusters)
            clusters[new_cluster_id] = [i]
            singleton_count += 1

    logger.info(f"Created {singleton_count} singleton clusters")

    # Step 4: Analyze cluster quality
    logger.info("Step 4: Analyzing cluster quality...")
    cluster_stats = analyze_cluster_quality(clusters, tasks_data, similarity_threshold)

    # Save debug data
    debug_data = {
        'input_parameters': {
            'total_tasks': len(tasks_data),
            'similarity_threshold': similarity_threshold,
            'total_computations': total_computations
        },
        'clustering_results': {
            'total_clusters': len(clusters),
            'clustered_tasks': len(clustered_tasks),
            'singleton_clusters': singleton_count,
            'similar_pairs_found': len(similarity_pairs)
        },
        'cluster_details': [
            {
                'cluster_id': cid,
                'size': len(tasks),
                'task_indices': tasks,
                'task_texts': [tasks_data[idx]['text'][:100] + '...' for idx in tasks[:3]]  # First 3 tasks
            }
            for cid, tasks in clusters.items()
        ],
        'quality_metrics': cluster_stats
    }
    debug_collector.save_intermediate_state('aggregation', 'clustering_process', debug_data)

    logger.info(f"Clustering completed: {len(clusters)} clusters created")
    return clusters

def analyze_cluster_quality(clusters, tasks_data, similarity_threshold):
    """Analyze the quality of formed clusters"""

    stats = {
        'total_clusters': len(clusters),
        'cluster_sizes': {},
        'intra_cluster_similarities': [],
        'inter_cluster_similarities': []
    }

    # Analyze cluster sizes
    sizes = [len(tasks) for tasks in clusters.values()]
    stats['cluster_sizes'] = {
        'min': min(sizes),
        'max': max(sizes),
        'mean': sum(sizes) / len(sizes),
        'distribution': {}
    }

    # Size distribution
    size_bins = [(1, 1), (2, 5), (6, 10), (11, 50), (51, float('inf'))]
    for min_size, max_size in size_bins:
        count = sum(1 for size in sizes if min_size <= size <= max_size)
        bin_name = f"{min_size}-{max_size if max_size != float('inf') else '+'}"
        stats['cluster_sizes']['distribution'][bin_name] = count

    # Sample intra-cluster similarities (for non-singleton clusters)
    for cluster_tasks in clusters.values():
        if len(cluster_tasks) > 1:
            # Sample similarities within cluster
            sample_similarities = []
            for i in range(min(len(cluster_tasks), 5)):  # Sample up to 5 pairs per cluster
                for j in range(i + 1, min(len(cluster_tasks), i + 6)):
                    if j < len(cluster_tasks):
                        sim = calculate_similarity(
                            tasks_data[cluster_tasks[i]]['text'],
                            tasks_data[cluster_tasks[j]]['text']
                        )
                        sample_similarities.append(sim)

            if sample_similarities:
                stats['intra_cluster_similarities'].extend(sample_similarities)

    return stats
```

### Thematic Clustering Debugging

**Theme Assignment Debugging**:
```python
def debug_theme_assignment(tasks_data, themes_config):
    """Debug thematic clustering assignment process"""

    logger = logging.getLogger('clustering.debug')

    assignment_results = []

    logger.info(f"Starting theme assignment for {len(tasks_data)} tasks")

    for i, task in enumerate(tasks_data):
        task_text = task['text']
        logger.debug(f"Processing task {i}: {task_text[:100]}...")

        # Evaluate each theme
        theme_scores = {}

        for theme_name, theme_keywords in themes_config.items():
            confidence, matched_keywords = evaluate_theme_match(task_text, theme_keywords)
            theme_scores[theme_name] = {
                'confidence': confidence,
                'matched_keywords': matched_keywords
            }

            if confidence > 0:
                logger.debug(f"  Theme '{theme_name}': confidence={confidence:.3f}, matches={matched_keywords}")

        # Select best theme
        best_theme = max(theme_scores.items(), key=lambda x: x[1]['confidence'])

        if best_theme[1]['confidence'] >= themes_config.get('confidence_threshold', 0.6):
            assigned_theme = best_theme[0]
            confidence = best_theme[1]['confidence']
            matched_keywords = best_theme[1]['matched_keywords']

            logger.debug(f"Task {i} assigned to theme '{assigned_theme}' with confidence {confidence:.3f}")
        else:
            assigned_theme = 'unassigned'
            confidence = 0.0
            matched_keywords = []

            logger.debug(f"Task {i} remains unassigned (max confidence: {best_theme[1]['confidence']:.3f})")

        assignment_result = {
            'task_index': i,
            'task_text': task_text,
            'assigned_theme': assigned_theme,
            'confidence': confidence,
            'matched_keywords': matched_keywords,
            'all_theme_scores': theme_scores
        }

        assignment_results.append(assignment_result)

    # Summary statistics
    theme_counts = {}
    confidence_distribution = {'high': 0, 'medium': 0, 'low': 0, 'unassigned': 0}

    for result in assignment_results:
        theme = result['assigned_theme']
        theme_counts[theme] = theme_counts.get(theme, 0) + 1

        if theme == 'unassigned':
            confidence_distribution['unassigned'] += 1
        elif result['confidence'] >= 0.8:
            confidence_distribution['high'] += 1
        elif result['confidence'] >= 0.6:
            confidence_distribution['medium'] += 1
        else:
            confidence_distribution['low'] += 1

    logger.info("Theme Assignment Summary:")
    logger.info(f"  Total tasks: {len(assignment_results)}")
    for theme, count in theme_counts.items():
        percentage = (count / len(assignment_results)) * 100
        logger.info(f"  {theme}: {count} tasks ({percentage:.1f}%)")

    logger.info("Confidence Distribution:")
    for level, count in confidence_distribution.items():
        percentage = (count / len(assignment_results)) * 100
        logger.info(f"  {level}: {count} tasks ({percentage:.1f}%)")

    # Save debug data
    debug_data = {
        'assignment_results': assignment_results,
        'summary_stats': {
            'theme_counts': theme_counts,
            'confidence_distribution': confidence_distribution,
            'total_tasks': len(assignment_results)
        }
    }
    debug_collector.save_intermediate_state('clustering', 'theme_assignment', debug_data)

    return assignment_results
```

## Performance Debugging

### Memory Profiling

**Memory Usage Analysis**:
```python
def profile_memory_usage(func, *args, **kwargs):
    """Profile memory usage of a function"""

    import tracemalloc
    import psutil
    import os

    process = psutil.Process(os.getpid())

    # Start memory tracing
    tracemalloc.start()

    # Record initial memory
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    initial_tracemalloc = tracemalloc.get_traced_memory()

    logger = logging.getLogger('performance.debug')
    logger.info(f"Starting memory profiling - Initial memory: {initial_memory:.1f} MB")

    try:
        # Execute function
        result = func(*args, **kwargs)

        # Record final memory
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        final_tracemalloc = tracemalloc.get_traced_memory()

        memory_delta = final_memory - initial_memory
        logger.info(f"Memory profiling completed - Final memory: {final_memory:.1f} MB (Δ{memory_delta:+.1f} MB)")

        # Get memory allocation statistics
        stats = tracemalloc.get_stats()
        logger.info("Top memory allocations:")
        for stat in stats[:10]:  # Top 10
            logger.info(f"  {stat.filename}:{stat.lineno} - {stat.size / 1024:.1f} KB ({stat.count} allocations)")

        # Get traceback of largest allocations
        tracebacks = tracemalloc.get_traceback_limit()
        tracemalloc.set_traceback_limit(25)

        logger.info("Largest memory allocations:")
        for i, (size, count, traceback) in enumerate(tracemalloc.get_traced_memory()[2][:5]):
            logger.info(f"  Allocation {i+1}: {size / 1024:.1f} KB")
            for frame in traceback:
                logger.info(f"    {frame.filename}:{frame.lineno} in {frame.name}")

        return result, {
            'initial_memory_mb': initial_memory,
            'final_memory_mb': final_memory,
            'memory_delta_mb': memory_delta,
            'peak_memory_mb': max(initial_memory, final_memory),
            'tracemalloc_stats': [(stat.filename, stat.lineno, stat.size) for stat in stats[:10]]
        }

    finally:
        tracemalloc.stop()
```

### CPU Profiling

**Function Performance Analysis**:
```python
def profile_function_performance(func, *args, **kwargs):
    """Profile CPU performance of a function"""

    import cProfile
    import pstats
    from io import StringIO

    pr = cProfile.Profile()
    pr.enable()

    try:
        result = func(*args, **kwargs)
    finally:
        pr.disable()

    # Analyze profiling results
    s = StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(20)  # Top 20 functions

    profiling_results = s.getvalue()

    # Extract key metrics
    stats = pstats.Stats(pr)
    total_calls = stats.total_calls
    total_time = stats.total_tt

    logger = logging.getLogger('performance.debug')
    logger.info(f"Function profiling completed:")
    logger.info(f"  Total function calls: {total_calls}")
    logger.info(f"  Total execution time: {total_time:.3f} seconds")
    logger.info("Top time-consuming functions:")
    for line in profiling_results.split('\n')[:25]:  # First 25 lines
        if line.strip():
            logger.info(f"  {line}")

    return result, {
        'total_calls': total_calls,
        'total_time': total_time,
        'profiling_output': profiling_results
    }
```

### Bottleneck Identification

**Pipeline Stage Timing**:
```python
import time
from contextlib import contextmanager

@contextmanager
def time_stage(stage_name):
    """Context manager to time pipeline stages"""

    logger = logging.getLogger('performance.debug')
    logger.info(f"Starting stage: {stage_name}")

    start_time = time.time()
    start_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

    try:
        yield
    finally:
        end_time = time.time()
        end_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

        duration = end_time - start_time
        memory_delta = end_memory - start_memory

        logger.info(f"Stage '{stage_name}' completed:")
        logger.info(f"  Duration: {duration:.2f} seconds")
        logger.info(f"  Memory delta: {memory_delta:+.1f} MB")
        logger.info(f"  Final memory: {end_memory:.1f} MB")

        # Save timing data
        timing_data = {
            'stage_name': stage_name,
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration,
            'start_memory_mb': start_memory,
            'end_memory_mb': end_memory,
            'memory_delta_mb': memory_delta
        }
        debug_collector.save_intermediate_state('performance', f'{stage_name}_timing', timing_data)
```

## Interactive Debugging

### Debug Console

**Interactive Debug Session**:
```python
def start_debug_console(global_vars=None):
    """Start an interactive debug console"""

    import code
    import readline

    # Set up console banner
    banner = """
SOC Job Task Analyzer - Debug Console
=====================================
Available variables:
- debug_collector: DebugDataCollector instance
- jobs_data: Current job data (if loaded)
- tasks_data: Current task data (if processed)
- clusters: Current clusters (if computed)
- themes: Current theme assignments (if computed)

Type 'help' for available commands or 'quit' to exit.
"""

    # Prepare console environment
    console_vars = {
        'debug_collector': debug_collector,
        'help': lambda: print_debug_help(),
        'quit': lambda: None
    }

    if global_vars:
        console_vars.update(global_vars)

    # Start interactive console
    try:
        code.interact(banner=banner, local=console_vars, exitmsg="Debug console exited.")
    except KeyboardInterrupt:
        print("\nDebug console interrupted.")

def print_debug_help():
    """Print debug console help"""

    help_text = """
Debug Console Commands:
======================

Data Inspection:
  jobs_data[:5]          - View first 5 jobs
  len(tasks_data)        - Count of processed tasks
  clusters.keys()        - Available cluster IDs
  themes[:10]           - First 10 theme assignments

Debug Data:
  debug_collector.debug_dir - Debug data directory
  list_debug_files()        - List saved debug files
  load_debug_data(filename) - Load debug data file

Analysis Functions:
  analyze_job(job_index)    - Analyze specific job
  analyze_cluster(cluster_id) - Analyze specific cluster
  compare_similarities(task1_idx, task2_idx) - Compare task similarities

Performance:
  profile_function(func)    - Profile function performance
  memory_usage()           - Current memory usage

Utilities:
  save_current_state()      - Save current pipeline state
  export_debug_report()     - Export comprehensive debug report
  clear_debug_data()        - Clear debug data directory

Type variable names directly to inspect them.
"""
    print(help_text)

def list_debug_files():
    """List available debug data files"""

    debug_dir = debug_collector.debug_dir
    if debug_dir.exists():
        files = list(debug_dir.glob("*.pkl")) + list(debug_dir.glob("*.json"))
        for file in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True):
            size_mb = file.stat().st_size / 1024 / 1024
            print(f"  {file.name} ({size_mb:.2f} MB)")
    else:
        print("No debug directory found")

def load_debug_data(filename):
    """Load debug data from file"""

    import pickle
    import json

    filepath = debug_collector.debug_dir / filename

    if filepath.exists():
        if filename.endswith('.pkl'):
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        elif filename.endswith('.json'):
            with open(filepath, 'r') as f:
                return json.load(f)
    else:
        print(f"Debug file not found: {filename}")
        return None
```

### Debug Report Generation

**Comprehensive Debug Report**:
```python
def generate_debug_report():
    """Generate comprehensive debug report"""

    from datetime import datetime
    import json

    report = {
        'report_metadata': {
            'generated_at': datetime.now().isoformat(),
            'execution_id': debug_collector.execution_id,
            'report_version': '1.0'
        },
        'system_info': get_system_info(),
        'configuration_summary': get_configuration_summary(),
        'pipeline_execution_summary': get_pipeline_execution_summary(),
        'performance_metrics': get_performance_metrics(),
        'error_summary': get_error_summary(),
        'data_quality_metrics': get_data_quality_metrics(),
        'recommendations': generate_debug_recommendations()
    }

    # Save report
    report_file = debug_collector.debug_dir / f"debug_report_{debug_collector.execution_id}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)

    logger = logging.getLogger('debug.report')
    logger.info(f"Debug report generated: {report_file}")

    return report

def get_system_info():
    """Get system information for debug report"""

    import platform
    import psutil

    return {
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'cpu_count': psutil.cpu_count(),
        'total_memory_gb': psutil.virtual_memory().total / (1024**3),
        'available_memory_gb': psutil.virtual_memory().available / (1024**3)
    }

def get_configuration_summary():
    """Summarize current configuration"""

    try:
        with open('configs/pipeline_config.json', 'r') as f:
            config = json.load(f)

        return {
            'pipeline_version': config['pipeline'].get('version'),
            'stages': config['pipeline'].get('stages'),
            'data_collection': {
                'api_provider': config['data_collection'].get('api_provider'),
                'search_queries_count': len(config['data_collection'].get('search_queries', []))
            },
            'classification': {
                'rules_file': config['job_classification'].get('rules_file'),
                'threshold': config['job_classification'].get('classification_threshold')
            },
            'aggregation': {
                'similarity_threshold': config['task_aggregation'].get('similarity_threshold'),
                'batch_size': config['task_aggregation'].get('processing_batch_size')
            }
        }
    except Exception as e:
        return {'error': str(e)}

def generate_debug_recommendations():
    """Generate debugging recommendations based on collected data"""

    recommendations = []

    # Check for common issues
    try:
        # Load latest debug data
        debug_files = list(debug_collector.debug_dir.glob("*.json"))
        if debug_files:
            latest_file = max(debug_files, key=lambda x: x.stat().st_mtime)
            with open(latest_file, 'r') as f:
                debug_data = json.load(f)

            # Analyze error patterns
            if 'error_summary' in debug_data and debug_data['error_summary'].get('total_errors', 0) > 0:
                recommendations.append({
                    'priority': 'high',
                    'category': 'errors',
                    'recommendation': 'Review error logs and address root causes',
                    'details': f"{debug_data['error_summary']['total_errors']} errors detected"
                })

            # Check performance
            if 'performance_metrics' in debug_data:
                perf = debug_data['performance_metrics']
                if perf.get('memory_usage_mb', 0) > 2000:  # > 2GB
                    recommendations.append({
                        'priority': 'medium',
                        'category': 'performance',
                        'recommendation': 'Consider memory optimization techniques',
                        'details': f"High memory usage: {perf['memory_usage_mb']} MB"
                    })

    except Exception as e:
        recommendations.append({
            'priority': 'low',
            'category': 'debugging',
            'recommendation': 'Debug data analysis failed',
            'details': str(e)
        })

    # General recommendations
    recommendations.extend([
        {
            'priority': 'low',
            'category': 'monitoring',
            'recommendation': 'Enable detailed logging for production runs',
            'details': 'Set LOG_LEVEL=DEBUG in environment variables'
        },
        {
            'priority': 'low',
            'category': 'data_quality',
            'recommendation': 'Implement data validation checks',
            'details': 'Add schema validation for input and output data'
        }
    ])

    return recommendations
```

This comprehensive debugging guide provides systematic approaches to identify, analyze, and resolve issues across all SOC Job Task Analyzer pipeline stages, ensuring reliable operation and maintenance.

---

**Last Updated:** December 2024
**Version:** 1.0.0
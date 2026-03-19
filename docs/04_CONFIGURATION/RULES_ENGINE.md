# Rules Engine Configuration

## Overview

The SOC Job Task Analyzer employs a configurable rules-based classification system to identify SOC (Security Operations Center) positions from job postings. This document details the rules engine architecture, configuration format, and optimization strategies for accurate job classification.

## Rules Engine Architecture

### Core Components

**Rule Processor**: `src/data_analyzer.py::apply_classification_rules()`
- Loads rules from `configs/rules.json`
- Applies pattern matching against job titles and descriptions
- Returns boolean classification results with confidence scores

**Rule Structure**:
```json
{
  "rules": [
    {
      "rule_id": "soc_tier1_basic",
      "description": "Basic SOC Tier 1 analyst identification",
      "conditions": [
        {
          "field": "title",
          "operator": "regex_match",
          "pattern": "(?i)(soc|security operations center).*analyst",
          "weight": 0.8
        },
        {
          "field": "description",
          "operator": "contains_any",
          "keywords": ["threat detection", "incident response", "log analysis"],
          "weight": 0.6
        }
      ],
      "threshold": 0.7,
      "exclusions": [
        {
          "field": "title",
          "operator": "contains",
          "value": "senior",
          "reason": "Exclude senior positions for Tier 1 focus"
        }
      ]
    }
  ]
}
```

### Rule Evaluation Logic

**Weighted Scoring System**:
```python
def evaluate_rule(job_data, rule):
    """Evaluate a single rule against job data"""

    total_score = 0.0
    max_score = sum(condition['weight'] for condition in rule['conditions'])

    for condition in rule['conditions']:
        if evaluate_condition(job_data, condition):
            total_score += condition['weight']

    # Check exclusions
    for exclusion in rule.get('exclusions', []):
        if evaluate_condition(job_data, exclusion):
            return 0.0  # Rule fails if any exclusion matches

    # Calculate confidence score
    confidence = total_score / max_score if max_score > 0 else 0.0

    return confidence if confidence >= rule['threshold'] else 0.0
```

## Configuration File Format

### Complete Rules Schema

**File Location**: `configs/rules.json`

**JSON Schema**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "rule_id": {
            "type": "string",
            "description": "Unique identifier for the rule"
          },
          "description": {
            "type": "string",
            "description": "Human-readable description of the rule's purpose"
          },
          "conditions": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "field": {
                  "type": "string",
                  "enum": ["title", "description", "company", "location"],
                  "description": "Job field to evaluate"
                },
                "operator": {
                  "type": "string",
                  "enum": ["regex_match", "contains", "contains_any", "exact_match", "starts_with", "ends_with"],
                  "description": "Comparison operator"
                },
                "pattern": {
                  "type": "string",
                  "description": "Regex pattern for regex_match operator"
                },
                "keywords": {
                  "type": "array",
                  "items": {"type": "string"},
                  "description": "Keyword list for contains_any operator"
                },
                "value": {
                  "type": "string",
                  "description": "Value for exact_match, contains, starts_with, ends_with operators"
                },
                "case_sensitive": {
                  "type": "boolean",
                  "default": false,
                  "description": "Whether comparison is case sensitive"
                },
                "weight": {
                  "type": "number",
                  "minimum": 0.0,
                  "maximum": 1.0,
                  "description": "Weight of this condition in rule scoring"
                }
              },
              "required": ["field", "operator", "weight"],
              "oneOf": [
                {"required": ["pattern"]},
                {"required": ["keywords"]},
                {"required": ["value"]}
              ]
            }
          },
          "threshold": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
            "description": "Minimum confidence score required for rule to pass"
          },
          "exclusions": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "field": {"type": "string", "enum": ["title", "description", "company", "location"]},
                "operator": {"type": "string", "enum": ["regex_match", "contains", "contains_any", "exact_match"]},
                "pattern": {"type": "string"},
                "keywords": {"type": "array", "items": {"type": "string"}},
                "value": {"type": "string"},
                "case_sensitive": {"type": "boolean", "default": false},
                "reason": {"type": "string", "description": "Reason for exclusion"}
              },
              "required": ["field", "operator", "reason"]
            },
            "description": "Conditions that disqualify a job even if other conditions pass"
          },
          "metadata": {
            "type": "object",
            "properties": {
              "author": {"type": "string"},
              "created_date": {"type": "string", "format": "date"},
              "last_modified": {"type": "string", "format": "date-time"},
              "validation_status": {"type": "string", "enum": ["draft", "validated", "deprecated"]},
              "performance_metrics": {
                "type": "object",
                "properties": {
                  "precision": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                  "recall": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                  "f1_score": {"type": "number", "minimum": 0.0, "maximum": 1.0}
                }
              }
            }
          }
        },
        "required": ["rule_id", "description", "conditions", "threshold"]
      }
    },
    "global_settings": {
      "type": "object",
      "properties": {
        "default_threshold": {"type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.5},
        "case_sensitive_default": {"type": "boolean", "default": false},
        "max_rules_per_job": {"type": "integer", "minimum": 1, "default": 5},
        "rule_evaluation_timeout_ms": {"type": "integer", "minimum": 100, "default": 5000}
      }
    }
  },
  "required": ["rules"]
}
```

## Current Rules Configuration

### SOC Tier 1 Analyst Rules

**Primary Classification Rule**:
```json
{
  "rule_id": "soc_tier1_analyst",
  "description": "Identifies entry-level SOC analyst positions",
  "conditions": [
    {
      "field": "title",
      "operator": "regex_match",
      "pattern": "(?i)(soc|security operations center|security operations).*analyst",
      "weight": 0.9
    },
    {
      "field": "description",
      "operator": "contains_any",
      "keywords": [
        "threat detection",
        "incident response",
        "log analysis",
        "security monitoring",
        "alert triage",
        "vulnerability scanning",
        "threat hunting",
        "forensic analysis"
      ],
      "weight": 0.7
    },
    {
      "field": "description",
      "operator": "contains_any",
      "keywords": [
        "24/7 monitoring",
        "shift work",
        "rotating shifts",
        "tier 1",
        "level 1",
        "junior analyst"
      ],
      "weight": 0.4
    }
  ],
  "threshold": 0.8,
  "exclusions": [
    {
      "field": "title",
      "operator": "regex_match",
      "pattern": "(?i)(senior|lead|principal|manager|director)",
      "reason": "Exclude senior/managerial positions"
    },
    {
      "field": "description",
      "operator": "contains_any",
      "keywords": ["team lead", "supervise", "manage team", "leadership"],
      "reason": "Exclude positions with leadership responsibilities"
    }
  ]
}
```

### Specialized SOC Role Rules

**SOC Engineer Rule**:
```json
{
  "rule_id": "soc_engineer",
  "description": "Identifies SOC engineering and technical positions",
  "conditions": [
    {
      "field": "title",
      "operator": "regex_match",
      "pattern": "(?i)(soc|security operations).*engineer",
      "weight": 0.8
    },
    {
      "field": "description",
      "operator": "contains_any",
      "keywords": [
        "tool configuration",
        "automation",
        "scripting",
        "SIEM",
        "splunk",
        "elastic",
        "wireshark",
        "python",
        "bash"
      ],
      "weight": 0.6
    }
  ],
  "threshold": 0.7
}
```

### Industry-Specific Rules

**Financial Services SOC**:
```json
{
  "rule_id": "financial_soc",
  "description": "SOC positions in financial services sector",
  "conditions": [
    {
      "field": "company",
      "operator": "contains_any",
      "keywords": ["bank", "finance", "financial", "capital", "investment"],
      "weight": 0.3
    },
    {
      "field": "description",
      "operator": "contains_any",
      "keywords": ["PCI DSS", "SOX", "regulatory compliance", "financial security"],
      "weight": 0.4
    }
  ],
  "threshold": 0.6
}
```

## Rule Development and Testing

### Rule Validation Framework

**Performance Metrics Calculation**:
```python
def validate_rule_performance(rule, test_dataset):
    """Validate rule performance against labeled test data"""

    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0

    for job, expected_soc in test_dataset:
        prediction = evaluate_rule(job, rule) > rule['threshold']

        if prediction and expected_soc:
            true_positives += 1
        elif prediction and not expected_soc:
            false_positives += 1
        elif not prediction and not expected_soc:
            true_negatives += 1
        elif not prediction and expected_soc:
            false_negatives += 1

    # Calculate metrics
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'accuracy': (true_positives + true_negatives) / len(test_dataset)
    }
```

### Rule Optimization Strategies

**Pattern Mining for New Rules**:
```python
def discover_new_patterns(jobs_data, min_support=0.05):
    """Discover frequent patterns in SOC job postings for rule creation"""

    from collections import Counter

    # Extract title patterns
    title_patterns = []
    for job in jobs_data:
        # Tokenize and normalize title
        tokens = tokenize_title(job['title'])
        title_patterns.extend(tokens)

    # Find frequent patterns
    pattern_counts = Counter(title_patterns)
    frequent_patterns = {
        pattern: count for pattern, count in pattern_counts.items()
        if count / len(jobs_data) >= min_support
    }

    return frequent_patterns
```

### A/B Testing Framework

**Rule Comparison System**:
```python
def compare_rules(rule_a, rule_b, test_dataset):
    """Compare performance of two rule variants"""

    metrics_a = validate_rule_performance(rule_a, test_dataset)
    metrics_b = validate_rule_performance(rule_b, test_dataset)

    comparison = {
        'rule_a': {
            'metrics': metrics_a,
            'rule_config': rule_a
        },
        'rule_b': {
            'metrics': metrics_b,
            'rule_config': rule_b
        },
        'improvement': {
            'precision_delta': metrics_b['precision'] - metrics_a['precision'],
            'recall_delta': metrics_b['recall'] - metrics_a['recall'],
            'f1_delta': metrics_b['f1_score'] - metrics_a['f1_score']
        }
    }

    return comparison
```

## Configuration Management

### Version Control for Rules

**Rules Versioning Strategy**:
```json
{
  "rules_version": "1.2.0",
  "changelog": [
    {
      "version": "1.2.0",
      "date": "2024-12-01",
      "changes": [
        "Added financial services specific rules",
        "Improved exclusion patterns for senior positions",
        "Enhanced keyword coverage for threat hunting"
      ],
      "performance_impact": {
        "precision_improvement": 0.03,
        "recall_improvement": 0.05
      }
    }
  ],
  "validation_history": [
    {
      "validation_date": "2024-12-01",
      "test_dataset_size": 500,
      "overall_f1_score": 0.87,
      "validation_status": "passed"
    }
  ]
}
```

### Rules Deployment Pipeline

**Automated Validation and Deployment**:
```python
def deploy_rules_update(new_rules_config, test_dataset):
    """Deploy rules update with automated validation"""

    # Validate new rules
    validation_results = validate_rules_config(new_rules_config, test_dataset)

    if validation_results['status'] == 'failed':
        raise ValueError(f"Rules validation failed: {validation_results['errors']}")

    # Performance regression check
    if validation_results['metrics']['f1_score'] < 0.85:  # Minimum threshold
        raise ValueError("Rules update would degrade performance below threshold")

    # Backup current rules
    backup_current_rules()

    # Deploy new rules
    save_rules_config(new_rules_config)

    # Log deployment
    log_deployment(validation_results)

    return {
        'status': 'deployed',
        'performance_metrics': validation_results['metrics'],
        'deployment_timestamp': datetime.now().isoformat()
    }
```

## Troubleshooting Rule Issues

### Common Rule Problems

**False Positives Analysis**:
```python
def analyze_false_positives(predictions, actuals, jobs_data):
    """Analyze patterns in false positive classifications"""

    false_positives = []
    for i, (predicted, actual) in enumerate(zip(predictions, actuals)):
        if predicted and not actual:
            false_positives.append({
                'job_index': i,
                'job_title': jobs_data[i]['title'],
                'job_description': jobs_data[i]['description'][:200] + '...',
                'matched_conditions': get_matched_conditions(jobs_data[i], rule),
                'failure_reason': identify_failure_reason(jobs_data[i], rule)
            })

    # Group by failure patterns
    from collections import Counter
    failure_patterns = Counter(fp['failure_reason'] for fp in false_positives)

    return {
        'false_positives': false_positives,
        'failure_patterns': dict(failure_patterns),
        'recommendations': generate_fix_recommendations(failure_patterns)
    }
```

### Rule Performance Monitoring

**Continuous Performance Tracking**:
```python
def monitor_rule_performance(production_data, window_days=30):
    """Monitor rule performance on production data"""

    recent_jobs = get_recent_jobs(window_days)
    predictions = classify_jobs_batch(recent_jobs)

    # Calculate rolling performance metrics
    metrics = calculate_performance_metrics(predictions, recent_jobs)

    # Alert on performance degradation
    if metrics['f1_score'] < 0.80:  # Alert threshold
        alert_performance_degradation(metrics)

    # Log metrics for trend analysis
    log_performance_metrics(metrics, window_days)

    return metrics
```

This rules engine provides a flexible, maintainable system for SOC job classification with comprehensive validation, optimization, and monitoring capabilities to ensure high accuracy and reliability in production environments.

---

**Last Updated:** December 2024
**Version:** 1.0.0
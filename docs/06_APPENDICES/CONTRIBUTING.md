# Contributing Guide

## Welcome

Thank you for your interest in contributing to the SOC Job Task Analyzer project! This document provides guidelines and information for contributors.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Environment](#development-environment)
3. [Code Style and Standards](#code-style-and-standards)
4. [Testing](#testing)
5. [Submitting Changes](#submitting-changes)
6. [Documentation](#documentation)
7. [Issue Reporting](#issue-reporting)
8. [Code Review Process](#code-review-process)
9. [Community Guidelines](#community-guidelines)

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher**
- **Git** for version control
- **Virtual environment tool** (venv, virtualenv, or conda)
- **API Keys** for external services (SerpAPI for job data)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/soc-job-task-analyzer.git
   cd soc-job-task-analyzer
   ```

3. Set up the upstream remote:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/soc-job-task-analyzer.git
   ```

### Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. Run initial tests:
   ```bash
   python -m pytest tests/
   ```

## Development Environment

### Project Structure

```
soc-job-task-analyzer/
├── src/                    # Source code
│   ├── soc_scrapper_API.py     # API integration
│   ├── data_analyzer.py        # Classification logic
│   ├── task_aggregator.py      # Deduplication
│   ├── task_thematic_clusterer.py  # Clustering
│   └── job_run.py              # Pipeline orchestration
├── tests/                  # Test files
├── docs/                   # Documentation
├── configs/                # Configuration files
├── data/                   # Data directories
│   ├── raw/                # Raw input data
│   └── processed/          # Processed output data
├── scripts/                # Utility scripts
└── requirements*.txt       # Dependencies
```

### Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards

3. **Run tests** to ensure nothing is broken:
   ```bash
   python -m pytest tests/
   ```

4. **Run linting and formatting:**
   ```bash
   # Format code
   black src/ tests/

   # Lint code
   flake8 src/ tests/

   # Type checking
   mypy src/
   ```

5. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

## Code Style and Standards

### Python Style Guide

This project follows [PEP 8](https://pep8.org/) with some modifications. We use:

- **Black** for code formatting (line length: 88 characters)
- **Flake8** for linting
- **MyPy** for static type checking
- **isort** for import sorting

### Key Conventions

#### Naming Conventions

```python
# Classes: PascalCase
class DataProcessor:
    pass

# Functions and methods: snake_case
def process_data(data):
    pass

# Constants: UPPER_CASE
MAX_RETRIES = 3

# Private methods: _single_underscore_prefix
def _validate_input(self, data):
    pass
```

#### Docstrings

Use Google-style docstrings for all public functions, classes, and methods:

```python
def process_job_data(jobs_data, config=None):
    """Process job data through the analysis pipeline.

    Args:
        jobs_data (list): List of job dictionaries from API
        config (dict, optional): Processing configuration

    Returns:
        dict: Processed results with metadata

    Raises:
        ValueError: If jobs_data is empty or invalid
        ProcessingError: If pipeline execution fails

    Example:
        >>> result = process_job_data(jobs)
        >>> print(result['summary'])
    """
    pass
```

#### Type Hints

Use type hints for all function parameters and return values:

```python
from typing import List, Dict, Any, Optional

def analyze_jobs(jobs: List[Dict[str, Any]], threshold: float = 0.8) -> Dict[str, Any]:
    """Analyze job data with similarity threshold."""
    pass

def get_job_by_id(job_id: str, jobs: Optional[List[Dict]] = None) -> Optional[Dict]:
    """Retrieve job by ID, returns None if not found."""
    pass
```

#### Error Handling

Use custom exceptions and provide meaningful error messages:

```python
class PipelineError(Exception):
    """Base exception for pipeline errors."""

    def __init__(self, message, stage=None, data=None):
        super().__init__(message)
        self.stage = stage
        self.data = data

def run_pipeline(config):
    """Run the analysis pipeline."""
    try:
        # Pipeline logic
        pass
    except APIError as e:
        raise PipelineError(f"API failure in scraping stage: {e}", stage="scraping") from e
    except ValidationError as e:
        raise PipelineError(f"Data validation failed: {e}", stage="validation") from e
```

#### Logging

Use the logging module with appropriate levels:

```python
import logging

logger = logging.getLogger(__name__)

def process_data(data):
    """Process data with logging."""
    logger.info("Starting data processing")
    logger.debug(f"Processing {len(data)} items")

    try:
        # Processing logic
        logger.info("Data processing completed successfully")
        return result
    except Exception as e:
        logger.error(f"Data processing failed: {e}")
        raise
```

### Import Organization

Organize imports according to PEP 8:

```python
# Standard library imports
import os
import sys
from typing import List, Dict, Any

# Third-party imports
import requests
import pandas as pd

# Local imports
from .data_processor import DataProcessor
from ..utils import helper_function
```

## Testing

### Test Structure

Tests are organized in the `tests/` directory:

```
tests/
├── unit/                   # Unit tests
│   ├── test_api_scraper.py
│   ├── test_classifier.py
│   └── test_aggregator.py
├── integration/            # Integration tests
│   └── test_pipeline.py
├── fixtures/               # Test data
└── conftest.py            # Test configuration
```

### Writing Tests

Use pytest with descriptive test names:

```python
import pytest
from unittest.mock import Mock, patch

class TestDataProcessor:
    """Test cases for DataProcessor class."""

    def test_process_valid_data(self):
        """Test processing of valid job data."""
        # Arrange
        processor = DataProcessor()
        valid_data = [
            {
                "title": "Data Scientist",
                "company": "Tech Corp",
                "description": "Analyze data and build models"
            }
        ]

        # Act
        result = processor.process_data(valid_data)

        # Assert
        assert result is not None
        assert "processed_jobs" in result
        assert len(result["processed_jobs"]) == 1

    def test_process_empty_data_raises_error(self):
        """Test that empty data raises ValueError."""
        processor = DataProcessor()

        with pytest.raises(ValueError, match="Empty data provided"):
            processor.process_data([])

    @patch('requests.get')
    def test_api_call_with_retry(self, mock_get):
        """Test API calls with retry logic."""
        # Mock API failure then success
        mock_get.side_effect = [
            requests.ConnectionError("Network error"),
            Mock(status_code=200, json=lambda: {"data": "success"})
        ]

        result = call_api_with_retry()

        assert result["data"] == "success"
        assert mock_get.call_count == 2
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/unit/test_classifier.py

# Run with coverage
python -m pytest --cov=src --cov-report=html

# Run tests matching pattern
python -m pytest -k "test_process"

# Run tests in verbose mode
python -m pytest -v
```

### Test Coverage Requirements

- **Minimum Coverage:** 85% overall
- **Critical Modules:** 95% coverage for core pipeline modules
- **New Features:** 90% coverage for new code

## Submitting Changes

### Commit Message Format

Use conventional commit format:

```bash
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions/modifications
- `chore`: Maintenance tasks

**Examples:**
```bash
feat: add fuzzy deduplication algorithm
fix: resolve memory leak in data processing
docs: update API reference for new methods
test: add integration tests for pipeline execution
```

### Pull Request Guidelines

1. **Title:** Clear, descriptive title following commit format
2. **Description:** Detailed explanation of changes
3. **Testing:** Describe how changes were tested
4. **Breaking Changes:** Note any breaking changes
5. **Screenshots/Demos:** Include for UI changes
6. **Related Issues:** Reference related issues with #

**PR Template:**
```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed
- [ ] All tests pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added for new functionality
- [ ] No breaking changes
- [ ] Commit messages follow conventions
```

## Documentation

### Documentation Standards

- Use Markdown for all documentation
- Include code examples where relevant
- Keep API documentation up to date
- Use consistent formatting and structure

### Updating Documentation

When making changes that affect documentation:

1. Update relevant `.md` files in `docs/`
2. Update docstrings in code
3. Update API reference if new functions added
4. Test documentation builds correctly

## Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Describe the Bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
A clear description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
- OS: [e.g., Windows 10]
- Python Version: [e.g., 3.10.0]
- Version: [e.g., 1.0.0]

**Additional Context**
Add any other context about the problem here.
```

### Feature Requests

Use the feature request template:

```markdown
**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear description of any alternative solutions or features you've considered.

**Additional Context**
Add any other context or screenshots about the feature request here.
```

## Code Review Process

### Review Checklist

**For Reviewers:**
- [ ] Code follows style guidelines
- [ ] Tests are included and pass
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Error handling is appropriate
- [ ] Code is maintainable and readable

**For Contributors:**
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] Breaking changes documented
- [ ] Commit messages are clear
- [ ] Related issues referenced

### Review Comments

- Be constructive and specific
- Suggest improvements, don't just point out problems
- Reference coding standards when relevant
- Ask questions to understand intent
- Acknowledge good practices

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn and contribute
- Maintain professional communication
- Respect differing viewpoints

### Getting Help

- Check existing documentation first
- Search existing issues and discussions
- Ask clear, specific questions
- Provide context and examples
- Be patient waiting for responses

### Recognition

Contributors are recognized through:
- GitHub contributor statistics
- Mention in release notes
- Attribution in documentation
- Community acknowledgments

---

Thank you for contributing to the SOC Job Task Analyzer project! Your contributions help make this tool better for researchers and analysts worldwide.

**Last Updated:** December 2024
**Version:** 1.0.0
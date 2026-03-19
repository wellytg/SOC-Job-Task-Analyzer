# SOC Job Task Analyzer - Documentation Table of Contents

## Overview
This documentation provides comprehensive guidance for the SOC Job Task Analyzer project, designed for PhD research in cybersecurity workforce analysis. The project scrapes, processes, and analyzes SOC (Security Operations Center) job postings to extract task requirements and identify thematic patterns.

## Documentation Structure

### 01_GETTING_STARTED
- **[README.md](01_GETTING_STARTED/README.md)** - Project overview, quick start guide, and key features
- **[ENVIRONMENT.md](01_GETTING_STARTED/ENVIRONMENT.md)** - Environment setup, dependencies, and system requirements
- **[ARCHITECTURE.md](01_GETTING_STARTED/ARCHITECTURE.md)** - High-level system architecture and data flow
- **[QUICK_START.md](01_GETTING_STARTED/QUICK_START.md)** - Step-by-step setup and first run tutorial

### 02_PIPELINE_REFERENCE
- **[PIPELINE_OVERVIEW.md](02_PIPELINE_REFERENCE/PIPELINE_OVERVIEW.md)** - Complete pipeline walkthrough with examples
- **[SCRAPING_MODULE.md](02_PIPELINE_REFERENCE/SCRAPING_MODULE.md)** - Data collection and API integration details
- **[CLASSIFICATION_MODULE.md](02_PIPELINE_REFERENCE/CLASSIFICATION_MODULE.md)** - Job title classification and filtering logic
- **[AGGREGATION_MODULE.md](02_PIPELINE_REFERENCE/AGGREGATION_MODULE.md)** - Task consolidation and deduplication algorithms
- **[CLUSTERING_MODULE.md](02_PIPELINE_REFERENCE/CLUSTERING_MODULE.md)** - Thematic clustering and pre-LLM processing

### 03_DATA_SCHEMA
- **[RAW_DATA_SCHEMA.md](03_DATA_SCHEMA/RAW_DATA_SCHEMA.md)** - API response formats and raw data structures
- **[PROCESSED_DATA_SCHEMA.md](03_DATA_SCHEMA/PROCESSED_DATA_SCHEMA.md)** - Intermediate processing outputs
- **[FINAL_OUTPUT_SCHEMA.md](03_DATA_SCHEMA/FINAL_OUTPUT_SCHEMA.md)** - LLM-ready data formats and validation

### 04_CONFIGURATION
- **[RULES_ENGINE.md](04_CONFIGURATION/RULES_ENGINE.md)** - Classification rules configuration and customization
- **[PIPELINE_CONFIG.md](04_CONFIGURATION/PIPELINE_CONFIG.md)** - Runtime parameters and execution options
- **[ENVIRONMENT_VARIABLES.md](04_CONFIGURATION/ENVIRONMENT_VARIABLES.md)** - API keys, paths, and environment management

### 05_TROUBLESHOOTING
- **[COMMON_ISSUES.md](05_TROUBLESHOOTING/COMMON_ISSUES.md)** - Frequently encountered problems and solutions
- **[DEBUGGING_GUIDE.md](05_TROUBLESHOOTING/DEBUGGING_GUIDE.md)** - Debugging tools and techniques
- **[PERFORMANCE_OPTIMIZATION.md](05_TROUBLESHOOTING/PERFORMANCE_OPTIMIZATION.md)** - Optimization strategies and benchmarking

### 06_APPENDICES
- **[GLOSSARY.md](06_APPENDICES/GLOSSARY.md)** - Technical terms and definitions
- **[API_REFERENCE.md](06_APPENDICES/API_REFERENCE.md)** - Complete API documentation
- **[CHANGELOG.md](06_APPENDICES/CHANGELOG.md)** - Version history and feature updates
- **[CONTRIBUTING.md](06_APPENDICES/CONTRIBUTING.md)** - Guidelines for extending the project

## Quick Navigation

### For New Users
1. Start with [QUICK_START.md](01_GETTING_STARTED/QUICK_START.md)
2. Review [ENVIRONMENT.md](01_GETTING_STARTED/ENVIRONMENT.md)
3. Run the pipeline using [PIPELINE_OVERVIEW.md](02_PIPELINE_REFERENCE/PIPELINE_OVERVIEW.md)

### For Developers
1. Understand architecture in [ARCHITECTURE.md](01_GETTING_STARTED/ARCHITECTURE.md)
2. Review module details in [02_PIPELINE_REFERENCE/](02_PIPELINE_REFERENCE/)
3. Check data schemas in [03_DATA_SCHEMA/](03_DATA_SCHEMA/)

### For Researchers
1. Review [FINAL_OUTPUT_SCHEMA.md](03_DATA_SCHEMA/FINAL_OUTPUT_SCHEMA.md)
2. Understand clustering in [CLUSTERING_MODULE.md](02_PIPELINE_REFERENCE/CLUSTERING_MODULE.md)
3. See validation methods in [DEBUGGING_GUIDE.md](05_TROUBLESHOOTING/DEBUGGING_GUIDE.md)

## File Organization Standards

### Naming Conventions
- Files use `UPPER_SNAKE_CASE.md` format
- Directories use `01_PREFIX_DESCRIPTIVE_NAME` format
- Code files follow `snake_case.py` convention

### Content Standards
- All documentation includes last updated dates
- Code examples are tested and runnable
- Cross-references use relative markdown links
- Tables of contents provided for documents >5 sections

### Version Control
- Documentation updates tracked in [CHANGELOG.md](06_APPENDICES/CHANGELOG.md)
- Major versions (1.x) include documentation reviews
- Minor versions (x.1) may include documentation patches

---

**Last Updated:** December 2024
**Version:** 1.0.0
**Authors:** SOC Job Task Analyzer Development Team
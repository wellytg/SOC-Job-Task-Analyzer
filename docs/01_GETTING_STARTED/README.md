# SOC Job Task Analyzer

## Overview

The SOC Job Task Analyzer is a comprehensive research tool designed for PhD-level analysis of cybersecurity workforce requirements. This project automates the collection, processing, and thematic analysis of SOC (Security Operations Center) job postings to identify core competencies, task patterns, and skill requirements in cybersecurity operations.

### Key Features

- **Automated Data Collection**: Scrapes job postings from Google Jobs API using SerpAPI
- **Intelligent Classification**: Filters and categorizes SOC-specific roles using configurable rules
- **Task Extraction**: Identifies and consolidates job responsibilities from unstructured text
- **Thematic Clustering**: Pre-processes tasks for LLM analysis with keyword-based clustering
- **Research-Ready Outputs**: Produces structured data formats suitable for academic analysis
- **Reproducible Pipeline**: Fully documented, version-controlled, and container-ready

### Research Applications

- **Workforce Analysis**: Identify trending SOC skills and competencies
- **Curriculum Development**: Inform cybersecurity education programs
- **Industry Benchmarking**: Compare SOC requirements across organizations
- **Gap Analysis**: Assess alignment between job requirements and training programs

## Quick Facts

| Metric | Value |
|--------|-------|
| **Languages** | Python 3.10+ |
| **Data Sources** | Google Jobs API (SerpAPI) |
| **Output Format** | JSON/CSV for LLM integration |
| **Deduplication Rate** | 72.5% (1059 → 291 unique tasks) |
| **Clustering Coverage** | 82.8% (241/291 tasks themed) |
| **Execution Time** | ~14 seconds for full pipeline |

## Project Structure

```
SOC-Job-Task-Analyzer/
├── src/                          # Source code
│   ├── soc_scrapper_API.py      # Main data collection
│   ├── data_analyzer.py         # Job classification
│   ├── task_aggregator.py       # Task consolidation
│   ├── task_thematic_clusterer.py # Pre-LLM clustering
│   └── job_run.py               # Pipeline orchestrator
├── configs/                      # Configuration files
│   └── rules.json               # Classification rules
├── data/                         # Data storage
│   ├── raw/                     # API responses
│   └── processed/               # Analysis outputs
├── docs/                         # Documentation
└── requirements.txt             # Python dependencies
```

## Academic Integrity

This project is designed with research reproducibility in mind:

- **Version Control**: All changes tracked with Git
- **Dependency Pinning**: Exact versions specified in requirements.txt
- **Data Provenance**: Complete audit trail from raw API to final analysis
- **Documentation**: Comprehensive guides for replication and extension
- **Ethical Scraping**: Respects API rate limits and terms of service

## Getting Started

### Prerequisites
- Python 3.10 or higher
- SerpAPI key (free tier available)
- Git for version control

### Quick Start
```bash
# Clone and setup
git clone <repository-url>
cd SOC-Job-Task-Analyzer
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configure API key
echo "SERPAPI_KEY=your_key_here" > .env

# Run full pipeline
python src/job_run.py
```

See [QUICK_START.md](QUICK_START.md) for detailed instructions.

## Pipeline Overview

The analysis pipeline consists of four main stages:

1. **Data Collection** (`soc_scrapper_API.py`)
   - Queries Google Jobs API for SOC-related positions
   - Handles pagination, deduplication, and error recovery
   - Stores raw JSON responses in quarter-based organization

2. **Job Classification** (`data_analyzer.py`)
   - Applies configurable rules to filter SOC Tier 1 roles
   - Normalizes job titles and extracts responsibilities
   - Outputs structured CSV with classified positions

3. **Task Aggregation** (`task_aggregator.py`)
   - Consolidates historical job data into unified task lexicon
   - Performs fuzzy deduplication (88% similarity threshold)
   - Generates frequency analysis and task summaries

4. **Thematic Clustering** (`task_thematic_clusterer.py`)
   - Groups tasks into 10 candidate themes using keyword matching
   - Calculates confidence scores for LLM validation
   - Produces structured input for semantic analysis

## Output Formats

The pipeline generates several research-ready outputs:

- **Task Lexicon** (`consolidated_tasks.json`): 291 unique SOC tasks with metadata
- **Themed Clusters** (`tasks_with_candidate_themes.json`): Tasks grouped by functional themes
- **Frequency Analysis** (`task_frequency_report.json`): Task occurrence statistics
- **Pipeline Summary** (`pipeline_summary.json`): Execution metrics and validation

## Configuration

The system is highly configurable through:

- **Rules Engine** (`configs/rules.json`): SOC role classification criteria
- **Environment Variables** (`.env`): API keys and runtime parameters
- **Pipeline Flags** (`job_run.py --help`): Execution options and debugging

## Research Validation

The pipeline includes built-in validation:

- **Data Quality Checks**: Missing field detection and logging
- **Deduplication Metrics**: Similarity scoring and consolidation reports
- **Clustering Accuracy**: Confidence scoring and coverage statistics
- **Reproducibility Tests**: Version-controlled outputs with checksums

## Extending the Project

The modular design supports easy extension:

- **Additional Data Sources**: LinkedIn, Indeed scrapers available
- **LLM Integration**: Ready for Claude/GPT semantic analysis
- **Custom Classification**: Rules engine supports new job categories
- **Batch Processing**: Quarter-based organization for large datasets

## Citation

If you use this project in your research, please cite:

```
SOC Job Task Analyzer
[Version 1.0.0]
Available at: [repository-url]
```

## License

This project is released under the MIT License. See LICENSE file for details.

## Contributing

We welcome contributions from the research community. See [CONTRIBUTING.md](06_APPENDICES/CONTRIBUTING.md) for guidelines.

---

**Last Updated:** December 2024
**Version:** 1.0.0
**Contact:** [Your contact information]
# SOC-Job-Task-Analyzer

A comprehensive toolset for collecting, processing, and analyzing Security Operations Center (SOC) job descriptions. This project uses a multi-LLM consensus methodology to extract standardized cybersecurity tasks and map them to thematic categories.

## 🚀 Project Overview

This repository automates the pipeline from raw job scraping to thematic task analysis:
1.  **Collection**: Scraping jobs via Google Jobs API and LinkedIn.
2.  **Normalization**: Rule-based classification of job titles.
3.  **Extraction**: Identifying unique cybersecurity tasks using state-of-the-art LLMs (Gemini, DeepSeek, Grok, GPT-4).
4.  **Thematic Mapping**: Consolidating tasks into 35 standardized categories with >85% model consensus.

## 📂 Project Structure

```text
SOC-Job-Task-Analyzer/
├── src/                # Core Python implementation
│   ├── job_run.py          # Main entry point for the analysis pipeline
│   ├── data_analsyer.py    # Rule-based classification & data processing
│   ├── job_task_analyser.py# LLM-based task extraction & mapping
│   ├── soc_scrapper_API.py # Google Jobs API scraper
│   └── soc_scrapper_*.py   # Alternative scrapers (LinkedIn, etc.)
├── configs/            # Configuration & logic
│   └── rules.json          # Title classification & normalization rules
├── data/               # Data storage (Git Ignored)
│   ├── raw/                # Original .json job descriptions
│   └── processed/          # CSV results and analysis summaries
├── .context.md         # AI-assistant domain context
├── methodology.md      # Detailed research methodology
└── requirements.txt    # Project dependencies
```

## 🛠️ Setup Rules

### 1. Environment Setup
We recommend using a virtual environment (Python 3.10+):
```powershell
# Create environment
python -m venv socenv

# Activate (Windows)
.\socenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Data Organization
*   **Raw Data**: Place any new job scraper outputs (`.json`) into `data/raw/`.
*   **Rules**: Modify `configs/rules.json` to update how job titles are categorized (e.g., Tier 1 vs. Tier 2).

### 3. Running Analysis
The primary analysis flow is managed via `src/data_analsyer.py`:
```powershell
python src/data_analsyer.py data/processed/your_data.csv configs/rules.json
```

## 📝 Methodology Summary
Our process extracted 211 unique tasks from 49 job descriptions, consolidated into 35 standardized responsibilities. Using a multi-LLM consensus (Gemini Pro, DeepSeek, Grok, ChatGPT-4), we achieved over 85% thematic overlap, validated by human cybersecurity researchers.

See [methodology.md](methodology.md) for full details.

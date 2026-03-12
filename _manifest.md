# PROJECT MANIFEST: SOC-Job-Task-Analyzer
*This file maintains the high-level state of the organized project.*

**Last Updated:** 2026-03-12 16:05

### **Project Structure**
- `.context.md`: Project domain and rules.
- `methodology.md`: Research background and methodology.
- `.gitignore`: Files excluded from GitHub (data, virtual env).
- `_manifest.md`: This file.

### **Directories**
#### `/src` (Python Scripts)
- `soc_scrapper.py`: Basic scraper.
- `soc_scrapper_API.py`: Scraper using Google Jobs API.
- `soc_scrapper_linkedin.py`: LinkedIn-specific scraper.
- `job_task_analyser.py`: Multi-LLM task extraction logic.
- `data_analsyer.py`: Data processing and thematic grouping.
- `job_run.py`: Entry point/runner.

#### `/configs`
- `rules.json`: Classification rules and normalization logic.

#### `/data/raw` (Git Ignored)
- Original `.json` job description files.

#### `/data/processed` (Git Ignored)
- Flattened `.csv` files and analysis summaries.

#### `/socenv` (Git Ignored)
- Virtual environment for project dependencies.

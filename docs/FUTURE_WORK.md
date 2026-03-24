# Future Work & Project Roadmap

## 1. Scraper Enhancements
- [ ] **Dynamic Query Generation:** Automatically generate search queries by combining core SOC terms with seniority modifiers from `configs/rules.json`.
- [ ] **Geographic Expansion:** Expand search beyond "United States" to include UK, Canada, and EU regions for comparative research.
- [ ] **API Cost Optimization:** Implement a check against SerpAPI credit balance before running large-scale multi-query scrapes.
- [ ] **Date Filtering:** Add ability to filter by `date_posted` (e.g., last 24h, last week) to avoid redundant scraping of old listings.

## 2. Classification & Analysis
- [ ] **LLM-Based Verification:** Use a local LLM (e.g., Llama 3) to verify the "Tier 1" classification of the filtered results to reduce false positives.
- [ ] **Multi-Tier Analysis:** Update `data_analyzer.py` to export separate CSVs for Tier 2 and Tier 3 for longitudinal workforce studies.
- [ ] **Skill Mapping:** Integrate with the NICE Framework KSA (Knowledge, Skills, Abilities) database to automatically map extracted tasks to standardized KSAs.
- [x] **Hierarchical Taxonomy Implementation:** Move beyond flat 10-theme clustering to 22+ sub-themes mapped to strategic goals (V1.2).

## 3. Tooling & Pipeline
- [ ] **Web Dashboard:** Build a Streamlit dashboard to visualize task frequency and thematic clustering results in real-time.
- [ ] **Automated Reporting:** Generate a PDF research summary after each pipeline run.
- [ ] **Archive Management:** Periodically move older `data/raw` runs to long-term storage or compress them to save space.

## 4. Archived Components (For Reference)
The following scripts were archived in `src/archive/` as they were redundant or required high maintenance:
- `soc_scrapper.py`: Selenium-based scraper (frequent CAPTCHA issues).
- `soc_scrapper_linkedin.py`: Experimental multi-source scraper (Indeed/ZipRecruiter).
- `job_task_analyser.py`: Conceptual prototype of the analysis pipeline.

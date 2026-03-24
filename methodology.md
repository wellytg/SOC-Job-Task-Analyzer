# Methodology: SOC Analyst Job Task Extraction

## **Phase 1: Pilot Study (Historical)**
Forty-nine SOC analyst job descriptions were collected via Google Jobs API and custom web scraping. These jobs were filtered for relevance and subsequently normalized using rule-based classification. From the resulting corpus, 211 unique cybersecurity tasks were identified and extracted, excluding administrative information. These tasks were systematically cleaned and consolidated into 35 standardized cybersecurity tasks focusing on actionable, measurable responsibilities like "monitor SIEM alerts," "escalate security incidents," or "conduct threat hunting activities."

## **Phase 2: Expanded Research Pipeline (V1.2 - Current)**
This phase implements a multi-stage automated pipeline to collect, classify, and analyze SOC Tier 1 job descriptions at scale, aligned with standardized cybersecurity workforce frameworks.

### **1. Data Collection Strategy**
Data was collected using a broad, 16-query search strategy via the Google Jobs API (SerpAPI). Search queries were derived from three primary sources:
*   **NIST NICE Framework (SP 800-181):** Mapping to the *Cyber Defense Analyst (PR-CDA-001)* work role.
*   **O*NET Occupational Classification:** Mapping to the *Information Security Analyst (15-1212.00)* code.
*   **Industry Standard Titles:** Including common variants like "SOC Analyst Tier 1", "Junior SOC Analyst", and "L1 Security Monitor".

This approach resulted in a raw dataset of **338 job listings**, which was de-duplicated to **156 unique listings** for analysis.

### **2. Rule-Based Classification (NIST/O*NET Filter Stack)**
To isolate entry-level operational roles from specialized engineering or senior management, a multi-tier "Filter Stack" logic was applied. Jobs were classified using a strictly defined set of JSON-based rules (see `configs/rules.json` and `analyst_rules_definitions.md`).
*   **Negative Filters:** Titles containing "Senior", "Lead", "Manager", or "Engineer" were excluded from the Tier 1 cohort.
*   **Positive Indicators:** Focused on "Junior", "Associate", "Entry", "Trainee", and "Level 1" modifiers.
*   **Result:** A high-purity cohort of **48 SOC Tier 1 positions** was identified for task extraction.

### **3. Task Extraction & Deduplication**
From the Tier 1 cohort, individual responsibilities were extracted and cleaned. A fuzzy-matching deduplication process (using an 88% similarity threshold) was employed to consolidate 1,263 raw responsibility statements into a unified lexicon of **471 unique cybersecurity tasks**.

### **4. Thematic Clustering & Validation**
Tasks were systematically grouped into 10 functional themes (e.g., *Security Monitoring & Alert Triage*, *Incident Response & Containment*) using keyword-based confidence scoring.
*   **Thematic Coverage:** 78% of all unique tasks were successfully mapped to functional themes.

## **Multi-LLM Consensus Strategy (Validation)**
To ensure robust semantic mapping reliability and align with emerging best practices, we employed multiple state-of-the-art LLMs, including:
- Gemini Pro
- DeepSeek
- Grok
- ChatGPT-4

Each model was deployed independently on identical standardized prompts to extract job tasks, group them thematically, and map tasks to strategic goals. Finally, human-in-the-loop validation was performed through independent annotations from cybersecurity researchers. This method yielded a high cross-model agreement, with thematic overlap exceeding 85%, and human coders confirming most model-derived categories.

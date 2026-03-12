# Methodology: SOC Analyst Job Task Extraction

Forty-nine SOC analyst job descriptions were collected via Google Jobs API and custom web scraping. These jobs were filtered for relevance and subsequently normalized using rule-based classification. From the resulting corpus, 211 unique cybersecurity tasks were identified and extracted, excluding administrative information. These tasks were systematically cleaned and consolidated into 35 standardized cybersecurity tasks focusing on actionable, measurable responsibilities like "monitor SIEM alerts," "escalate security incidents," or "conduct threat hunting activities."

## **Multi-LLM Consensus Strategy**
To ensure robust semantic mapping reliability and align with emerging best practices, we employed multiple state-of-the-art LLMs, including:
- Gemini Pro
- DeepSeek
- Grok
- ChatGPT-4

Each model was deployed independently on identical standardized prompts to extract job tasks, group them thematically, and map tasks to strategic goals. Finally, human-in-the-loop validation was performed through independent annotations from cybersecurity researchers. This method yielded a high cross-model agreement, with thematic overlap exceeding 85%, and human coders confirming most model-derived categories.

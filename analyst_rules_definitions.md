# SOC Analyst Tier 1: Classification Rules & Logic Definition

## 1. Overview
This document defines the logic and cross-referenced standards used to classify "SOC Tier 1 Analyst" job descriptions. The goal is to isolate entry-level operational roles from specialized engineering, senior architecture, or management roles to ensure high-quality data for research into SOC task analysis.

## 2. Cross-Reference Standards

### A. NIST NICE Framework (SP 800-181)
The primary mapping for a SOC Tier 1 Analyst is the **Cyber Defense Analyst (PR-CDA-001)** work role within the **Protect and Defend** category.
*   **Definition:** Uses data collected from a variety of cyber defense tools (e.g., IDS alerts, firewalls, network traffic logs) to analyze events that occur within their environments for the purposes of mitigating threats.
*   **Key Tasks (Tier 1 Focus):**
    *   **T0040:** Characterize and analyze network traffic to identify anomalous activity.
    *   **T0214:** Perform tier 1, 2, and 3 support for real-time incident handling (with Tier 1 focusing on triage).
    *   **T0258:** Document and escalate incidents to higher-level analysts.

### B. O*NET Standard Occupational Classification
SOC Analysts are typically classified under the broad category:
*   **Code:** **15-1212.00 - Information Security Analysts**
*   **Role Description:** Plan, implement, upgrade, or monitor security measures for the protection of computer networks and information.
*   **Relevance:** O*NET provides the "Job Title" layer used by government and large-scale HR systems, whereas NICE provides the functional task layer.

### C. Industry Standards
Industry practice (SANS, GIAC, CREST) typically differentiates Tier 1 by:
*   **Title Modifiers:** Junior (Jr), Associate, Level 1 (L1), Tier 1 (T1), Analyst I.
*   **Functional Focus:** Monitoring, Triage, and Playbook-driven response.

## 3. Academic Sources
The following academic research informs the task-level granularity of these rules:

1.  **NDSS Symposium (2023):** *"A Test Tool to Evaluate the Skill Sets of Tier-1 Security Analysts"*. Confirms Tier 1 tasks as high-volume alert triage and low-depth investigation.
2.  **Al Harrack (2021):** *"Mapping out O*NET Data to Inform Workforce Readiness"*. Establishes the link between O*NET 15-1212.00 and the specific task requirements in the NICE Framework.
3.  **D'Amico et al.:** *"Task Analysis toward Characterizing Cyber-Cognitive Situation Awareness"*. Defines the "monitoring" phase as the core cognitive load for entry-level analysts.

## 4. Classification Logic
The rules are structured as a "Filter Stack." Higher-tier roles (Tier 3, Tier 2, Lead) are evaluated first to act as "Negative Filters." If a title contains "Lead" or "Senior," it is immediately excluded from Tier 1.

### Primary Tier 1 Indicators:
*   **Presence of Level:** "1", "I", "L1", "T1".
*   **Presence of Seniority Modifiers:** "Junior", "Jr", "Associate", "Entry", "Trainee", "Intern".
*   **Presence of Framework Roles:** "Cyber Defense Analyst" (NICE), "Incident Monitor".

### Exclusion Criteria (Must Not Contain):
*   "Senior", "Sr", "Lead", "Principal", "Architect", "Manager", "Engineer", "Tier 2", "Tier 3".

## 5. Refined JSON Rules (For `configs/rules.json`)

The following JSON block provides a comprehensive set of rules to isolate Tier 1 roles using the logic defined above.

```json
[
	{
		"name": "SOC Analyst Tier 3 / Lead",
		"must_contain": [
			["soc", "security", "csoc", "cybersecurity", "defense", "incident"],
			["analyst", "responder", "specialist"],
			["3", "iii", "senior", "sr", "lead", "principal", "expert", "manager", "staff", "architect"]
		],
		"must_not_contain": [["1", "i", "jr", "junior", "associate", "entry", "intern"]]
	},
	{
		"name": "SOC Analyst Tier 2",
		"must_contain": [
			["soc", "security", "csoc", "cybersecurity", "defense"],
			["analyst"],
			["2", "ii", "mid", "intermediate"]
		],
		"must_not_contain": [["1", "i", "3", "iii", "jr", "junior", "associate", "senior", "sr", "lead", "principal"]]
	},
	{
		"name": "SOC Analyst Tier 1",
		"must_contain": [
			["soc", "security", "csoc", "cybersecurity", "defense", "infosec", "information"],
			["analyst", "monitor", "specialist", "triage"],
			["1", "i", "jr", "junior", "associate", "entry", "trainee", "intern", "t1", "l1"]
		],
		"must_not_contain": [["2", "ii", "3", "iii", "senior", "sr", "lead", "manager", "principal", "architect", "engineer"]]
	},
	{
		"name": "SOC Analyst Tier 1",
		"must_contain": [
			["cyber"],
			["defense"],
			["analyst"]
		],
		"must_not_contain": [["2", "ii", "3", "iii", "senior", "sr", "lead", "manager", "principal", "engineer"]]
	},
	{
		"name": "SOC Analyst Tier 1",
		"must_contain": [
			["information"],
			["security"],
			["analyst"],
			["1", "i", "jr", "junior", "associate", "entry"]
		],
		"must_not_contain": [["2", "ii", "3", "iii", "senior", "sr", "lead", "manager", "principal", "engineer", "architect"]]
	},
	{
		"name": "SOC Analyst (General)",
		"must_contain": [
			["soc", "security", "csoc", "cybersecurity"],
			["analyst"]
		],
		"must_not_contain": [
			["1", "i", "2", "ii", "3", "iii", "lead", "jr", "junior", "associate", "senior", "sr", "engineer", "manager"]
		]
	}
]
```

# STEP 0: INITIALIZATION
def initialize_analysis():
    """Load dataset and set up analysis environment"""
    requirements = {
        "input_format": "CSV with columns: Title, Company, Location, Responsibilities",
        "outputs": ["extracted_tasks", "thematic_categories", "goal_mapping_table", "survey_instrument"],
        "parameters": {
            "min_tasks_per_category": 5,
            "goal_inference_threshold": 0.7  # Confidence score for goal inference
        }
    }
    return requirements

# STEP 1: DATA EXTRACTION
def extract_job_tasks(responsibilities_text):
    """Extract discrete job tasks from responsibilities column"""
    extraction_rules = [
        "Split on: newlines (\\n), bullet points (•, -), semicolons (;), periods (.)",
        "Keep only verb-led phrases describing actionable duties",
        "Remove: EEOC statements, benefits info, contact information, company descriptions",
        "Clean: strip whitespace, remove empty strings, standardize formatting"
    ]
    
    # Implementation logic
    tasks = []
    for text in responsibilities_text:
        # Apply splitting rules
        fragments = re.split(r'[\n•;-]|\.\s+', text)
        for fragment in fragments:
            if is_actionable_task(fragment):  # Custom function to filter tasks
                tasks.append(clean_task(fragment))
    return tasks

# STEP 2: TASK AGGREGATION & ANALYSIS
def analyze_task_frequency(tasks):
    """Aggregate and analyze task frequency"""
    task_counts = Counter(tasks)
    representative_tasks = task_counts.most_common(30)  # Top 30 tasks
    return representative_tasks

# STEP 3: THEMATIC CATEGORIZATION
def categorize_tasks(tasks):
    """Group tasks into thematic categories"""
    categorization_rules = {
        "Security Monitoring & Alert Triage": [
            "monitor", "alert", "triage", "SIEM", "real-time", "detect"
        ],
        "Incident Response & Handling": [
            "incident", "respond", "escalate", "contain", "remediate", "isolate"
        ],
        # ... (similar patterns for other categories)
    }
    
    categorized_tasks = {}
    for category, keywords in categorization_rules.items():
        categorized_tasks[category] = [
            task for task in tasks 
            if any(keyword in task.lower() for keyword in keywords)
        ]
    return categorized_tasks

# STEP 4: GOAL INFERENCE
def infer_goals_from_categories(categorized_tasks):
    """Map thematic categories to strategic goals"""
    goal_mapping_template = {
        "Security Monitoring & Alert Triage": {
            "goals": ["Rapid Threat Detection", "Comprehensive Coverage", "Alert Efficiency"],
            "survey_questions": [
                "How critical is minimizing time-to-detection for security incidents?",
                "Rate the importance of monitoring coverage across all critical assets"
            ]
        },
        # ... (template for all categories)
    }
    
    goal_mapping = {}
    for category, tasks in categorized_tasks.items():
        if category in goal_mapping_template:
            goal_mapping[category] = {
                "tasks": tasks,
                "inferred_goals": goal_mapping_template[category]["goals"],
                "survey_items": goal_mapping_template[category]["survey_questions"]
            }
    return goal_mapping

# STEP 5: SURVEY INSTRUMENT GENERATION
def generate_survey_instrument(goal_mapping):
    """Create ranking survey for CISOs/SOC Managers"""
    survey = {
        "instructions": "Please rate the importance of each goal for your SOC operations (1=Not Important, 5=Critical)",
        "sections": []
    }
    
    for category, data in goal_mapping.items():
        section = {
            "category": category,
            "goals": []
        }
        for i, goal in enumerate(data["inferred_goals"]):
            section["goals"].append({
                "goal_id": f"G{len(survey['sections'])*3 + i + 1}",
                "description": goal,
                "survey_question": data["survey_items"][i],
                "rating_scale": "1-5 Likert scale"
            })
        survey["sections"].append(section)
    
    return survey

# MAIN EXECUTION PIPELINE
def analyze_soc_jobs_dataset(csv_file_path):
    """Complete analysis pipeline"""
    # Step 0: Initialize
    config = initialize_analysis()
    
    # Step 1: Extract data
    df = pd.read_csv(csv_file_path)
    tasks = extract_job_tasks(df['Responsibilities'])
    
    # Step 2: Analyze frequency
    common_tasks = analyze_task_frequency(tasks)
    
    # Step 3: Categorize
    categorized = categorize_tasks([task[0] for task in common_tasks])
    
    # Step 4: Infer goals
    goal_map = infer_goals_from_categories(categorized)
    
    # Step 5: Generate survey
    survey = generate_survey_instrument(goal_map)
    
    return {
        "extracted_tasks": common_tasks,
        "thematic_categories": categorized,
        "goal_mapping_table": goal_map,
        "survey_instrument": survey
    }
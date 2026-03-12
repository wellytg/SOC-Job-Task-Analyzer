# Apply to your dataset
results = analyze_soc_jobs_dataset("soc_jobs_flattened_20250918_201733.csv")

# Export for your research
import json
with open('goal_mapping_analysis.json', 'w') as f:
    json.dump(results, f, indent=2)
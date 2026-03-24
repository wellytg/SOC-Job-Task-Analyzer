"""
task_thematic_clusterer.py

Pre-LLM thematic clustering and candidate theme assignment.
Groups tasks by keyword patterns to create candidate themes with confidence scores.

Pipeline Step 4 (BONUS): Pre-LLM Analysis & Clustering
Input: data/processed/task_lexicon/consolidated_tasks.json
Output:
  - data/processed/task_lexicon/tasks_with_candidate_themes.json
  - data/processed/task_lexicon/clustering_analysis_report.txt
  - data/processed/task_lexicon/theme_summary.json
"""

import os
import json
import re
from collections import defaultdict
from datetime import datetime
import sys


class TaskThematicClusterer:
    def __init__(self, input_json=None, rules_path="configs/theme_rules.json", output_folder="data/processed/task_lexicon"):
        self.input_json = input_json
        self.rules_path = rules_path
        self.output_folder = output_folder
        self.tasks_with_themes = []
        self.theme_clusters = defaultdict(list)
        self.unclustered_tasks = []
        
        # Load hierarchical theme rules
        self.theme_rules = self.load_theme_rules(rules_path)
        
        os.makedirs(self.output_folder, exist_ok=True)
    
    def load_theme_rules(self, rules_path):
        """Load hierarchical theme rules from JSON"""
        try:
            if not os.path.exists(rules_path):
                print(f"Warning: Rules file not found at {rules_path}. Using empty rules.")
                return []
            
            with open(rules_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading theme rules: {e}")
            return []

    def find_latest_consolidated_tasks(self):
        """Find the most recent consolidated_tasks JSON file"""
        if self.input_json:
            return self.input_json
        
        files = [
            f for f in os.listdir(self.output_folder)
            if f.startswith("consolidated_tasks_") and f.endswith(".json")
            and "candidate" not in f and "delta" not in f
        ]
        
        if not files:
            return None
        
        latest = sorted(files)[-1]
        return os.path.join(self.output_folder, latest)
    
    def load_tasks(self, json_path):
        """Load task lexicon from JSON"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract tasks from the 'tasks' list in the JSON
            tasks = [t['text'] for t in data.get('tasks', [])]
            print(f"Loaded {len(tasks)} tasks from {os.path.basename(json_path)}")
            return tasks
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return []
    
    def calculate_confidence(self, task, keywords):
        """
        Calculate confidence score for a task matching a set of keywords.
        """
        task_lower = task.lower()
        matches = []
        
        for keyword in keywords:
            # Simple keyword matching (can be improved with regex)
            if keyword.lower() in task_lower:
                matches.append(keyword)
        
        if not matches:
            return 0.0
        
        # Base score on number of matches
        match_count = len(matches)
        base_score = min(match_count / 1.5, 1.0)  # Reached 1.0 with 2+ matches
        
        # Position boost (if keyword appears early)
        first_match_idx = task_lower.find(matches[0].lower())
        position_boost = max(0.1, 1.0 - (first_match_idx / len(task) * 0.3))
        
        confidence = (base_score * 0.7 + position_boost * 0.3)
        return round(confidence, 3)
    
    def cluster_task(self, task):
        """
        Assign task to candidate theme/sub-theme based on keyword matching.
        """
        best_match = {
            "primary_theme": "Unclassified",
            "sub_theme": "Unclassified",
            "strategic_goal": "Unknown",
            "confidence": 0.0,
            "matching_keywords": []
        }
        
        for primary in self.theme_rules:
            for sub in primary['sub_themes']:
                confidence = self.calculate_confidence(task, sub['keywords'])
                
                if confidence > best_match['confidence']:
                    best_match = {
                        "primary_theme": primary['primary_theme'],
                        "sub_theme": sub['name'],
                        "strategic_goal": primary['strategic_goal'],
                        "confidence": confidence,
                        "matching_keywords": [kw for kw in sub['keywords'] if kw.lower() in task.lower()]
                    }
        
        return best_match
    
    def cluster_all_tasks(self, tasks):
        """Cluster all tasks into hierarchical themes"""
        print(f"\nClustering {len(tasks)} tasks into hierarchical themes...\n")
        
        for task in tasks:
            match = self.cluster_task(task)
            
            if match['confidence'] >= 0.3:  # Confidence threshold
                task_entry = {
                    "task": task,
                    "primary_theme": match['primary_theme'],
                    "sub_theme": match['sub_theme'],
                    "strategic_goal": match['strategic_goal'],
                    "confidence": match['confidence'],
                    "matching_keywords": match['matching_keywords'],
                    "confidence_level": self._interpret_confidence(match['confidence'])
                }
                self.tasks_with_themes.append(task_entry)
                self.theme_clusters[match['primary_theme']].append(task_entry)
            else:
                self.unclustered_tasks.append(task)
        
        # Print summary
        print(f"Clustered: {len(self.tasks_with_themes)} tasks")
        print(f"Unclustered (low confidence): {len(self.unclustered_tasks)} tasks\n")
    
    def _interpret_confidence(self, confidence):
        """Convert confidence score to human-readable level"""
        if confidence >= 0.8:
            return "HIGH"
        elif confidence >= 0.6:
            return "MEDIUM"
        elif confidence >= 0.4:
            return "LOW"
        else:
            return "VERY_LOW"
    
    def save_themed_tasks(self):
        """Save tasks with candidate themes"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create output structure
        output = {
            "metadata": {
                "timestamp": timestamp,
                "total_tasks": len(self.tasks_with_themes) + len(self.unclustered_tasks),
                "clustered_tasks": len(self.tasks_with_themes),
                "unclustered_tasks": len(self.unclustered_tasks),
                "unique_primary_themes": len(self.theme_clusters)
            },
            "tasks": self.tasks_with_themes,
            "unclustered_tasks": self.unclustered_tasks
        }
        
        # Save JSON
        json_path = os.path.join(
            self.output_folder,
            f"tasks_with_candidate_themes_{timestamp}.json"
        )
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"✓ Saved: {json_path}")
        
        return json_path, output
    
    def save_clustering_report(self, output_data):
        """Generate detailed clustering analysis report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(
            self.output_folder,
            f"clustering_analysis_report_{timestamp}.txt"
        )
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 90 + "\n")
            f.write("HIERARCHICAL TASK CLUSTERING REPORT\n")
            f.write("=" * 90 + "\n\n")
            
            # Summary
            meta = output_data['metadata']
            f.write(f"Total Tasks: {meta['total_tasks']}\n")
            f.write(f"Clustered: {meta['clustered_tasks']}\n")
            f.write(f"Unclustered: {meta['unclustered_tasks']}\n\n")
            
            # Distribution
            f.write("PRIMARY THEME DISTRIBUTION\n")
            f.write("-" * 30 + "\n")
            for theme in sorted(self.theme_clusters.keys()):
                tasks = self.theme_clusters[theme]
                # Calculate sub-theme breakdown
                sub_counts = defaultdict(int)
                for t in tasks:
                    sub_counts[t['sub_theme']] += 1
                
                f.write(f"\n[{theme}] ({len(tasks)} tasks)\n")
                f.write(f"  Strategic Goal: {tasks[0]['strategic_goal']}\n")
                for sub, count in sorted(sub_counts.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"  - {sub:35s}: {count:3d} tasks\n")
        
        print(f"✓ Saved: {report_path}")
        return report_path
    
    def run(self):
        """Execute full clustering pipeline"""
        print("=" * 90)
        print("TASK THEMATIC CLUSTERER - Hierarchical Analysis")
        print("=" * 90 + "\n")
        
        json_path = self.find_latest_consolidated_tasks()
        if not json_path:
            return {"status": "error", "message": "No consolidated tasks found"}
        
        tasks = self.load_tasks(json_path)
        if not tasks:
            return {"status": "error", "message": "Failed to load tasks"}
        
        self.cluster_all_tasks(tasks)
        json_output_path, output_data = self.save_themed_tasks()
        report_path = self.save_clustering_report(output_data)
        
        return {
            "status": "success",
            "clustered_tasks": len(self.tasks_with_themes),
            "unique_themes": len(self.theme_clusters),
            "output_json": json_output_path
        }


if __name__ == "__main__":
    clusterer = TaskThematicClusterer()
    result = clusterer.run()
    print(json.dumps(result, indent=2))

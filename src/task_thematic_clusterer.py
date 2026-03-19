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
    def __init__(self, input_json=None, output_folder="data/processed/task_lexicon"):
        self.input_json = input_json
        self.output_folder = output_folder
        self.tasks_with_themes = []
        self.theme_clusters = defaultdict(list)
        self.unclustered_tasks = []
        
        # Define domain-specific keyword patterns and associated themes
        # ORDER MATTERS: Rules applied in sequence, first match wins
        self.theme_rules = [
            {
                "theme": "Security Monitoring & Alert Triage",
                "keywords": [
                    r"\bmonitor\b", r"\bwatch\b", r"\bsurveill", r"\balert",
                    r"\btriage\b", r"\bsiem\b", r"\bsoc\b", r"\bthreats?",
                    r"\banomal", r"\bevents?", r"\bingest\b", r"\bincoming\b"
                ],
                "must_have_one": True,
                "weight": 1.0
            },
            {
                "theme": "Incident Response & Containment",
                "keywords": [
                    r"\bincident", r"\brespond", r"\bescalat", r"\bcontain",
                    r"\bremediat", r"\biso late", r"\bquarantine", r"\beradica",
                    r"\bcontainment\b", r"\bsuppression\b", r"\bimpact"
                ],
                "must_have_one": True,
                "weight": 1.0
            },
            {
                "theme": "Threat Analysis & Triage",
                "keywords": [
                    r"\banalyze?\b", r"\binvestigat", r"\bretrie", r"\banalyses",
                    r"\bexamin", r"\bdata\s+(mining|collection)", r"\bforensic",
                    r"\broot\s+cause", r"\btriage\b", r"\breview"
                ],
                "must_have_one": True,
                "weight": 0.95
            },
            {
                "theme": "Log Review & Event Correlation",
                "keywords": [
                    r"\blog", r"\bevent", r"\bcorrelat", r"\bpattern",
                    r"\bindicator", r"\bioc\b", r"\bsignature", r"\bparse"
                ],
                "must_have_one": True,
                "weight": 0.9
            },
            {
                "theme": "Communication & Escalation",
                "keywords": [
                    r"\breport", r"\bcommunicat", r"\bescalat", r"\bnotif",
                    r"\balert\s+management", r"\bstakeholder", r"\bdocument"
                ],
                "must_have_one": True,
                "weight": 0.85
            },
            {
                "theme": "System & Network Defense",
                "keywords": [
                    r"\bfirewall", r"\nids\b", r"\bids/ips", r"\bips\b",
                    r"\bnetwork\s+(segmentation|defense)", r"\bvpn\b",
                    r"\baccept\s+connection", r"\bdeny\b", r"\nblock\b"
                ],
                "must_have_one": True,
                "weight": 0.9
            },
            {
                "theme": "Vulnerability & Threat Intelligence",
                "keywords": [
                    r"\bvulnerabil", r"\bpatches?\b", r"\bupdates?\b",
                    r"\bthreat.*intel", r"\btic\b", r"\bintel", r"\bcve\b",
                    r"\bexploit", r"\bcvss\b"
                ],
                "must_have_one": True,
                "weight": 0.9
            },
            {
                "theme": "Compliance & Documentation",
                "keywords": [
                    r"\bcompl", r"\bdocument", r"\breport", r"\bprocess",
                    r"\bprocedure", r"\bstandard", r"\baudit", r"\bsoc\s+2"
                ],
                "must_have_one": True,
                "weight": 0.75
            },
            {
                "theme": "Tool & Platform Operations",
                "keywords": [
                    r"\btool", r"\bplatform\b", r"\bopera", r"\bmaintain",
                    r"\bconfigur", r"\bupdat", r"\bscreen", r"\bdashboard"
                ],
                "must_have_one": True,
                "weight": 0.7
            },
            {
                "theme": "Team Collaboration & Support",
                "keywords": [
                    r"\bcollaboat", r"\bteam\b", r"\bsupport", r"\bassist",
                    r"\btraining\b", r"\bhelp\b", r"\bcoordinate", r"\bparticipate"
                ],
                "must_have_one": True,
                "weight": 0.7
            }
        ]
        
        os.makedirs(self.output_folder, exist_ok=True)
    
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
            
            tasks = [t['text'] for t in data.get('tasks', [])]
            print(f"Loaded {len(tasks)} tasks from {os.path.basename(json_path)}")
            return tasks
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return []
    
    def calculate_confidence(self, task, theme_rule):
        """
        Calculate confidence score for a task matching a theme.
        Score based on:
        - Number of keyword matches
        - Keyword specificity
        - Position in text (earlier = higher)
        """
        task_lower = task.lower()
        matches = []
        
        for keyword_pattern in theme_rule['keywords']:
            for match in re.finditer(keyword_pattern, task_lower, re.IGNORECASE):
                matches.append({
                    'keyword': keyword_pattern,
                    'start': match.start(),
                    'length': len(match.group())
                })
        
        if not matches:
            return 0.0
        
        # Base score on number of matches
        match_count = len(matches)
        base_score = min(match_count / 2.0, 1.0)  # Cap at 1.0 with 2+ matches
        
        # Boost for early mentions (first keyword appearance is stronger signal)
        first_match_position = min(m['start'] for m in matches)
        position_boost = max(0.1, 1.0 - (first_match_position / len(task) * 0.3))
        
        # Combine scores
        confidence = (base_score * 0.6 + position_boost * 0.4) * theme_rule.get('weight', 1.0)
        
        return round(confidence, 3)
    
    def cluster_task(self, task):
        """
        Assign task to candidate theme based on keyword matching.
        Returns: (theme_name, confidence, matching_keywords)
        """
        best_theme = None
        best_confidence = 0.0
        best_keywords = []
        
        for rule in self.theme_rules:
            confidence = self.calculate_confidence(task, rule)
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_theme = rule['theme']
                
                # Track matching keywords
                task_lower = task.lower()
                best_keywords = [
                    kw for kw in rule['keywords']
                    if re.search(kw, task_lower, re.IGNORECASE)
                ]
        
        return best_theme, best_confidence, best_keywords
    
    def cluster_all_tasks(self, tasks):
        """Cluster all tasks into candidate themes"""
        print(f"\nClustering {len(tasks)} tasks into candidate themes...\n")
        
        for task in tasks:
            theme, confidence, keywords = self.cluster_task(task)
            
            if confidence >= 0.3:  # Confidence threshold
                task_entry = {
                    "task": task,
                    "candidate_theme": theme,
                    "confidence": confidence,
                    "matching_keywords": keywords,
                    "confidence_level": self._interpret_confidence(confidence)
                }
                self.tasks_with_themes.append(task_entry)
                self.theme_clusters[theme].append(task_entry)
            else:
                self.unclustered_tasks.append(task)
        
        # Print summary
        print(f"Clustered: {len(self.tasks_with_themes)} tasks")
        print(f"Unclustered (low confidence): {len(self.unclustered_tasks)} tasks\n")
        
        print("Theme Distribution:")
        for theme in sorted(self.theme_clusters.keys()):
            count = len(self.theme_clusters[theme])
            avg_confidence = round(
                sum(t['confidence'] for t in self.theme_clusters[theme]) / count,
                3
            )
            print(f"  {theme:45s}: {count:3d} tasks (avg confidence: {avg_confidence})")
    
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
                "date_created": datetime.now().isoformat(),
                "total_tasks": len(self.tasks_with_themes) + len(self.unclustered_tasks),
                "clustered_tasks": len(self.tasks_with_themes),
                "unclustered_tasks": len(self.unclustered_tasks),
                "clustering_threshold": 0.3,
                "unique_themes": len(self.theme_clusters)
            },
            "tasks": self.tasks_with_themes,
            "unclustered_tasks": self.unclustered_tasks,
            "theme_summary": {
                theme: {
                    "count": len(tasks),
                    "avg_confidence": round(
                        sum(t['confidence'] for t in tasks) / len(tasks), 3
                    ),
                    "sample_tasks": [t['task'] for t in tasks[:3]]
                }
                for theme, tasks in self.theme_clusters.items()
            }
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
            f.write("TASK THEMATIC CLUSTERING REPORT (Pre-LLM Analysis)\n")
            f.write("=" * 90 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Summary
            meta = output_data['metadata']
            f.write("-" * 90 + "\n")
            f.write("SUMMARY\n")
            f.write("-" * 90 + "\n")
            f.write(f"Total Tasks: {meta['total_tasks']}\n")
            f.write(f"Clustered (confidence >= 0.3): {meta['clustered_tasks']}\n")
            f.write(f"Unclustered (low confidence): {meta['unclustered_tasks']}\n")
            f.write(f"Unique Candidate Themes: {meta['unique_themes']}\n\n")
            
            # Per-theme analysis
            f.write("-" * 90 + "\n")
            f.write("PER-THEME ANALYSIS\n")
            f.write("-" * 90 + "\n\n")
            
            for theme in sorted(self.theme_clusters.keys()):
                tasks = self.theme_clusters[theme]
                f.write(f"\n[{theme}]\n")
                f.write(f"  Task Count: {len(tasks)}\n")
                f.write(f"  Avg Confidence: {output_data['theme_summary'][theme]['avg_confidence']}\n")
                f.write(f"  Confidence Breakdown:\n")
                
                # Count by confidence level
                by_level = defaultdict(int)
                for task in tasks:
                    level = task['confidence_level']
                    by_level[level] += 1
                
                for level in ['HIGH', 'MEDIUM', 'LOW', 'VERY_LOW']:
                    if by_level[level] > 0:
                        f.write(f"    {level:10s}: {by_level[level]:3d} tasks\n")
                
                f.write(f"\n  Sample Tasks:\n")
                for i, task in enumerate(tasks[:5], 1):
                    f.write(f"    {i}. [{task['confidence']}] {task['task']}\n")
            
            # Unclustered tasks
            if self.unclustered_tasks:
                f.write(f"\n\n{'=' * 90}\n")
                f.write("UNCLUSTERED TASKS (Low Confidence - Require Manual Review)\n")
                f.write("=" * 90 + "\n\n")
                for i, task in enumerate(self.unclustered_tasks[:20], 1):
                    f.write(f"{i:3d}. {task}\n")
                if len(self.unclustered_tasks) > 20:
                    f.write(f"\n... and {len(self.unclustered_tasks) - 20} more\n")
            
            f.write("\n" + "=" * 90 + "\n")
            f.write("NEXT STEPS\n")
            f.write("=" * 90 + "\n")
            f.write("""
1. Review HIGH and MEDIUM confidence clusters for validity
2. Investigate UNCLUSTERED tasks - may reveal new themes or need rule adjustments
3. Validate that clustering aligns with SOC domain expertise
4. Pass tasks_with_candidate_themes.json to LLM for final semantic analysis
5. LLM will refine/merge/validate these candidate themes
""")
        
        print(f"✓ Saved: {report_path}")
        return report_path
    
    def run(self):
        """Execute full clustering pipeline"""
        print("=" * 90)
        print("TASK THEMATIC CLUSTERER - Pre-LLM Analysis")
        print("=" * 90 + "\n")
        
        # Step 1: Find and load tasks
        json_path = self.find_latest_consolidated_tasks()
        if not json_path:
            print("✗ No consolidated tasks found. Run task_aggregator.py first.")
            return {"status": "error", "message": "No consolidated tasks found"}
        
        tasks = self.load_tasks(json_path)
        if not tasks:
            print("✗ Failed to load tasks.")
            return {"status": "error", "message": "Failed to load tasks"}
        
        # Step 2: Cluster all tasks
        self.cluster_all_tasks(tasks)
        
        # Step 3: Save outputs
        json_output_path, output_data = self.save_themed_tasks()
        report_path = self.save_clustering_report(output_data)
        
        print("\n" + "=" * 90)
        print("✓ CLUSTERING COMPLETE")
        print("=" * 90)
        
        return {
            "status": "success",
            "clustered_tasks": len(self.tasks_with_themes),
            "unclustered_tasks": len(self.unclustered_tasks),
            "unique_themes": len(self.theme_clusters),
            "output_json": json_output_path,
            "output_report": report_path
        }


if __name__ == "__main__":
    clusterer = TaskThematicClusterer()
    result = clusterer.run()
    print(json.dumps(result, indent=2))

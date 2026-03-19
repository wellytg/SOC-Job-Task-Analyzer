"""
task_aggregator.py

Consolidates job descriptions from all historical SOC Tier 1 job listings across sources and dates.
Extracts, normalizes, and deduplicates tasks to create a unified task lexicon.

Pipeline Step 3: Task Aggregation & Normalization
Input: All *_soc_tier1_analysis.csv files from data/processed/
Output: 
  - data/processed/task_lexicon/consolidated_tasks.json (structured)
  - data/processed/task_lexicon/consolidated_tasks.csv (human-readable)
  - data/processed/task_lexicon/task_frequency_report.txt
  - data/processed/task_lexicon/task_delta.json (vs previous aggregation)
"""

import os
import json
import pandas as pd
import re
from collections import Counter
from difflib import SequenceMatcher
from datetime import datetime
import sys

class TaskAggregator:
    def __init__(self, processed_folder="data/processed", output_folder="data/processed/task_lexicon"):
        self.processed_folder = processed_folder
        self.output_folder = output_folder
        self.tasks = []
        self.unique_tasks = []
        self.task_metadata = {}
        
        os.makedirs(self.output_folder, exist_ok=True)
    
    def find_soc_tier1_files(self):
        """Locate all *_soc_tier1_analysis.csv files recursively"""
        tier1_files = []
        for root, dirs, files in os.walk(self.processed_folder):
            # Skip task_lexicon folder itself
            if "task_lexicon" in root:
                continue
            for file in files:
                if "_soc_tier1_analysis.csv" in file:
                    tier1_files.append(os.path.join(root, file))
        
        return sorted(tier1_files)
    
    def extract_tasks(self, responsibility_text):
        """
        Extract discrete tasks from responsibility text.
        Split on: bullets (•, -), newlines, semicolons, numbered lists
        """
        if not isinstance(responsibility_text, str) or not responsibility_text.strip():
            return []
        
        # Replace common bullet characters with semicolon for uniform splitting
        text = responsibility_text.replace("•", ";").replace("- ", ";").replace("\n", ";")
        
        # Split on semicolons and colons
        fragments = re.split(r'[;:]', text)
        
        tasks = []
        for fragment in fragments:
            # Clean up each fragment
            fragment = fragment.strip()
            
            # Skip empty or very short fragments
            if len(fragment) < 4:
                continue
            
            # Remove EEOC statements, generic boilerplate
            if any(skip in fragment.lower() for skip in [
                "equal opportunity", "affirmative action", "minorities", 
                "veterans", "disability", "sexual orientation", "please apply",
                "apply at", "contact us", "see website", "learn more"
            ]):
                continue
            
            # Standardize: remove extra whitespace, normalize case
            fragment = re.sub(r'\s+', ' ', fragment)
            tasks.append(fragment)
        
        return tasks
    
    def normalize_task(self, task):
        """
        Normalize task text for better matching.
        - Lowercase
        - Remove punctuation at end
        - Standardize common patterns
        """
        task = task.lower().strip()
        task = task.rstrip('.,;:!')
        
        # Normalize common patterns
        task = re.sub(r'\b(you will|you should|may be required|required to)\b', '', task).strip()
        task = re.sub(r'\bmust\s+', '', task).strip()
        task = re.sub(r'\s+', ' ', task)  # Remove extra spaces
        
        return task
    
    def are_similar_tasks(self, task1, task2, threshold=0.85):
        """Check if two tasks are similar using sequence matching"""
        ratio = SequenceMatcher(None, task1, task2).ratio()
        return ratio >= threshold
    
    def deduplicate_tasks(self, tasks):
        """
        Deduplicate tasks using fuzzy matching.
        Keep first occurrence, merge metadata.
        """
        normalized = {self.normalize_task(t): t for t in tasks}
        unique = list(normalized.values())
        
        # Further fuzzy deduplication
        deduped = []
        for task in unique:
            norm_task = self.normalize_task(task)
            is_duplicate = False
            
            for existing in deduped:
                norm_existing = self.normalize_task(existing)
                if self.are_similar_tasks(norm_task, norm_existing, threshold=0.88):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                deduped.append(task)
        
        return deduped
    
    def aggregate_from_files(self):
        """Read all SOC Tier 1 CSVs and extract tasks"""
        files = self.find_soc_tier1_files()
        print(f"Found {len(files)} SOC Tier 1 analysis files")
        
        if not files:
            print("Warning: No SOC Tier 1 files found. Creating empty lexicon.")
            return
        
        all_tasks = []
        file_summary = {}
        
        for filepath in files:
            try:
                df = pd.read_csv(filepath, encoding='utf-8')
                
                if 'Responsibilities' not in df.columns:
                    print(f"  Skipping {filepath} - no Responsibilities column")
                    continue
                
                file_tasks = []
                for resp in df['Responsibilities'].dropna():
                    extracted = self.extract_tasks(str(resp))
                    file_tasks.extend(extracted)
                
                # Store file metadata
                file_key = os.path.basename(filepath)
                file_summary[file_key] = {
                    "path": filepath,
                    "total_tasks_extracted": len(file_tasks),
                    "source": "serpapi" if "serpapi" in filepath else "other"
                }
                
                all_tasks.extend(file_tasks)
                print(f"  ✓ {file_key}: {len(file_tasks)} tasks extracted")
                
            except Exception as e:
                print(f"  ✗ Error reading {filepath}: {e}")
                continue
        
        print(f"\nTotal tasks extracted: {len(all_tasks)}")
        
        # Store raw and deduplicate
        self.tasks = all_tasks
        self.unique_tasks = self.deduplicate_tasks(all_tasks)
        
        print(f"After deduplication: {len(self.unique_tasks)} unique tasks")
        
        # Calculate task frequency
        self.task_metadata['file_summary'] = file_summary
        self.task_metadata['total_tasks_extracted'] = len(all_tasks)
        self.task_metadata['unique_tasks_count'] = len(self.unique_tasks)
        self.task_metadata['deduplication_ratio'] = round(
            (1 - len(self.unique_tasks) / len(all_tasks)) * 100 if all_tasks else 0, 2
        )
    
    def save_consolidated_tasks(self):
        """Save consolidated tasks in multiple formats"""
        if not self.unique_tasks:
            print("No tasks to save. Skipping output generation.")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. JSON format (structured, with metadata)
        json_data = {
            "metadata": {
                "timestamp": timestamp,
                "date_created": datetime.now().isoformat(),
                "total_unique_tasks": len(self.unique_tasks),
                "deduplication_ratio_percent": self.task_metadata.get('deduplication_ratio', 0),
                "files_processed": len(self.task_metadata.get('file_summary', {}))
            },
            "file_summary": self.task_metadata.get('file_summary', {}),
            "tasks": [
                {
                    "id": f"TASK_{i:04d}",
                    "text": task,
                    "normalized": self.normalize_task(task),
                    "character_count": len(task),
                    "word_count": len(task.split())
                }
                for i, task in enumerate(self.unique_tasks, 1)
            ]
        }
        
        json_path = os.path.join(self.output_folder, f"consolidated_tasks_{timestamp}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"✓ Saved: {json_path}")
        
        # 2. CSV format (for human review)
        csv_data = []
        for i, task in enumerate(self.unique_tasks, 1):
            csv_data.append({
                'Task ID': f'TASK_{i:04d}',
                'Task Description': task,
                'Word Count': len(task.split()),
                'Character Count': len(task)
            })
        
        csv_df = pd.DataFrame(csv_data)
        csv_path = os.path.join(self.output_folder, f"consolidated_tasks_{timestamp}.csv")
        csv_df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"✓ Saved: {csv_path}")
        
        # 3. Frequency report (text)
        task_freq = Counter(self.normalize_task(t) for t in self.unique_tasks)
        
        report_path = os.path.join(self.output_folder, f"task_frequency_report_{timestamp}.txt")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("TASK LEXICON FREQUENCY REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Unique Tasks: {len(self.unique_tasks)}\n")
            f.write(f"Total Tasks Before Dedup: {self.task_metadata.get('total_tasks_extracted', 0)}\n")
            f.write(f"Deduplication Rate: {self.task_metadata.get('deduplication_ratio', 0)}%\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("TOP 30 MOST COMMON NORMALIZED PATTERNS\n")
            f.write("-" * 80 + "\n\n")
            
            for i, (norm_task, freq) in enumerate(task_freq.most_common(30), 1):
                f.write(f"{i:2d}. [{freq:3d}x] {norm_task}\n")
            
            f.write("\n" + "-" * 80 + "\n")
            f.write("ALL UNIQUE TASKS (sorted by length)\n")
            f.write("-" * 80 + "\n\n")
            
            for i, task in enumerate(sorted(self.unique_tasks, key=len, reverse=True), 1):
                f.write(f"{i:4d}. {task}\n")
        
        print(f"✓ Saved: {report_path}")
        
        return json_path, csv_path, report_path
    
    def compare_with_previous(self):
        """Compare current tasks with previous aggregation (if exists)"""
        # Find most recent previous aggregation
        existing_jsons = [
            f for f in os.listdir(self.output_folder)
            if f.startswith("consolidated_tasks_") and f.endswith(".json")
        ]
        
        if not existing_jsons:
            print("No previous aggregation found. Skipping delta analysis.")
            return None
        
        latest_json = sorted(existing_jsons)[-1]
        latest_path = os.path.join(self.output_folder, latest_json)
        
        try:
            with open(latest_path, 'r', encoding='utf-8') as f:
                previous = json.load(f)
            
            previous_tasks = set(t['text'] for t in previous.get('tasks', []))
            current_tasks = set(self.unique_tasks)
            
            new_tasks = current_tasks - previous_tasks
            removed_tasks = previous_tasks - current_tasks
            
            delta = {
                "timestamp": datetime.now().isoformat(),
                "compared_with": latest_json,
                "previous_count": len(previous_tasks),
                "current_count": len(current_tasks),
                "new_tasks": list(new_tasks),
                "removed_tasks": list(removed_tasks),
                "new_count": len(new_tasks),
                "removed_count": len(removed_tasks),
                "net_change": len(new_tasks) - len(removed_tasks)
            }
            
            delta_path = os.path.join(self.output_folder, "task_delta_latest.json")
            with open(delta_path, 'w', encoding='utf-8') as f:
                json.dump(delta, f, ensure_ascii=False, indent=2)
            
            print(f"\n✓ Delta Analysis:")
            print(f"  Previous tasks: {len(previous_tasks)}")
            print(f"  Current tasks: {len(current_tasks)}")
            print(f"  New tasks: {len(new_tasks)}")
            print(f"  Removed tasks: {len(removed_tasks)}")
            print(f"  Saved: {delta_path}")
            
            return delta_path
            
        except Exception as e:
            print(f"Error comparing with previous: {e}")
            return None
    
    def run(self):
        """Execute full aggregation pipeline"""
        print("=" * 80)
        print("TASK AGGREGATOR - Consolidating SOC Job Task Lexicon")
        print("=" * 80 + "\n")
        
        # Step 1: Find and aggregate files
        self.aggregate_from_files()
        
        # Step 2: Save outputs
        if self.unique_tasks:
            json_path, csv_path, report_path = self.save_consolidated_tasks()
            
            # Step 3: Compare with previous
            delta_path = self.compare_with_previous()
            
            print("\n" + "=" * 80)
            print("✓ AGGREGATION COMPLETE")
            print("=" * 80)
            return {
                "status": "success",
                "unique_tasks_count": len(self.unique_tasks),
                "output_json": json_path,
                "output_csv": csv_path,
                "output_report": report_path,
                "output_delta": delta_path
            }
        else:
            print("\n✗ No tasks to output. Check input files.")
            return {"status": "error", "message": "No valid tasks found"}


if __name__ == "__main__":
    aggregator = TaskAggregator()
    result = aggregator.run()
    print(json.dumps(result, indent=2))

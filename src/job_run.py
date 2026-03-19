"""
job_run.py

Full SOC Job Task Analysis Pipeline Orchestrator.

Complete workflow:
1. Data Aggregation: Consolidate newly scraped jobs
2. Classification & Normalization: Apply domain rules to classify jobs
3. Task Extraction: Extract and deduplicate tasks from SOC Tier 1 descriptions
4. Pre-LLM Clustering: Group tasks into candidate themes (with confidence scores)
5. Output: Prepare materials for LLM semantic analysis

Usage:
  python job_run.py                    # Run full pipeline with latest data
  python job_run.py --skip-raw         # Skip raw data aggregation (test mode)
  python job_run.py --cluster-only     # Run only clustering step
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from data_analyzer import analyze_job_data, load_rules
from task_aggregator import TaskAggregator
from task_thematic_clusterer import TaskThematicClusterer
import pandas as pd


class PipelineOrchestrator:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.results = {}
        self.start_time = datetime.now()
    
    def log(self, message, level="INFO"):
        """Log pipeline progress"""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}")
    
    def step_1_classify_recent_jobs(self, rules_file="configs/rules.json"):
        """
        Step 1: Find latest processed CSV and classify jobs
        (Usually called by data_analsyer on a single file)
        """
        self.log("=" * 80, "STEP")
        self.log("STEP 1: Job Classification & Tier 1 Filtering", "STEP")
        self.log("=" * 80, "STEP")
        
        # Find the most recent processed CSV
        processed_dir = Path("data/processed")
        
        # Look for latest flattened CSV (not analysis files)
        csv_files = sorted(
            processed_dir.glob("soc_jobs_flattened_*.csv"),
            key=os.path.getmtime,
            reverse=True
        )
        
        # Filter out analysis/unclassified files
        csv_files = [
            f for f in csv_files
            if "_analysis" not in f.name and "_unclassified" not in f.name
        ]
        
        if not csv_files:
            # Check in serpapi subfolder
            serpapi_csvs = sorted(
                processed_dir.glob("serpapi_*/soc_jobs_flattened_*.csv"),
                key=os.path.getmtime,
                reverse=True
            )
            csv_files = serpapi_csvs
        
        if not csv_files:
            self.log("No processed CSV files found", "ERROR")
            return False
        
        latest_csv = csv_files[0]
        self.log(f"Found latest CSV: {latest_csv}")
        
        # Run classification
        try:
            df = pd.read_csv(latest_csv, encoding='utf-8')
            self.log(f"Loaded {len(df)} jobs from CSV")
            
            # Apply analysis (this creates the *_soc_tier1_analysis.csv)
            soc1_df, unclassified_df, stats = analyze_job_data(df, rules_file)
            
            if soc1_df is not None:
                self.log(f"Classification complete: {stats['soc_tier1_count']} SOC Tier 1 jobs found")
                self.results['step_1'] = {
                    "status": "success",
                    "jobs_classified": len(df),
                    "soc_tier1_count": stats['soc_tier1_count'],
                    "unclassified_count": stats['unclassified_count']
                }
                return True
            else:
                self.log("Classification failed", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Error in classification: {e}", "ERROR")
            return False
    
    def step_2_aggregate_tasks(self):
        """
        Step 2: Consolidate all historical SOC Tier 1 job descriptions
        Extract and deduplicate tasks across all jobs and dates
        """
        self.log("\n" + "=" * 80, "STEP")
        self.log("STEP 2: Task Aggregation & Normalization", "STEP")
        self.log("=" * 80, "STEP")
        
        try:
            aggregator = TaskAggregator()
            result = aggregator.run()
            
            if result['status'] == 'success':
                self.log(f"✓ Aggregation complete: {result['unique_tasks_count']} unique tasks")
                self.results['step_2'] = result
                return True
            else:
                self.log(f"✗ Aggregation failed: {result.get('message', 'Unknown error')}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Error in task aggregation: {e}", "ERROR")
            return False
    
    def step_3_cluster_tasks(self):
        """
        Step 3 (BONUS): Pre-LLM thematic clustering
        Group tasks by keyword patterns with confidence scores
        """
        self.log("\n" + "=" * 80, "STEP")
        self.log("STEP 3 (BONUS): Pre-LLM Thematic Clustering", "STEP")
        self.log("=" * 80, "STEP")
        
        try:
            clusterer = TaskThematicClusterer()
            result = clusterer.run()
            
            if result['status'] == 'success':
                self.log(f"✓ Clustering complete: {result['unique_themes']} themes identified")
                self.log(f"  - Clustered tasks: {result['clustered_tasks']}")
                self.log(f"  - Unclustered (review): {result['unclustered_tasks']}")
                self.results['step_3'] = result
                return True
            else:
                self.log(f"✗ Clustering failed: {result.get('message', 'Unknown error')}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Error in task clustering: {e}", "ERROR")
            return False
    
    def generate_summary(self):
        """Generate pipeline execution summary"""
        self.log("\n" + "=" * 80, "SUMMARY")
        self.log("PIPELINE EXECUTION SUMMARY", "SUMMARY")
        self.log("=" * 80, "SUMMARY")
        
        duration = (datetime.now() - self.start_time).total_seconds()
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": duration,
            "steps_completed": len(self.results),
            "results": self.results
        }
        
        # Print summary
        for step, data in self.results.items():
            status = "✓" if data.get('status') == 'success' else "✗"
            self.log(f"{status} {step}: {data.get('status', 'unknown').upper()}")
        
        self.log(f"Total duration: {duration:.2f}s")
        
        # Save summary
        summary_path = f"data/processed/task_lexicon/pipeline_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs(os.path.dirname(summary_path), exist_ok=True)
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        self.log(f"Summary saved to: {summary_path}")
        
        return summary_path
    
    def run(self, steps=None, skip_raw=False, cluster_only=False):
        """
        Execute pipeline
        
        Args:
            steps: List of steps to run (default: all)
            skip_raw: Skip Step 1 (classification) - use existing SOC Tier 1 CSVs
            cluster_only: Run only Step 3 (clustering)
        """
        if cluster_only:
            self.log("Starting pipeline (CLUSTERING ONLY MODE)")
            return self.step_3_cluster_tasks()
        
        if not skip_raw:
            if not self.step_1_classify_recent_jobs():
                self.log("Pipeline failed at Step 1", "ERROR")
                return False
        else:
            self.log("Skipped Step 1 (classification) - using existing SOC Tier 1 files")
        
        if not self.step_2_aggregate_tasks():
            self.log("Pipeline failed at Step 2", "ERROR")
            return False
        
        if not self.step_3_cluster_tasks():
            self.log("Pipeline failed at Step 3 (non-fatal - clustering is bonus)", "WARN")
            # Don't fail, clustering is optional
        
        self.generate_summary()
        self.log("\n✓ PIPELINE COMPLETE", "SUCCESS")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="SOC Job Task Analysis Pipeline - Full Orchestration"
    )
    parser.add_argument(
        "--skip-raw",
        action="store_true",
        help="Skip job classification (Step 1) - use existing SOC Tier 1 CSVs"
    )
    parser.add_argument(
        "--cluster-only",
        action="store_true",
        help="Run only clustering step (Step 3)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=True,
        help="Verbose output (default: True)"
    )
    
    args = parser.parse_args()
    
    # Create orchestrator and run
    orchestrator = PipelineOrchestrator(verbose=args.verbose)
    success = orchestrator.run(
        skip_raw=args.skip_raw,
        cluster_only=args.cluster_only
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
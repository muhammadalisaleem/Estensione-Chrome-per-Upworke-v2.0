"""
Data Collection Script for Upwork Job Scorer ML
Helps collect and label job data for training
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Data directory
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Output files
DATASET_FILE = DATA_DIR / "initial_dataset.csv"
JSON_BACKUP = DATA_DIR / "initial_dataset.json"


class JobLabeler:
    """Interactive job labeling tool"""
    
    def __init__(self):
        self.jobs: List[Dict] = []
        self.load_existing_data()
    
    def load_existing_data(self):
        """Load existing dataset if available"""
        if DATASET_FILE.exists():
            with open(DATASET_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.jobs = list(reader)
            print(f"Loaded {len(self.jobs)} existing jobs")
        else:
            print("No existing dataset found. Starting fresh.")
    
    def add_job(self, job_data: Dict):
        """Add a labeled job to the dataset"""
        
        # Validate required fields
        required_fields = [
            'job_id', 'title', 'description', 'proposals', 
            'payment_verified', 'client_spending', 'client_rating',
            'posted_time_seconds', 'quality_label'
        ]
        
        for field in required_fields:
            if field not in job_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate quality label
        if job_data['quality_label'] not in ['excellent', 'good', 'poor', 'spam']:
            raise ValueError("quality_label must be 'excellent', 'good', 'poor', or 'spam'")
        
        # Add timestamp
        job_data['labeled_at'] = datetime.now().isoformat()
        
        self.jobs.append(job_data)
        print(f"Added job: {job_data['title'][:50]}... (Label: {job_data['quality_label']})")
    
    def interactive_labeling(self):
        """Interactive command-line labeling"""
        print("\n" + "="*80)
        print("INTERACTIVE JOB LABELING")
        print("="*80)
        print("\nEnter job details and label them for training.")
        print("Quality labels: excellent, good, poor, spam")
        print("Type 'done' when finished, 'stats' for statistics\n")
        
        while True:
            command = input("\nCommand (add/stats/done): ").strip().lower()
            
            if command == 'done':
                break
            elif command == 'stats':
                self.print_statistics()
                continue
            elif command != 'add':
                print("Unknown command. Use 'add', 'stats', or 'done'")
                continue
            
            try:
                job_data = self.collect_job_input()
                self.add_job(job_data)
            except KeyboardInterrupt:
                print("\nLabeling interrupted")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def collect_job_input(self) -> Dict:
        """Collect job data from user input"""
        print("\n--- Enter Job Details ---")
        
        job_data = {
            'job_id': input("Job ID: ").strip(),
            'title': input("Title: ").strip(),
            'description': input("Description (full text): ").strip(),
            'proposals': input("Number of proposals: ").strip(),
            'payment_verified': input("Payment verified (yes/no): ").strip().lower() == 'yes',
            'client_spending': input("Client spending ($): ").strip(),
            'client_rating': input("Client rating (0-5): ").strip(),
            'posted_time_seconds': input("Posted time (seconds ago): ").strip(),
            'job_type': input("Job type (fixed/hourly): ").strip(),
            'budget': input("Budget ($, optional): ").strip() or "0",
            'hourly_rate': input("Hourly rate ($/hr, optional): ").strip() or "0",
        }
        
        # Label the job
        print("\nQuality Labels:")
        print("  excellent - High-quality client, clear requirements, fair pay")
        print("  good      - Decent client, reasonable requirements")
        print("  poor      - Low quality, vague, or low budget")
        print("  spam      - Scam or fraudulent posting")
        
        quality_label = input("Quality label: ").strip().lower()
        job_data['quality_label'] = quality_label
        
        return job_data
    
    def import_from_json(self, json_file: Path):
        """Import jobs from JSON file"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            for job in data:
                self.add_job(job)
        else:
            self.add_job(data)
        
        print(f"Imported {len(data) if isinstance(data, list) else 1} jobs from {json_file}")
    
    def save(self):
        """Save dataset to CSV and JSON"""
        if not self.jobs:
            print("No jobs to save")
            return
        
        # Save as CSV
        fieldnames = list(self.jobs[0].keys())
        with open(DATASET_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.jobs)
        
        # Save as JSON backup
        with open(JSON_BACKUP, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, indent=2, ensure_ascii=False)
        
        print(f"\nDataset saved!")
        print(f"  CSV: {DATASET_FILE}")
        print(f"  JSON: {JSON_BACKUP}")
        print(f"  Total jobs: {len(self.jobs)}")
    
    def print_statistics(self):
        """Print dataset statistics"""
        if not self.jobs:
            print("No jobs in dataset")
            return
        
        print("\n" + "="*80)
        print("DATASET STATISTICS")
        print("="*80)
        print(f"Total jobs: {len(self.jobs)}")
        
        # Count by quality label
        label_counts = {}
        for job in self.jobs:
            label = job['quality_label']
            label_counts[label] = label_counts.get(label, 0) + 1
        
        print("\nQuality Distribution:")
        for label, count in sorted(label_counts.items()):
            percentage = (count / len(self.jobs)) * 100
            print(f"  {label:12s}: {count:3d} ({percentage:5.1f}%)")
        
        # Payment verification stats
        verified_count = sum(1 for job in self.jobs if job.get('payment_verified'))
        print(f"\nPayment Verified: {verified_count}/{len(self.jobs)} ({verified_count/len(self.jobs)*100:.1f}%)")


def main():
    """Main function"""
    labeler = JobLabeler()
    
    print("Upwork Job Scorer - Data Collection Tool")
    print("=" * 80)
    
    # Check if there's data to import
    import_file = DATA_DIR / "import.json"
    if import_file.exists():
        response = input(f"\nFound {import_file}. Import it? (yes/no): ").strip().lower()
        if response == 'yes':
            try:
                labeler.import_from_json(import_file)
                import_file.rename(DATA_DIR / f"imported_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            except Exception as e:
                print(f"Import failed: {e}")
    
    # Interactive labeling
    labeler.interactive_labeling()
    
    # Print statistics
    labeler.print_statistics()
    
    # Save
    if labeler.jobs:
        labeler.save()
    
    print("\nDone!")


if __name__ == "__main__":
    main()

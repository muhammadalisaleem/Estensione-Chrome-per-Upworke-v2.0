"""
Kaggle Dataset Importer
Downloads and adapts job posting datasets from Kaggle for training
"""

import os
import json
import csv
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
import re
from datetime import datetime

# Data directory
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

KAGGLE_DIR = DATA_DIR / "kaggle_imports"
KAGGLE_DIR.mkdir(exist_ok=True)


class KaggleDatasetAdapter:
    """Adapts Kaggle datasets to our job labeling format"""
    
    def __init__(self):
        self.imported_jobs: List[Dict] = []
    
    def download_dataset(self, dataset_name: str):
        """
        Download a dataset from Kaggle
        
        Args:
            dataset_name: Kaggle dataset identifier (e.g., 'username/dataset-name')
        """
        try:
            import kaggle
            
            print(f"\n📥 Downloading dataset: {dataset_name}")
            print(f"   Destination: {KAGGLE_DIR}")
            
            kaggle.api.dataset_download_files(
                dataset_name,
                path=str(KAGGLE_DIR),
                unzip=True
            )
            
            print(f"✅ Download complete!")
            
        except ImportError:
            print("❌ Kaggle package not installed. Run: pip install kaggle")
            print("\nTo use Kaggle API:")
            print("1. Go to https://www.kaggle.com/account")
            print("2. Create API token (downloads kaggle.json)")
            print("3. Place kaggle.json in: ~/.kaggle/ (Linux/Mac) or C:\\Users\\<user>\\.kaggle\\ (Windows)")
            raise
        except Exception as e:
            print(f"❌ Download failed: {e}")
            raise
    
    def list_available_files(self):
        """List all files in kaggle imports directory"""
        files = list(KAGGLE_DIR.glob("*.csv"))
        
        if not files:
            print("No CSV files found in kaggle_imports/")
            return []
        
        print(f"\n📁 Available files in {KAGGLE_DIR}:")
        for i, file in enumerate(files, 1):
            size_mb = file.stat().st_size / (1024 * 1024)
            print(f"   {i}. {file.name} ({size_mb:.2f} MB)")
        
        return files
    
    def preview_csv(self, csv_path: Path, rows: int = 5):
        """Preview a CSV file"""
        print(f"\n📊 Preview of {csv_path.name}:")
        
        df = pd.read_csv(csv_path, nrows=rows)
        print(f"\nColumns: {list(df.columns)}")
        print(f"Total rows (sampled): {rows}")
        print("\nFirst few rows:")
        print(df.head())
        
        return df
    
    def import_generic_job_dataset(
        self,
        csv_path: Path,
        mapping: Dict[str, str],
        default_values: Dict[str, any] = None
    ):
        """
        Import a generic job dataset with column mapping
        
        Args:
            csv_path: Path to CSV file
            mapping: Dictionary mapping our fields to dataset columns
                Example: {'title': 'job_title', 'description': 'job_desc', ...}
            default_values: Default values for missing fields
        """
        print(f"\n🔄 Importing {csv_path.name}...")
        
        df = pd.read_csv(csv_path)
        print(f"   Total rows: {len(df)}")
        
        defaults = default_values or {}
        imported_count = 0
        
        for idx, row in df.iterrows():
            try:
                job_data = self._map_row_to_job(row, mapping, defaults)
                
                # Auto-label based on heuristics if no label provided
                if 'quality_label' not in job_data or not job_data['quality_label']:
                    job_data['quality_label'] = self._auto_label_job(job_data)
                
                self.imported_jobs.append(job_data)
                imported_count += 1
                
                if imported_count % 100 == 0:
                    print(f"   Processed {imported_count} jobs...")
                    
            except Exception as e:
                print(f"   ⚠️  Skipped row {idx}: {e}")
                continue
        
        print(f"✅ Imported {imported_count} jobs from {csv_path.name}")
        return imported_count
    
    def _map_row_to_job(self, row: pd.Series, mapping: Dict, defaults: Dict) -> Dict:
        """Map a CSV row to our job format"""
        
        job_data = {
            'job_id': self._safe_get(row, mapping.get('job_id'), f"kaggle_{row.name}"),
            'title': self._safe_get(row, mapping.get('title'), 'Unknown'),
            'description': self._safe_get(row, mapping.get('description'), ''),
            'proposals': str(self._safe_get(row, mapping.get('proposals'), defaults.get('proposals', '25'))),
            'payment_verified': self._safe_get(row, mapping.get('payment_verified'), defaults.get('payment_verified', False)),
            'client_spending': str(self._safe_get(row, mapping.get('client_spending'), defaults.get('client_spending', '5000'))),
            'client_rating': str(self._safe_get(row, mapping.get('client_rating'), defaults.get('client_rating', '4.0'))),
            'posted_time_seconds': str(self._safe_get(row, mapping.get('posted_time_seconds'), defaults.get('posted_time_seconds', '86400'))),
            'job_type': self._safe_get(row, mapping.get('job_type'), defaults.get('job_type', 'fixed')),
            'budget': str(self._safe_get(row, mapping.get('budget'), defaults.get('budget', '1000'))),
            'hourly_rate': str(self._safe_get(row, mapping.get('hourly_rate'), defaults.get('hourly_rate', '25'))),
            'quality_label': self._safe_get(row, mapping.get('quality_label'), ''),
            'labeled_at': datetime.now().isoformat(),
            'source': 'kaggle_import',
        }
        
        return job_data
    
    def _safe_get(self, row: pd.Series, column: Optional[str], default: any):
        """Safely get a value from a row"""
        if not column or column not in row:
            return default
        
        value = row[column]
        
        # Handle NaN values
        if pd.isna(value):
            return default
        
        return value
    
    def _auto_label_job(self, job_data: Dict) -> str:
        """
        Auto-label job based on heuristics
        This is a rough approximation - manual review is recommended
        """
        description = job_data['description'].lower()
        title = job_data['title'].lower()
        
        # Check for spam indicators
        spam_patterns = [
            r'\b\d{10,}\b',  # Long numbers (phone)
            r'\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b',  # Email
            r'\bwhatsapp\b', r'\bskype\b', r'\btelegram\b',  # Off-platform
            r'\bcontact me\b', r'\bcall me\b',
            r'\bwork from home\b.*\bearn\b.*\$\d+',  # MLM patterns
        ]
        
        for pattern in spam_patterns:
            if re.search(pattern, description) or re.search(pattern, title):
                return 'spam'
        
        # Check for poor quality indicators
        poor_indicators = [
            len(description) < 100,  # Too short
            'asap' in description or 'urgent' in title,
            'simple' in title and 'quick' in title,
            float(job_data.get('client_rating', '0')) < 3.0,
        ]
        
        if sum(poor_indicators) >= 2:
            return 'poor'
        
        # Check for excellent indicators
        excellent_indicators = [
            job_data.get('payment_verified', False),
            float(job_data.get('client_spending', '0')) > 10000,
            float(job_data.get('client_rating', '0')) >= 4.5,
            len(description) > 300,
        ]
        
        if sum(excellent_indicators) >= 3:
            return 'excellent'
        
        # Default to 'good'
        return 'good'
    
    def export_to_csv(self, output_path: Path):
        """Export imported jobs to CSV"""
        if not self.imported_jobs:
            print("No jobs to export")
            return
        
        fieldnames = list(self.imported_jobs[0].keys())
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.imported_jobs)
        
        print(f"\n✅ Exported {len(self.imported_jobs)} jobs to {output_path}")
    
    def print_statistics(self):
        """Print statistics about imported data"""
        if not self.imported_jobs:
            print("No jobs imported yet")
            return
        
        print("\n" + "="*80)
        print("IMPORT STATISTICS")
        print("="*80)
        print(f"Total jobs: {len(self.imported_jobs)}")
        
        # Count by quality label
        label_counts = {}
        for job in self.imported_jobs:
            label = job['quality_label']
            label_counts[label] = label_counts.get(label, 0) + 1
        
        print("\nQuality Distribution:")
        for label, count in sorted(label_counts.items()):
            percentage = (count / len(self.imported_jobs)) * 100
            print(f"  {label:12s}: {count:4d} ({percentage:5.1f}%)")
        
        print("\n⚠️  Note: Labels were auto-generated. Manual review recommended!")


def interactive_kaggle_import():
    """Interactive Kaggle dataset import"""
    print("="*80)
    print("KAGGLE DATASET IMPORTER")
    print("="*80)
    
    adapter = KaggleDatasetAdapter()
    
    print("\n📚 Recommended Kaggle datasets for job postings:")
    print("   1. austinreese/usa-job-postings")
    print("   2. madhab/jobposts")
    print("   3. airiddha/trainrev1")
    print("   4. PromptCloudHQ/us-technology-jobs-on-dice-com")
    print("   5. Or search: https://www.kaggle.com/datasets?search=job+postings")
    
    while True:
        print("\n" + "="*80)
        print("OPTIONS:")
        print("  1. Download dataset from Kaggle")
        print("  2. List available CSV files")
        print("  3. Preview a CSV file")
        print("  4. Import a CSV file with mapping")
        print("  5. Export imported jobs")
        print("  6. Show statistics")
        print("  0. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            dataset_name = input("Enter dataset name (e.g., 'username/dataset-name'): ").strip()
            try:
                adapter.download_dataset(dataset_name)
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            adapter.list_available_files()
        
        elif choice == '3':
            files = adapter.list_available_files()
            if files:
                file_num = input("Enter file number to preview: ").strip()
                try:
                    file_idx = int(file_num) - 1
                    adapter.preview_csv(files[file_idx])
                except (ValueError, IndexError):
                    print("Invalid file number")
        
        elif choice == '4':
            files = adapter.list_available_files()
            if files:
                file_num = input("Enter file number to import: ").strip()
                try:
                    file_idx = int(file_num) - 1
                    csv_path = files[file_idx]
                    
                    # Show preview
                    df = adapter.preview_csv(csv_path, rows=3)
                    
                    print("\n📝 Create column mapping:")
                    print("   Enter the column name from the dataset for each field.")
                    print("   Leave blank to use defaults.\n")
                    
                    mapping = {}
                    our_fields = ['title', 'description', 'proposals', 'payment_verified',
                                'client_spending', 'client_rating', 'job_type', 'budget']
                    
                    for field in our_fields:
                        col = input(f"   {field}: ").strip()
                        if col:
                            mapping[field] = col
                    
                    # Default values
                    defaults = {
                        'proposals': '25',
                        'payment_verified': False,
                        'client_spending': '5000',
                        'client_rating': '4.0',
                        'posted_time_seconds': '86400',
                        'job_type': 'fixed',
                        'budget': '1000',
                        'hourly_rate': '25',
                    }
                    
                    adapter.import_generic_job_dataset(csv_path, mapping, defaults)
                    adapter.print_statistics()
                    
                except (ValueError, IndexError):
                    print("Invalid file number")
                except Exception as e:
                    print(f"Import error: {e}")
        
        elif choice == '5':
            if adapter.imported_jobs:
                output_file = DATA_DIR / "kaggle_imported_jobs.csv"
                adapter.export_to_csv(output_file)
                
                # Also save as JSON backup
                json_file = DATA_DIR / "kaggle_imported_jobs.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(adapter.imported_jobs, f, indent=2)
                print(f"   JSON backup: {json_file}")
            else:
                print("No jobs to export")
        
        elif choice == '6':
            adapter.print_statistics()
        
        else:
            print("Invalid choice")
    
    print("\nDone!")


def quick_import_example():
    """Example: Quick import of a common job dataset"""
    adapter = KaggleDatasetAdapter()
    
    # Example mapping for a typical job posting dataset
    mapping = {
        'title': 'job_title',
        'description': 'job_description',
        'job_type': 'employment_type',
    }
    
    defaults = {
        'proposals': '30',
        'payment_verified': False,
        'client_spending': '5000',
        'client_rating': '4.0',
        'posted_time_seconds': '86400',
        'budget': '1500',
    }
    
    # Find CSV file
    csv_files = list(KAGGLE_DIR.glob("*.csv"))
    if csv_files:
        adapter.import_generic_job_dataset(csv_files[0], mapping, defaults)
        adapter.print_statistics()
        
        output_file = DATA_DIR / "kaggle_imported_jobs.csv"
        adapter.export_to_csv(output_file)


if __name__ == "__main__":
    interactive_kaggle_import()

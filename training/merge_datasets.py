"""
Merge Multiple Datasets
Combines Kaggle imports, manual labels, and other sources into final dataset
"""

import pandas as pd
from pathlib import Path
from datetime import datetime


def merge_datasets(
    input_files: list,
    output_file: Path,
    remove_duplicates: bool = True,
    balance_labels: bool = False
):
    """
    Merge multiple CSV datasets
    
    Args:
        input_files: List of CSV file paths
        output_file: Output path for merged dataset
        remove_duplicates: Remove duplicate job_ids
        balance_labels: Balance dataset across quality labels
    """
    print("="*80)
    print("DATASET MERGER")
    print("="*80)
    
    all_data = []
    
    # Load all datasets
    for file_path in input_files:
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"⚠️  Skipping {file_path.name} (not found)")
            continue
        
        print(f"\n📁 Loading {file_path.name}...")
        df = pd.read_csv(file_path)
        print(f"   Rows: {len(df)}")
        
        # Show label distribution
        if 'quality_label' in df.columns:
            label_counts = df['quality_label'].value_counts()
            for label, count in label_counts.items():
                print(f"      {label}: {count}")
        
        all_data.append(df)
    
    if not all_data:
        print("\n❌ No valid datasets found!")
        return
    
    # Combine all datasets
    print(f"\n🔗 Merging {len(all_data)} datasets...")
    combined = pd.concat(all_data, ignore_index=True)
    print(f"   Total rows before deduplication: {len(combined)}")
    
    # Remove duplicates
    if remove_duplicates:
        print("\n🔍 Removing duplicates...")
        original_count = len(combined)
        
        # Remove duplicates by job_id
        if 'job_id' in combined.columns:
            combined = combined.drop_duplicates(subset=['job_id'], keep='first')
        
        # Also remove near-duplicates by title+description
        combined = combined.drop_duplicates(subset=['title', 'description'], keep='first')
        
        removed = original_count - len(combined)
        print(f"   Removed {removed} duplicates")
        print(f"   Remaining rows: {len(combined)}")
    
    # Balance labels
    if balance_labels:
        print("\n⚖️  Balancing dataset...")
        combined = balance_dataset(combined)
    
    # Show final statistics
    print("\n" + "="*80)
    print("FINAL DATASET STATISTICS")
    print("="*80)
    print(f"Total jobs: {len(combined)}")
    
    if 'quality_label' in combined.columns:
        print("\nQuality Label Distribution:")
        label_counts = combined['quality_label'].value_counts()
        for label, count in label_counts.items():
            percentage = (count / len(combined)) * 100
            print(f"  {label:12s}: {count:4d} ({percentage:5.1f}%)")
    
    if 'source' in combined.columns:
        print("\nData Sources:")
        source_counts = combined['source'].value_counts()
        for source, count in source_counts.items():
            percentage = (count / len(combined)) * 100
            print(f"  {source:20s}: {count:4d} ({percentage:5.1f}%)")
    
    # Save merged dataset
    print(f"\n💾 Saving to {output_file}...")
    combined.to_csv(output_file, index=False)
    
    # Save JSON backup
    json_file = output_file.with_suffix('.json')
    combined.to_json(json_file, orient='records', indent=2)
    print(f"   JSON backup: {json_file}")
    
    print("\n✅ Merge complete!")
    
    return combined


def balance_dataset(df: pd.DataFrame, target_per_label: int = None) -> pd.DataFrame:
    """
    Balance dataset by sampling equal numbers from each label
    
    Args:
        df: Input dataframe
        target_per_label: Target number per label (None = use minimum)
    """
    if 'quality_label' not in df.columns:
        return df
    
    label_counts = df['quality_label'].value_counts()
    
    if target_per_label is None:
        target_per_label = label_counts.min()
    
    print(f"   Target per label: {target_per_label}")
    
    balanced_dfs = []
    for label in label_counts.index:
        label_df = df[df['quality_label'] == label]
        
        if len(label_df) > target_per_label:
            # Downsample
            sampled = label_df.sample(n=target_per_label, random_state=42)
        else:
            # Keep all
            sampled = label_df
        
        balanced_dfs.append(sampled)
        print(f"      {label}: {len(label_df)} → {len(sampled)}")
    
    balanced = pd.concat(balanced_dfs, ignore_index=True)
    
    # Shuffle
    balanced = balanced.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return balanced


def main():
    """Interactive dataset merger"""
    data_dir = Path(__file__).parent / "data"
    
    # Find available datasets
    csv_files = list(data_dir.glob("*.csv"))
    csv_files = [f for f in csv_files if not f.name.startswith('final_')]
    
    if not csv_files:
        print("No CSV files found in data/ directory")
        return
    
    print("Available datasets:")
    for i, file in enumerate(csv_files, 1):
        size_mb = file.stat().st_size / (1024 * 1024)
        print(f"  {i}. {file.name} ({size_mb:.2f} MB)")
    
    print("\nWhich datasets would you like to merge?")
    print("Enter numbers separated by spaces (e.g., '1 2 3'), or 'all' for all files:")
    
    choice = input("> ").strip().lower()
    
    if choice == 'all':
        selected_files = csv_files
    else:
        try:
            indices = [int(x) - 1 for x in choice.split()]
            selected_files = [csv_files[i] for i in indices]
        except (ValueError, IndexError):
            print("Invalid input")
            return
    
    print(f"\nSelected {len(selected_files)} files")
    
    # Ask about balancing
    balance = input("\nBalance dataset across labels? (yes/no): ").strip().lower() == 'yes'
    
    # Output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = data_dir / f"final_dataset_{timestamp}.csv"
    
    # Merge
    merge_datasets(
        selected_files,
        output_file,
        remove_duplicates=True,
        balance_labels=balance
    )
    
    print(f"\n📁 Merged dataset: {output_file}")
    print("\n✅ Ready for model training!")


if __name__ == "__main__":
    main()

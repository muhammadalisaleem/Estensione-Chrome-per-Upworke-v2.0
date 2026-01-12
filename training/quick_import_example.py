"""
Quick Example: Import Job Dataset from Kaggle
This script demonstrates how to quickly import and process a Kaggle dataset
"""

from kaggle_import import KaggleDatasetAdapter
from pathlib import Path

def main():
    print("="*80)
    print("QUICK KAGGLE IMPORT EXAMPLE")
    print("="*80)
    
    adapter = KaggleDatasetAdapter()
    
    # Step 1: Download a popular job dataset
    print("\n📥 Step 1: Downloading dataset from Kaggle...")
    print("   Dataset: austinreese/usa-job-postings")
    print("   (Contains 19,000+ US job postings)\n")
    
    try:
        adapter.download_dataset('austinreese/usa-job-postings')
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        print("\nMake sure you have:")
        print("  1. Installed kaggle: pip install kaggle")
        print("  2. Set up API credentials (see KAGGLE_SETUP.md)")
        return
    
    # Step 2: Find the downloaded CSV
    print("\n📁 Step 2: Finding downloaded files...")
    files = adapter.list_available_files()
    
    if not files:
        print("No CSV files found. Check if download was successful.")
        return
    
    csv_file = files[0]  # Use first CSV file
    
    # Step 3: Preview the data
    print(f"\n👀 Step 3: Previewing {csv_file.name}...")
    adapter.preview_csv(csv_file, rows=3)
    
    # Step 4: Define column mapping
    # This mapping is for the austinreese/usa-job-postings dataset
    # Adjust based on the actual columns in your dataset
    print("\n🗺️  Step 4: Mapping columns...")
    
    mapping = {
        'title': 'job_title',          # Map their 'job_title' to our 'title'
        'description': 'description',   # Map their 'description' to our 'description'
        'job_type': 'employment_type',  # Map their 'employment_type' to our 'job_type'
    }
    
    defaults = {
        'proposals': '30',
        'payment_verified': False,
        'client_spending': '5000',
        'client_rating': '4.0',
        'posted_time_seconds': '86400',  # 1 day ago
        'budget': '1500',
        'hourly_rate': '25',
    }
    
    print("   Column mapping:")
    for our_field, their_field in mapping.items():
        print(f"      {our_field:20s} ← {their_field}")
    
    # Step 5: Import with auto-labeling
    print("\n🤖 Step 5: Importing and auto-labeling jobs...")
    print("   (This may take a minute for large datasets)")
    
    # Limit to first 500 jobs for quick testing
    # Remove this limit to import all jobs
    try:
        adapter.import_generic_job_dataset(csv_file, mapping, defaults)
    except Exception as e:
        print(f"❌ Import failed: {e}")
        print("\nTry adjusting the column mapping based on the preview above.")
        return
    
    # Step 6: Show statistics
    print("\n📊 Step 6: Import statistics...")
    adapter.print_statistics()
    
    # Step 7: Export to our format
    print("\n💾 Step 7: Exporting to our CSV format...")
    output_file = Path(__file__).parent / "data" / "kaggle_imported_jobs.csv"
    adapter.export_to_csv(output_file)
    
    # Also save JSON backup
    import json
    json_file = Path(__file__).parent / "data" / "kaggle_imported_jobs.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(adapter.imported_jobs, f, indent=2)
    print(f"   JSON backup: {json_file}")
    
    # Step 8: Next steps
    print("\n" + "="*80)
    print("✅ IMPORT COMPLETE!")
    print("="*80)
    print(f"\n📁 Output files:")
    print(f"   • {output_file}")
    print(f"   • {json_file}")
    
    print(f"\n📈 Imported: {len(adapter.imported_jobs)} jobs")
    
    print("\n🔍 NEXT STEPS:")
    print("   1. Review the imported data:")
    print("      python collect_data.py  (then choose 'stats')")
    print()
    print("   2. Fix incorrect labels:")
    print("      • Open data/kaggle_imported_jobs.csv in Excel/VS Code")
    print("      • Review 'quality_label' column")
    print("      • Manually fix obvious errors")
    print()
    print("   3. Merge with manual labels (optional):")
    print("      • Label additional edge cases manually")
    print("      • Combine both datasets")
    print()
    print("   4. Start training (Phase 3):")
    print("      • Once you have 200+ labeled jobs")
    print("      • Train spam detector model")
    print()
    print("⚠️  Remember: Auto-labels are approximate (~70% accuracy)")
    print("   Manual review will significantly improve model quality!")


if __name__ == "__main__":
    main()

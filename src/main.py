"""
Main application file for CrediGlobe project.
Orchestrates the complete data analysis pipeline for World Bank IDS dataset.
"""

from data_loader import DataLoader
from data_cleaner import DataCleaner
from database import DebtDatabase
from visualizer import DebtVisualizer
import sys


def main():
    """Main execution function for the CrediGlobe analysis."""
    
    print("=" * 60)
    print("CrediGlobe - Global Debt Analysis & Financial Insights")
    print("Making Sense of Global Debt Through Data")
    print("=" * 60)
    print()
    
    # Step 1: Check if dataset is ready
    print("Step 1: Checking dataset availability...")
    loader = DataLoader(data_dir="../data/raw")
    readiness = loader.check_dataset_readiness()
    
    if not readiness["ready"]:
        print("\n⚠️  Dataset Not Found!")
        print(f"Message: {readiness['message']}")
        print("\nInstructions:")
        for instruction in readiness["instructions"]:
            print(f"  - {instruction}")
        print("\n" + "=" * 60)
        print("Please add the World Bank IDS dataset files and run this script again.")
        print("=" * 60)
        return
    
    print(f"✓ {readiness['message']}")
    print("\nDataset files found:")
    for filename, status in readiness['files_status'].items():
        print(f"  ✓ {filename}")
    print()
    
    # Step 2: Load primary data file
    print("Step 2: Loading primary data (IDSData.csv)...")
    success, message = loader.load_primary_data()
    if not success:
        print(f"✗ {message}")
        return
    
    print(f"✓ {message}")
    df = loader.get_primary_data()
    
    # Display basic info about the primary data
    info = loader.get_basic_info('data')
    print(f"\nPrimary Data Info:")
    print(f"  Rows: {info['rows']}")
    print(f"  Columns: {info['columns']}")
    print(f"  Column Names: {', '.join(info['column_names'][:5])}{'...' if len(info['column_names']) > 5 else ''}")
    
    print("\nSample Data (first 3 rows):")
    print(df.head(3))
    print()
    
    # Step 2b: Load metadata files (optional but helpful)
    print("Step 2b: Loading metadata files...")
    load_results = loader.load_all_files()
    
    metadata_loaded = sum(1 for success, _ in load_results.values() if success)
    print(f"✓ Successfully loaded {metadata_loaded}/{len(load_results)} dataset files")
    print()
    
    # Step 3: Clean the data
    print("Step 3: Cleaning data...")
    cleaner = DataCleaner(df)
    
    # Remove duplicates
    cleaner.remove_duplicates()
    
    # Handle missing values (strategy can be adjusted based on actual data)
    cleaner.handle_missing_values(strategy="drop")
    
    # Get cleaned data
    df_clean = cleaner.get_cleaned_data()
    summary = cleaner.get_cleaning_summary()
    
    print(f"✓ Data cleaning complete")
    print(f"  Original shape: {summary['original_shape']}")
    print(f"  Cleaned shape: {summary['cleaned_shape']}")
    print(f"  Rows removed: {summary['rows_removed']}")
    for operation in summary['cleaning_operations']:
        print(f"  - {operation}")
    print()
    
    # Step 4: Store data in database
    print("Step 4: Setting up database...")
    db = DebtDatabase(db_path="../data/crediglobe.db")
    
    if not db.connect():
        print("✗ Failed to connect to database")
        return
    
    print("✓ Connected to database")
    
    # Note: Column names will be determined from actual data
    # Database table structure will adapt to the actual columns in IDSData.csv
    if not db.create_debt_table():
        print("✗ Failed to create table")
        return
    
    print("✓ Table created")
    
    success, message = db.insert_data_from_dataframe(df_clean, table_name="ids_data")
    print(f"✓ {message}")
    print()
    
    # Step 5: Perform SQL analysis (column names will be detected from actual data)
    print("Step 5: Running SQL analysis...")
    print("Note: Analysis queries will be based on actual column names in the dataset")
    
    # These queries will need to be adapted once we know the actual column structure
    # For now, skip specific queries until dataset is inspected
    print("✓ Database ready for custom queries")
    print()
    
    # Step 6: Create visualizations
    print("Step 6: Visualization preparation...")
    viz = DebtVisualizer(output_dir="../visualizations")
    print("✓ Visualizer ready (visualizations will be created after data inspection)")
    print()
    
    # Close database connection
    db.close()
    
    print("=" * 60)
    print("Initial Analysis Complete!")
    print()
    print("Next Steps:")
    print("1. Inspect the actual column names in IDSData.csv")
    print("2. Customize SQL queries based on actual schema")
    print("3. Create visualizations based on actual data structure")
    print("4. Check 'data/crediglobe.db' for the populated database")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ An error occurred: {str(e)}")
        sys.exit(1)

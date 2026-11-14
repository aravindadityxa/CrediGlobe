"""
Dataset inspection script for World Bank IDS files.
Examines all CSV files without modifying them.
"""

import pandas as pd
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import DataLoader

def inspect_file(filepath, file_description):
    """Inspect a single CSV file and display comprehensive information."""
    print("=" * 80)
    print(f"FILE: {os.path.basename(filepath)}")
    print(f"Description: {file_description}")
    print("=" * 80)
    
    try:
        # Load the file
        df = pd.read_csv(filepath)
        
        # Basic info
        print(f"\n📊 BASIC INFORMATION:")
        print(f"  Rows: {len(df):,}")
        print(f"  Columns: {len(df.columns)}")
        print(f"  File size: {os.path.getsize(filepath):,} bytes")
        print(f"  Memory usage: {df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB")
        
        # Column names
        print(f"\n📋 COLUMN NAMES:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        # Data types
        print(f"\n🔤 DATA TYPES:")
        for col, dtype in df.dtypes.items():
            print(f"  {col}: {dtype}")
        
        # Missing values
        print(f"\n❓ MISSING VALUES:")
        missing = df.isnull().sum()
        total_rows = len(df)
        for col in df.columns:
            miss_count = missing[col]
            miss_pct = (miss_count / total_rows) * 100
            if miss_count > 0:
                print(f"  {col}: {miss_count:,} ({miss_pct:.2f}%)")
            else:
                print(f"  {col}: 0 (0.00%)")
        
        # Duplicates
        print(f"\n🔍 DUPLICATE RECORDS:")
        dup_count = df.duplicated().sum()
        print(f"  Duplicate rows: {dup_count:,} ({(dup_count/total_rows)*100:.2f}%)")
        
        # Sample data
        print(f"\n📄 FIRST 5 RECORDS:")
        print(df.head(5).to_string())
        
        # Additional statistics for numeric columns
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        if numeric_cols:
            print(f"\n📈 NUMERIC COLUMN STATISTICS:")
            print(df[numeric_cols].describe().to_string())
        
        # Categorical columns summary
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        if categorical_cols:
            print(f"\n📊 CATEGORICAL COLUMN UNIQUE VALUES:")
            for col in categorical_cols[:5]:  # Show first 5 categorical columns
                unique_count = df[col].nunique()
                print(f"  {col}: {unique_count:,} unique values")
                if unique_count <= 10:
                    print(f"    Values: {df[col].unique().tolist()}")
        
        print("\n")
        return df
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None


def main():
    """Main inspection routine."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "WORLD BANK IDS DATASET INSPECTION" + " " * 25 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")
    
    data_dir = "data/raw"
    
    # Define files and descriptions
    files_info = {
        'IDSData.csv': 'Primary debt statistics data',
        'IDSCountry.csv': 'Country metadata and information',
        'IDSCountry-Series.csv': 'Country-Series relationship mapping',
        'IDSSeries.csv': 'Series (indicator) metadata and descriptions',
        'IDSFootNote.csv': 'Footnotes and additional notes',
        'IDSSeries-Time.csv': 'Time-series specific metadata'
    }
    
    datasets = {}
    
    # Inspect each file
    for filename, description in files_info.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            df = inspect_file(filepath, description)
            if df is not None:
                datasets[filename] = df
        else:
            print(f"⚠️  File not found: {filepath}")
        
        input("\nPress Enter to continue to next file...")
        print("\n\n")
    
    # RELATIONSHIP ANALYSIS
    print("=" * 80)
    print("RELATIONSHIP ANALYSIS")
    print("=" * 80)
    print("\n")
    
    if 'IDSData.csv' in datasets and 'IDSCountry.csv' in datasets:
        print("🔗 RELATIONSHIP: IDSData.csv ↔ IDSCountry.csv")
        data_df = datasets['IDSData.csv']
        country_df = datasets['IDSCountry.csv']
        
        # Find common columns
        common_cols = set(data_df.columns).intersection(set(country_df.columns))
        print(f"  Common columns: {list(common_cols)}")
        
        if common_cols:
            for col in common_cols:
                data_unique = data_df[col].nunique()
                country_unique = country_df[col].nunique()
                print(f"    {col}: {data_unique} in IDSData, {country_unique} in IDSCountry")
        print()
    
    if 'IDSData.csv' in datasets and 'IDSSeries.csv' in datasets:
        print("🔗 RELATIONSHIP: IDSData.csv ↔ IDSSeries.csv")
        data_df = datasets['IDSData.csv']
        series_df = datasets['IDSSeries.csv']
        
        common_cols = set(data_df.columns).intersection(set(series_df.columns))
        print(f"  Common columns: {list(common_cols)}")
        
        if common_cols:
            for col in common_cols:
                data_unique = data_df[col].nunique()
                series_unique = series_df[col].nunique()
                print(f"    {col}: {data_unique} in IDSData, {series_unique} in IDSSeries")
        print()
    
    # SUMMARY
    print("\n")
    print("=" * 80)
    print("SUMMARY OF ALL FILES")
    print("=" * 80)
    print()
    
    for filename, df in datasets.items():
        print(f"📁 {filename}")
        print(f"   Rows: {len(df):,} | Columns: {len(df.columns)} | Missing: {df.isnull().sum().sum():,}")
        print()
    
    print("=" * 80)
    print("INSPECTION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()

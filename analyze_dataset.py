"""
Comprehensive dataset analysis for World Bank IDS files.
Examines all CSV files and their relationships.
"""

import pandas as pd
import os

def analyze_csv(filepath, description):
    """Analyze a single CSV file."""
    print("\n" + "=" * 80)
    print(f"FILE: {os.path.basename(filepath)}")
    print(f"Description: {description}")
    print("=" * 80)
    
    try:
        df = pd.read_csv(filepath)
        
        # Basic info
        print(f"\nBASIC INFORMATION:")
        print(f"  Total Rows: {len(df):,}")
        print(f"  Total Columns: {len(df.columns)}")
        file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"  File Size: {file_size_mb:.2f} MB")
        print(f"  Memory Usage: {df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB")
        
        # Column names
        print(f"\nCOLUMN NAMES ({len(df.columns)} total):")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        # Data types
        print(f"\nDATA TYPES:")
        dtype_counts = df.dtypes.value_counts()
        for dtype, count in dtype_counts.items():
            print(f"  {dtype}: {count} columns")
        
        # Missing values
        print(f"\nMISSING VALUES:")
        missing = df.isnull().sum()
        total_rows = len(df)
        total_missing = missing.sum()
        print(f"  Total missing values: {total_missing:,}")
        
        if total_missing > 0:
            print(f"  Columns with missing values:")
            for col in df.columns:
                miss_count = missing[col]
                if miss_count > 0:
                    miss_pct = (miss_count / total_rows) * 100
                    print(f"    {col}: {miss_count:,} ({miss_pct:.1f}%)")
        else:
            print(f"  No missing values found!")
        
        # Duplicates
        print(f"\nDUPLICATE RECORDS:")
        dup_count = df.duplicated().sum()
        dup_pct = (dup_count / total_rows) * 100
        print(f"  Duplicate rows: {dup_count:,} ({dup_pct:.2f}%)")
        
        # Sample data
        print(f"\nFIRST 5 RECORDS:")
        print(df.head(5).to_string(index=False, max_colwidth=50))
        
        # Unique values for key columns
        if len(df.columns) <= 10:  # For smaller files
            print(f"\nUNIQUE VALUE COUNTS:")
            for col in df.columns:
                unique_count = df[col].nunique()
                non_null_count = df[col].count()
                print(f"  {col}: {unique_count:,} unique ({non_null_count:,} non-null)")
        
        return df
        
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def main():
    print("\n" + "=" * 80)
    print("  WORLD BANK INTERNATIONAL DEBT STATISTICS - DATASET INSPECTION  ")
    print("=" * 80)
    
    data_dir = "data/raw"
    
    files_info = [
        ('IDSData.csv', 'Primary debt statistics (main data)'),
        ('IDSCountry.csv', 'Country metadata'),
        ('IDSSeries.csv', 'Series/Indicator metadata'),
        ('IDSCountry-Series.csv', 'Country-Series relationships'),
        ('IDSFootNote.csv', 'Footnotes and notes'),
        ('IDSSeries-Time.csv', 'Time-series metadata')
    ]
    
    datasets = {}
    
    # Analyze each file
    for filename, description in files_info:
        filepath = os.path.join(data_dir, filename)
        df = analyze_csv(filepath, description)
        if df is not None:
            datasets[filename] = df
    
    # RELATIONSHIP ANALYSIS
    print("\n\n" + "=" * 80)
    print("RELATIONSHIP ANALYSIS")
    print("=" * 80)
    
    if 'IDSData.csv' in datasets:
        data_df = datasets['IDSData.csv']
        print(f"\nPRIMARY DATASET: IDSData.csv")
        print(f"  Structure: WIDE format (years as columns)")
        print(f"  Unique Countries: {data_df['Country Code'].nunique():,}")
        print(f"  Unique Indicators: {data_df['Indicator Code'].nunique():,}")
        
        # Year columns
        year_cols = [col for col in data_df.columns if col not in ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']]
        print(f"  Year Range: {year_cols[0]} to {year_cols[-1]}")
        print(f"  Total Year Columns: {len(year_cols)}")
    
    if 'IDSCountry.csv' in datasets:
        country_df = datasets['IDSCountry.csv']
        print(f"\nRELATIONSHIP: IDSData.csv <-> IDSCountry.csv")
        print(f"  Join Key: 'Country Code'")
        print(f"  Countries in IDSData: {data_df['Country Code'].nunique():,}")
        print(f"  Countries in IDSCountry: {country_df['Country Code'].nunique():,}")
        
        # Check overlap
        data_countries = set(data_df['Country Code'].unique())
        meta_countries = set(country_df['Country Code'].unique())
        common = data_countries.intersection(meta_countries)
        print(f"  Common Countries: {len(common):,}")
        print(f"  Countries only in Data: {len(data_countries - meta_countries)}")
        print(f"  Countries only in Metadata: {len(meta_countries - data_countries)}")
    
    if 'IDSSeries.csv' in datasets:
        series_df = datasets['IDSSeries.csv']
        print(f"\nRELATIONSHIP: IDSData.csv <-> IDSSeries.csv")
        print(f"  Join Key: 'Indicator Code' (Data) -> 'Series Code' (Series)")
        print(f"  Indicators in IDSData: {data_df['Indicator Code'].nunique():,}")
        print(f"  Series in IDSSeries: {series_df['Series Code'].nunique():,}")
        
        # Check overlap
        data_indicators = set(data_df['Indicator Code'].unique())
        meta_series = set(series_df['Series Code'].unique())
        common = data_indicators.intersection(meta_series)
        print(f"  Common Indicators: {len(common):,}")
        print(f"  Indicators only in Data: {len(data_indicators - meta_series)}")
        print(f"  Series only in Metadata: {len(meta_series - data_indicators)}")
    
    if 'IDSCountry-Series.csv' in datasets:
        cs_df = datasets['IDSCountry-Series.csv']
        print(f"\nRELATIONSHIP: IDSCountry-Series.csv")
        print(f"  Purpose: Links countries to specific series with notes")
        print(f"  Total Mappings: {len(cs_df):,}")
        print(f"  Unique Countries: {cs_df['CountryCode'].nunique():,}")
        print(f"  Unique Series: {cs_df['SeriesCode'].nunique():,}")
    
    if 'IDSFootNote.csv' in datasets:
        fn_df = datasets['IDSFootNote.csv']
        print(f"\nRELATIONSHIP: IDSFootNote.csv")
        print(f"  Purpose: Footnotes for specific country-series-year combinations")
        print(f"  Total Footnotes: {len(fn_df):,}")
        print(f"  Unique Countries: {fn_df['CountryCode'].nunique():,}")
        print(f"  Unique Series: {fn_df['SeriesCode'].nunique():,}")
    
    if 'IDSSeries-Time.csv' in datasets:
        st_df = datasets['IDSSeries-Time.csv']
        print(f"\nRELATIONSHIP: IDSSeries-Time.csv")
        print(f"  Purpose: Time-specific notes for series")
        print(f"  Total Entries: {len(st_df):,}")
    
    # DATA QUALITY OBSERVATIONS
    print("\n\n" + "=" * 80)
    print("DATA QUALITY OBSERVATIONS")
    print("=" * 80)
    
    if 'IDSData.csv' in datasets:
        print("\nIDSData.csv (Primary Dataset):")
        
        # Check year columns for missing data
        year_cols = [col for col in data_df.columns if col not in ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']]
        total_year_cells = len(data_df) * len(year_cols)
        missing_year_data = data_df[year_cols].isnull().sum().sum()
        missing_pct = (missing_year_data / total_year_cells) * 100
        
        print(f"  Missing data in year columns: {missing_year_data:,} / {total_year_cells:,} ({missing_pct:.1f}%)")
        print(f"  Country Name: {data_df['Country Name'].isnull().sum()} missing")
        print(f"  Country Code: {data_df['Country Code'].isnull().sum()} missing")
        print(f"  Indicator Name: {data_df['Indicator Name'].isnull().sum()} missing")
        print(f"  Indicator Code: {data_df['Indicator Code'].isnull().sum()} missing")
        
        # Sample some indicators
        print(f"\n  Sample Indicator Types:")
        sample_indicators = data_df['Indicator Name'].head(10).tolist()
        for i, ind in enumerate(sample_indicators[:5], 1):
            print(f"    {i}. {ind[:70]}...")
    
    # SUMMARY
    print("\n\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    print("\nFILES SUMMARY:")
    for filename, df in datasets.items():
        size_mb = os.path.getsize(os.path.join(data_dir, filename)) / (1024 * 1024)
        missing = df.isnull().sum().sum()
        print(f"  {filename}")
        print(f"    Rows: {len(df):,} | Columns: {len(df.columns)} | Missing: {missing:,} | Size: {size_mb:.2f} MB")
    
    print("\nKEY FINDINGS:")
    print("  1. IDSData.csv is in WIDE format (years as columns)")
    print("  2. Primary keys: Country Code + Indicator Code")
    print("  3. Metadata files provide additional context")
    print("  4. Significant missing data in year columns (normal for this type of dataset)")
    print("  5. Files can be joined using Country Code and Indicator/Series Code")
    
    print("\nRECOMMENDED COLUMNS FOR ANALYSIS:")
    print("  From IDSData.csv:")
    print("    - Country Code (for joining)")
    print("    - Country Name (for display)")
    print("    - Indicator Code (for grouping)")
    print("    - Indicator Name (for understanding)")
    print("    - Year columns (1970-2024) for actual debt values")
    
    print("\nPOTENTIAL ISSUES TO ADDRESS:")
    print("  1. WIDE format needs transformation to LONG format for analysis")
    print("  2. High percentage of missing values in year columns")
    print("  3. Empty string values may exist (need conversion to NaN)")
    print("  4. Data types of year columns need verification")
    
    print("\n" + "=" * 80)
    print("INSPECTION COMPLETE")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()

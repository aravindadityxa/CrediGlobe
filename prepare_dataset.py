"""
World Bank IDS Dataset Preparation Script

This script transforms the raw World Bank International Debt Statistics dataset
from WIDE format to LONG format and enriches it with metadata.

IMPORTANT: Original files in data/raw/ are NEVER modified.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def load_raw_data():
    """Load all raw CSV files without modification."""
    print_section("STEP 1: LOADING RAW DATA")
    
    data_dir = "data/raw"
    
    print("\nLoading IDSData.csv...")
    df_data = pd.read_csv(os.path.join(data_dir, "IDSData.csv"))
    print(f"  Loaded: {len(df_data):,} rows, {len(df_data.columns)} columns")
    
    print("\nLoading IDSCountry.csv...")
    df_country = pd.read_csv(os.path.join(data_dir, "IDSCountry.csv"))
    print(f"  Loaded: {len(df_country):,} rows, {len(df_country.columns)} columns")
    
    print("\nLoading IDSSeries.csv...")
    df_series = pd.read_csv(os.path.join(data_dir, "IDSSeries.csv"))
    print(f"  Loaded: {len(df_series):,} rows, {len(df_series.columns)} columns")
    
    print("\n[OK] All raw files loaded successfully")
    print("[OK] Original files remain unmodified in data/raw/")
    
    return df_data, df_country, df_series


def identify_columns(df_data):
    """Identify metadata columns and year columns dynamically."""
    print_section("STEP 2: IDENTIFYING COLUMN STRUCTURE")
    
    # Metadata columns (known structure)
    metadata_cols = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
    
    # Year columns are everything else except unnamed columns
    all_cols = df_data.columns.tolist()
    year_cols = [col for col in all_cols 
                 if col not in metadata_cols 
                 and not col.startswith('Unnamed')]
    
    # Identify empty/unnamed columns
    unnamed_cols = [col for col in all_cols if col.startswith('Unnamed')]
    
    print(f"\nMetadata columns: {len(metadata_cols)}")
    for col in metadata_cols:
        print(f"  - {col}")
    
    print(f"\nYear columns: {len(year_cols)}")
    print(f"  Range: {year_cols[0]} to {year_cols[-1]}")
    print(f"  Total: {len(year_cols)} years")
    
    print(f"\nEmpty/Unnamed columns: {len(unnamed_cols)}")
    for col in unnamed_cols:
        print(f"  - {col} (will be removed)")
    
    return metadata_cols, year_cols, unnamed_cols


def clean_empty_columns(df, unnamed_cols):
    """Remove empty/unnamed columns."""
    print_section("STEP 3: REMOVING EMPTY COLUMNS")
    
    original_cols = len(df.columns)
    df_clean = df.drop(columns=unnamed_cols, errors='ignore')
    removed = original_cols - len(df_clean.columns)
    
    print(f"\nOriginal columns: {original_cols}")
    print(f"Removed columns: {removed}")
    print(f"Remaining columns: {len(df_clean.columns)}")
    
    return df_clean


def transform_wide_to_long(df_data, metadata_cols, year_cols):
    """Transform data from WIDE format to LONG format."""
    print_section("STEP 4: TRANSFORMING WIDE FORMAT TO LONG FORMAT")
    
    print(f"\nBefore transformation:")
    print(f"  Shape: {df_data.shape}")
    print(f"  Format: WIDE (years as columns)")
    
    # Use pd.melt to transform
    print(f"\nTransforming...")
    df_long = pd.melt(
        df_data,
        id_vars=metadata_cols,
        value_vars=year_cols,
        var_name='Year',
        value_name='Value'
    )
    
    print(f"\nAfter transformation:")
    print(f"  Shape: {df_long.shape}")
    print(f"  Format: LONG (one row per country-indicator-year)")
    
    # Show sample
    print(f"\nSample of transformed data:")
    print(df_long.head(10).to_string(index=False))
    
    return df_long


def convert_data_types(df_long):
    """Convert Year and Value to appropriate data types."""
    print_section("STEP 5: CONVERTING DATA TYPES")
    
    print("\nBefore conversion:")
    print(f"  Year: {df_long['Year'].dtype}")
    print(f"  Value: {df_long['Value'].dtype}")
    
    # Convert Year to integer
    df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce').astype('Int64')
    
    # Value is already float64 (correct for handling NaN)
    # Ensure it's float64
    df_long['Value'] = pd.to_numeric(df_long['Value'], errors='coerce')
    
    print("\nAfter conversion:")
    print(f"  Year: {df_long['Year'].dtype}")
    print(f"  Value: {df_long['Value'].dtype}")
    
    return df_long


def analyze_missing_values(df_long):
    """Analyze missing values without removing data."""
    print_section("STEP 6: ANALYZING MISSING VALUES")
    
    total_rows = len(df_long)
    
    print(f"\nTotal rows: {total_rows:,}")
    print(f"\nMissing value analysis:")
    
    for col in df_long.columns:
        missing_count = df_long[col].isnull().sum()
        missing_pct = (missing_count / total_rows) * 100
        print(f"  {col}: {missing_count:,} ({missing_pct:.2f}%)")
    
    # Analyze missing values by year
    print(f"\nMissing values by year range:")
    df_long_copy = df_long.copy()
    df_long_copy['Year_Range'] = pd.cut(
        df_long_copy['Year'], 
        bins=[1969, 1990, 2000, 2016, 2024],
        labels=['1970-1990', '1991-2000', '2001-2016', '2017-2024']
    )
    
    year_missing = df_long_copy.groupby('Year_Range')['Value'].apply(
        lambda x: (x.isnull().sum(), len(x), (x.isnull().sum()/len(x))*100)
    )
    
    for year_range, (missing, total, pct) in year_missing.items():
        print(f"  {year_range}: {missing:,}/{total:,} ({pct:.1f}% missing)")
    
    print(f"\n[NOTE] NOTE: Missing values are PRESERVED (not removed)")
    print(f"    Missing values represent data not yet available or not applicable")
    print(f"    They will be handled appropriately during analysis")
    
    return df_long


def enrich_with_country_metadata(df_long, df_country):
    """Join with country metadata."""
    print_section("STEP 7: ENRICHING WITH COUNTRY METADATA")
    
    # Clean unnamed columns from country data
    df_country_clean = df_country.loc[:, ~df_country.columns.str.startswith('Unnamed')]
    
    # Select key metadata columns
    country_cols = ['Country Code', 'Region', 'Income Group', 'Currency Unit', 'Lending category']
    df_country_subset = df_country_clean[country_cols].copy()
    
    print(f"\nCountry metadata columns to add:")
    for col in country_cols[1:]:  # Skip Country Code (join key)
        print(f"  - {col}")
    
    print(f"\nBefore join:")
    print(f"  Rows: {len(df_long):,}")
    print(f"  Columns: {len(df_long.columns)}")
    
    # Perform left join
    df_enriched = df_long.merge(
        df_country_subset,
        on='Country Code',
        how='left'
    )
    
    print(f"\nAfter join:")
    print(f"  Rows: {len(df_enriched):,}")
    print(f"  Columns: {len(df_enriched.columns)}")
    
    # Check for unmatched countries
    unmatched = df_enriched['Region'].isnull().sum()
    if unmatched > 0:
        print(f"\n[WARNING] Warning: {unmatched:,} rows with no country metadata match")
    else:
        print(f"\n[OK] All countries matched successfully")
    
    return df_enriched


def enrich_with_indicator_metadata(df_enriched, df_series):
    """Join with indicator/series metadata."""
    print_section("STEP 8: ENRICHING WITH INDICATOR METADATA")
    
    # Clean unnamed columns from series data
    df_series_clean = df_series.loc[:, ~df_series.columns.str.startswith('Unnamed')]
    
    # Select key metadata columns
    # Note: IDSSeries uses 'Series Code' which matches 'Indicator Code' in data
    series_cols = ['Series Code', 'Topic', 'Short definition', 'Source']
    df_series_subset = df_series_clean[series_cols].copy()
    
    print(f"\nIndicator metadata columns to add:")
    for col in series_cols[1:]:  # Skip Series Code (join key)
        print(f"  - {col}")
    
    print(f"\nBefore join:")
    print(f"  Rows: {len(df_enriched):,}")
    print(f"  Columns: {len(df_enriched.columns)}")
    
    # Perform left join (Indicator Code = Series Code)
    df_final = df_enriched.merge(
        df_series_subset,
        left_on='Indicator Code',
        right_on='Series Code',
        how='left'
    )
    
    # Drop duplicate Series Code column (we already have Indicator Code)
    df_final = df_final.drop(columns=['Series Code'])
    
    print(f"\nAfter join:")
    print(f"  Rows: {len(df_final):,}")
    print(f"  Columns: {len(df_final.columns)}")
    
    # Check for unmatched indicators
    unmatched = df_final['Topic'].isnull().sum()
    if unmatched > 0:
        print(f"\n⚠️  Warning: {unmatched:,} rows with no indicator metadata match")
    else:
        print(f"\n[OK] All indicators matched successfully")
    
    return df_final


def check_for_duplicates(df_final):
    """Check for unexpected duplicate records."""
    print_section("STEP 9: CHECKING FOR DUPLICATES")
    
    # Define what makes a unique record
    key_cols = ['Country Code', 'Indicator Code', 'Year']
    
    print(f"\nChecking for duplicates based on:")
    for col in key_cols:
        print(f"  - {col}")
    
    # Check for duplicates
    duplicates = df_final.duplicated(subset=key_cols, keep=False)
    dup_count = duplicates.sum()
    
    if dup_count > 0:
        print(f"\n[WARNING] Found {dup_count:,} duplicate records!")
        print(f"\nSample duplicates:")
        print(df_final[duplicates][key_cols + ['Value']].head(10).to_string(index=False))
        
        # Remove duplicates, keeping first occurrence
        df_final = df_final.drop_duplicates(subset=key_cols, keep='first')
        print(f"\n[OK] Removed duplicates, kept first occurrence")
        print(f"  Rows after deduplication: {len(df_final):,}")
    else:
        print(f"\n[OK] No duplicate records found")
    
    return df_final


def generate_summary(df_original, df_final):
    """Generate comprehensive cleaning summary."""
    print_section("STEP 10: CLEANING SUMMARY")
    
    print(f"\n{'='*40}")
    print("TRANSFORMATION SUMMARY")
    print(f"{'='*40}")
    
    print(f"\n[DATA] ORIGINAL DATA (WIDE FORMAT):")
    print(f"  Shape: {df_original.shape}")
    print(f"  Format: {df_original.shape[0]:,} rows × {df_original.shape[1]} columns")
    print(f"  Structure: {df_original.shape[0]:,} country-indicator combinations")
    
    print(f"\n[DATA] TRANSFORMED DATA (LONG FORMAT):")
    print(f"  Shape: {df_final.shape}")
    print(f"  Format: {len(df_final):,} rows × {len(df_final.columns)} columns")
    print(f"  Structure: One row per country-indicator-year")
    
    print(f"\n[CALC] ROW CALCULATION:")
    original_metadata_cols = 4
    original_year_cols = df_original.shape[1] - original_metadata_cols - 1  # -1 for unnamed
    expected_rows = df_original.shape[0] * original_year_cols
    print(f"  Expected: {df_original.shape[0]:,} combinations × {original_year_cols} years = {expected_rows:,} rows")
    print(f"  Actual: {len(df_final):,} rows")
    print(f"  Match: {'[OK] Yes' if len(df_final) == expected_rows else '[X] No'}")
    
    print(f"\n[COLS] COLUMNS ADDED:")
    original_cols = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code', 'Year', 'Value']
    new_cols = [col for col in df_final.columns if col not in original_cols]
    print(f"  Total new columns: {len(new_cols)}")
    for col in new_cols:
        print(f"    - {col}")
    
    print(f"\n[MISSING] MISSING VALUES:")
    total_cells = len(df_final) * len(df_final.columns)
    total_missing = df_final.isnull().sum().sum()
    missing_pct = (total_missing / total_cells) * 100
    print(f"  Total: {total_missing:,} / {total_cells:,} ({missing_pct:.2f}%)")
    print(f"  Primary data (Value column): {df_final['Value'].isnull().sum():,} ({(df_final['Value'].isnull().sum()/len(df_final))*100:.2f}%)")
    
    print(f"\n[TYPES] DATA TYPES:")
    for col in df_final.columns:
        dtype = df_final[col].dtype
        print(f"  {col}: {dtype}")
    
    print(f"\n[YEARS] YEAR COVERAGE:")
    print(f"  Min year: {df_final['Year'].min()}")
    print(f"  Max year: {df_final['Year'].max()}")
    print(f"  Total years: {df_final['Year'].nunique()}")
    
    print(f"\n[GEO] GEOGRAPHIC COVERAGE:")
    print(f"  Countries: {df_final['Country Code'].nunique()}")
    print(f"  Regions: {df_final['Region'].nunique()}")
    
    print(f"\n[INDICATORS] INDICATOR COVERAGE:")
    print(f"  Unique indicators: {df_final['Indicator Code'].nunique()}")
    print(f"  Topics: {df_final['Topic'].nunique()}")
    
    print(f"\n[MEMORY] MEMORY USAGE:")
    memory_mb = df_final.memory_usage(deep=True).sum() / (1024 * 1024)
    print(f"  Total: {memory_mb:.2f} MB")


def save_processed_data(df_final):
    """Save the processed dataset."""
    print_section("STEP 11: SAVING PROCESSED DATA")
    
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "ids_data_long.csv")
    
    print(f"\nSaving to: {output_file}")
    df_final.to_csv(output_file, index=False)
    
    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"[OK] Saved successfully")
    print(f"  File size: {file_size_mb:.2f} MB")
    print(f"  Rows: {len(df_final):,}")
    print(f"  Columns: {len(df_final.columns)}")
    
    return output_file


def verify_processed_data(output_file):
    """Verify the processed data can be loaded correctly."""
    print_section("STEP 12: VERIFICATION")
    
    print(f"\nReloading saved file to verify...")
    df_verify = pd.read_csv(output_file)
    
    print(f"[OK] File loads successfully")
    print(f"  Shape: {df_verify.shape}")
    
    print(f"\n[OK] Sample of processed data:")
    print(df_verify.head(10).to_string(index=False, max_colwidth=50))
    
    print(f"\n[OK] Data types preserved:")
    for col in ['Year', 'Value', 'Country Code', 'Indicator Code']:
        print(f"  {col}: {df_verify[col].dtype}")
    
    return df_verify


def main():
    """Main execution function."""
    print("\n")
    print("=" * 80)
    print(" WORLD BANK IDS DATASET PREPARATION ".center(80))
    print(" Transforming WIDE format to LONG format ".center(80))
    print("=" * 80)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Load raw data
    df_data, df_country, df_series = load_raw_data()
    df_original = df_data.copy()  # Keep original for comparison
    
    # Step 2: Identify columns
    metadata_cols, year_cols, unnamed_cols = identify_columns(df_data)
    
    # Step 3: Clean empty columns
    df_data = clean_empty_columns(df_data, unnamed_cols)
    
    # Step 4: Transform to long format
    df_long = transform_wide_to_long(df_data, metadata_cols, year_cols)
    
    # Step 5: Convert data types
    df_long = convert_data_types(df_long)
    
    # Step 6: Analyze missing values (no removal)
    df_long = analyze_missing_values(df_long)
    
    # Step 7: Enrich with country metadata
    df_enriched = enrich_with_country_metadata(df_long, df_country)
    
    # Step 8: Enrich with indicator metadata
    df_final = enrich_with_indicator_metadata(df_enriched, df_series)
    
    # Step 9: Check for duplicates
    df_final = check_for_duplicates(df_final)
    
    # Step 10: Generate summary
    generate_summary(df_original, df_final)
    
    # Step 11: Save processed data
    output_file = save_processed_data(df_final)
    
    # Step 12: Verify
    df_verify = verify_processed_data(output_file)
    
    # Final message
    print("\n" + "=" * 80)
    print("[OK] DATASET PREPARATION COMPLETE")
    print("=" * 80)
    print(f"\n[OK] Original files preserved in: data/raw/")
    print(f"[OK] Processed data saved to: {output_file}")
    print(f"[OK] Ready for exploratory data analysis")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()

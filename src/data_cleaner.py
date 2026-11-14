"""
Data cleaning and preprocessing utilities for CrediGlobe project.
Handles missing values, duplicates, data type conversions, and outliers.
"""

import pandas as pd
import numpy as np
from typing import Optional, List


class DataCleaner:
    """Handles data cleaning and preprocessing operations."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the DataCleaner with a DataFrame.
        
        Args:
            df: pandas DataFrame to clean
        """
        self.df = df.copy()
        self.original_shape = df.shape
        self.cleaning_log = []
    
    def handle_missing_values(self, strategy: str = "drop", threshold: float = 0.5) -> pd.DataFrame:
        """
        Handle missing values in the dataset.
        
        Args:
            strategy: 'drop' to remove rows with missing values,
                     'fill_median' for numerical columns,
                     'fill_mode' for categorical columns
            threshold: If strategy is 'drop', only drop columns with missing % > threshold
            
        Returns:
            Cleaned DataFrame
        """
        missing_before = self.df.isnull().sum().sum()
        
        if strategy == "drop":
            # Drop rows with any missing values
            self.df = self.df.dropna()
            self.cleaning_log.append(f"Dropped rows with missing values: {missing_before} missing values removed")
        
        elif strategy == "fill_median":
            # Fill numeric columns with median
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if self.df[col].isnull().any():
                    median_val = self.df[col].median()
                    self.df[col].fillna(median_val, inplace=True)
            self.cleaning_log.append(f"Filled numeric missing values with median")
        
        elif strategy == "fill_mode":
            # Fill categorical columns with mode
            categorical_cols = self.df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                if self.df[col].isnull().any():
                    mode_val = self.df[col].mode()[0] if not self.df[col].mode().empty else "Unknown"
                    self.df[col].fillna(mode_val, inplace=True)
            self.cleaning_log.append(f"Filled categorical missing values with mode")
        
        return self.df
    
    def remove_duplicates(self, subset: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Remove duplicate rows from the dataset.
        
        Args:
            subset: List of column names to consider for duplicates.
                   If None, all columns are used.
            
        Returns:
            DataFrame with duplicates removed
        """
        duplicates_before = self.df.duplicated(subset=subset).sum()
        self.df = self.df.drop_duplicates(subset=subset)
        self.cleaning_log.append(f"Removed {duplicates_before} duplicate rows")
        return self.df
    
    def convert_data_types(self, column_types: dict) -> pd.DataFrame:
        """
        Convert columns to specified data types.
        
        Args:
            column_types: Dictionary mapping column names to desired types
                         e.g., {'year': 'int', 'debt': 'float'}
            
        Returns:
            DataFrame with converted types
        """
        for column, dtype in column_types.items():
            if column in self.df.columns:
                try:
                    self.df[column] = self.df[column].astype(dtype)
                    self.cleaning_log.append(f"Converted {column} to {dtype}")
                except Exception as e:
                    self.cleaning_log.append(f"Failed to convert {column} to {dtype}: {str(e)}")
        
        return self.df
    
    def handle_outliers(self, columns: List[str], method: str = "iqr", action: str = "cap") -> pd.DataFrame:
        """
        Detect and handle outliers in specified columns.
        
        Args:
            columns: List of column names to check for outliers
            method: 'iqr' for Interquartile Range method, 'zscore' for Z-score method
            action: 'cap' to cap outliers, 'remove' to remove rows with outliers
            
        Returns:
            DataFrame with outliers handled
        """
        for col in columns:
            if col not in self.df.columns or not pd.api.types.is_numeric_dtype(self.df[col]):
                continue
            
            if method == "iqr":
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers_count = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()
                
                if action == "cap":
                    self.df[col] = self.df[col].clip(lower=lower_bound, upper=upper_bound)
                    self.cleaning_log.append(f"Capped {outliers_count} outliers in {col}")
                elif action == "remove":
                    self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]
                    self.cleaning_log.append(f"Removed {outliers_count} outlier rows in {col}")
        
        return self.df
    
    def standardize_text(self, columns: List[str]) -> pd.DataFrame:
        """
        Standardize text in specified columns (trim, lowercase, etc.).
        
        Args:
            columns: List of column names to standardize
            
        Returns:
            DataFrame with standardized text
        """
        for col in columns:
            if col in self.df.columns and self.df[col].dtype == 'object':
                self.df[col] = self.df[col].str.strip().str.lower()
                self.cleaning_log.append(f"Standardized text in {col}")
        
        return self.df
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """
        Get the cleaned DataFrame.
        
        Returns:
            Cleaned pandas DataFrame
        """
        return self.df
    
    def get_cleaning_summary(self) -> dict:
        """
        Get a summary of cleaning operations performed.
        
        Returns:
            Dictionary containing cleaning statistics
        """
        return {
            "original_shape": self.original_shape,
            "cleaned_shape": self.df.shape,
            "rows_removed": self.original_shape[0] - self.df.shape[0],
            "cleaning_operations": self.cleaning_log
        }

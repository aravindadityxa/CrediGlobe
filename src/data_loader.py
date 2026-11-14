"""
Data loading and inspection utilities for CrediGlobe project.
Handles loading World Bank International Debt Statistics dataset (multiple CSV files).
"""

import pandas as pd
import os
from typing import Optional, Dict, Tuple


class DataLoader:
    """Handles loading and basic inspection of World Bank IDS data from multiple CSV files."""
    
    # World Bank IDS dataset file structure
    DATASET_FILES = {
        'data': 'IDSData.csv',              # Primary data file with debt statistics
        'country': 'IDSCountry.csv',        # Country metadata
        'series': 'IDSSeries.csv',          # Series (indicator) metadata
        'country_series': 'IDSCountry-Series.csv',  # Country-Series relationships
        'footnote': 'IDSFootNote.csv',      # Footnotes and additional information
        'series_time': 'IDSSeries-Time.csv' # Time-series metadata
    }
    
    def __init__(self, data_dir: str = "../data/raw"):
        """
        Initialize the DataLoader with the path to the dataset directory.
        
        Args:
            data_dir: Path to the directory containing World Bank IDS CSV files
        """
        self.data_dir = data_dir
        self.datasets: Dict[str, Optional[pd.DataFrame]] = {
            'data': None,
            'country': None,
            'series': None,
            'country_series': None,
            'footnote': None,
            'series_time': None
        }
    
    def check_dataset_readiness(self) -> dict:
        """
        Check if all required dataset files are present.
        
        Returns:
            Dictionary with readiness status and file information
        """
        if not os.path.exists(self.data_dir):
            return {
                "ready": False,
                "message": "Dataset directory not found",
                "missing_directory": self.data_dir,
                "instructions": [
                    f"Create directory: {self.data_dir}",
                    "Place World Bank IDS dataset CSV files in this directory:",
                    "  - IDSData.csv (primary data)",
                    "  - IDSCountry.csv (country metadata)",
                    "  - IDSCountry-Series.csv (country-series mapping)",
                    "  - IDSSeries.csv (series metadata)",
                    "  - IDSFootNote.csv (footnotes)",
                    "  - IDSSeries-Time.csv (time-series metadata)"
                ]
            }
        
        # Check which files are present
        files_status = {}
        all_present = True
        
        for key, filename in self.DATASET_FILES.items():
            filepath = os.path.join(self.data_dir, filename)
            exists = os.path.exists(filepath)
            files_status[filename] = {
                "present": exists,
                "path": filepath
            }
            if not exists:
                all_present = False
        
        if not all_present:
            missing_files = [f for f, status in files_status.items() if not status["present"]]
            return {
                "ready": False,
                "message": f"Missing {len(missing_files)} dataset file(s)",
                "files_status": files_status,
                "missing_files": missing_files,
                "instructions": [
                    f"Place the following files in {self.data_dir}:",
                    *[f"  - {f}" for f in missing_files]
                ]
            }
        
        return {
            "ready": True,
            "message": "All dataset files are present",
            "files_status": files_status
        }
    
    def load_primary_data(self) -> Tuple[bool, str]:
        """
        Load the primary data file (IDSData.csv).
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        filepath = os.path.join(self.data_dir, self.DATASET_FILES['data'])
        
        try:
            if not os.path.exists(filepath):
                return False, f"Primary data file not found at: {filepath}"
            
            self.datasets['data'] = pd.read_csv(filepath)
            return True, f"Successfully loaded {len(self.datasets['data'])} rows from IDSData.csv"
        
        except Exception as e:
            return False, f"Error loading primary data: {str(e)}"
    
    def load_metadata_file(self, file_key: str) -> Tuple[bool, str]:
        """
        Load a specific metadata file.
        
        Args:
            file_key: Key from DATASET_FILES ('country', 'series', etc.)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if file_key not in self.DATASET_FILES:
            return False, f"Unknown file key: {file_key}"
        
        filepath = os.path.join(self.data_dir, self.DATASET_FILES[file_key])
        
        try:
            if not os.path.exists(filepath):
                return False, f"File not found at: {filepath}"
            
            self.datasets[file_key] = pd.read_csv(filepath)
            return True, f"Successfully loaded {len(self.datasets[file_key])} rows from {self.DATASET_FILES[file_key]}"
        
        except Exception as e:
            return False, f"Error loading {self.DATASET_FILES[file_key]}: {str(e)}"
    
    def load_all_files(self) -> Dict[str, Tuple[bool, str]]:
        """
        Load all dataset files.
        
        Returns:
            Dictionary with load status for each file
        """
        results = {}
        
        for key in self.DATASET_FILES.keys():
            success, message = self.load_metadata_file(key)
            results[key] = (success, message)
        
        return results
    
    def get_primary_data(self) -> Optional[pd.DataFrame]:
        """
        Get the primary data DataFrame (IDSData.csv).
        
        Returns:
            Primary data DataFrame or None if not loaded
        """
        return self.datasets.get('data')
    
    def get_metadata(self, file_key: str) -> Optional[pd.DataFrame]:
        """
        Get a specific metadata DataFrame.
        
        Args:
            file_key: Key from DATASET_FILES
            
        Returns:
            Requested DataFrame or None if not loaded
        """
        return self.datasets.get(file_key)
    
    def get_basic_info(self, file_key: str = 'data') -> dict:
        """
        Get basic information about a loaded dataset.
        
        Args:
            file_key: Which dataset to inspect (default: 'data')
            
        Returns:
            Dictionary containing dataset statistics
        """
        df = self.datasets.get(file_key)
        
        if df is None:
            return {"error": f"Dataset '{file_key}' not loaded. Call load methods first."}
        
        return {
            "file": self.DATASET_FILES.get(file_key, "unknown"),
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 * 1024)
        }
    
    def display_sample(self, file_key: str = 'data', n: int = 5) -> pd.DataFrame:
        """
        Display first n rows of a dataset.
        
        Args:
            file_key: Which dataset to display
            n: Number of rows to display
            
        Returns:
            DataFrame containing first n rows
        """
        df = self.datasets.get(file_key)
        
        if df is None:
            print(f"Dataset '{file_key}' not loaded. Call load methods first.")
            return pd.DataFrame()
        
        return df.head(n)
    
    def get_dataset_summary(self) -> dict:
        """
        Get a summary of all loaded datasets.
        
        Returns:
            Dictionary with summary of all datasets
        """
        summary = {}
        
        for key, df in self.datasets.items():
            if df is not None:
                summary[key] = {
                    "file": self.DATASET_FILES[key],
                    "loaded": True,
                    "rows": len(df),
                    "columns": len(df.columns)
                }
            else:
                summary[key] = {
                    "file": self.DATASET_FILES[key],
                    "loaded": False
                }
        
        return summary

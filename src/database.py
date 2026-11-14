"""
Database operations for CrediGlobe project.
Handles SQLite database creation, table setup, and data insertion.
"""

import sqlite3
import pandas as pd
from typing import Optional, List, Tuple


class DebtDatabase:
    """Manages SQLite database operations for debt data."""
    
    def __init__(self, db_path: str = "data/crediglobe.db"):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
    
    def connect(self) -> bool:
        """
        Establish connection to the database.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def create_debt_table(self) -> bool:
        """
        Create the main debt table if it doesn't exist.
        
        Returns:
            True if table created successfully, False otherwise
        """
        if not self.conn:
            print("No database connection. Call connect() first.")
            return False
        
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS international_debt (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                country_name TEXT NOT NULL,
                country_code TEXT,
                indicator_name TEXT,
                indicator_code TEXT,
                debt_amount REAL,
                year INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            return True
        
        except Exception as e:
            print(f"Error creating table: {e}")
            return False
    
    def insert_data_from_dataframe(self, df: pd.DataFrame, table_name: str = "international_debt") -> Tuple[bool, str]:
        """
        Insert data from a pandas DataFrame into the database.
        
        Args:
            df: DataFrame containing debt data
            table_name: Name of the target table
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.conn:
            return False, "No database connection. Call connect() first."
        
        try:
            # Insert DataFrame into SQLite table
            df.to_sql(table_name, self.conn, if_exists='replace', index=False)
            self.conn.commit()
            return True, f"Successfully inserted {len(df)} rows into {table_name}"
        
        except Exception as e:
            return False, f"Error inserting data: {str(e)}"
    
    def execute_query(self, query: str) -> Optional[pd.DataFrame]:
        """
        Execute a SQL query and return results as a DataFrame.
        
        Args:
            query: SQL query to execute
            
        Returns:
            DataFrame with query results or None if error
        """
        if not self.conn:
            print("No database connection. Call connect() first.")
            return None
        
        try:
            return pd.read_sql_query(query, self.conn)
        except Exception as e:
            print(f"Query execution error: {e}")
            return None
    
    def get_total_debt_by_country(self, limit: int = 10) -> Optional[pd.DataFrame]:
        """
        Get total debt by country, sorted in descending order.
        
        Args:
            limit: Number of countries to return
            
        Returns:
            DataFrame with country and total debt
        """
        query = f"""
        SELECT 
            country_name,
            SUM(debt_amount) as total_debt
        FROM international_debt
        GROUP BY country_name
        ORDER BY total_debt DESC
        LIMIT {limit}
        """
        return self.execute_query(query)
    
    def get_debt_by_indicator(self) -> Optional[pd.DataFrame]:
        """
        Get total debt grouped by debt indicator.
        
        Returns:
            DataFrame with indicator and total debt
        """
        query = """
        SELECT 
            indicator_name,
            COUNT(*) as count,
            SUM(debt_amount) as total_debt,
            AVG(debt_amount) as avg_debt
        FROM international_debt
        GROUP BY indicator_name
        ORDER BY total_debt DESC
        """
        return self.execute_query(query)
    
    def get_country_debt_details(self, country_name: str) -> Optional[pd.DataFrame]:
        """
        Get detailed debt information for a specific country.
        
        Args:
            country_name: Name of the country
            
        Returns:
            DataFrame with country's debt details
        """
        query = f"""
        SELECT *
        FROM international_debt
        WHERE country_name = '{country_name}'
        ORDER BY debt_amount DESC
        """
        return self.execute_query(query)
    
    def get_average_debt_per_country(self) -> Optional[pd.DataFrame]:
        """
        Calculate average debt per country.
        
        Returns:
            DataFrame with country and average debt
        """
        query = """
        SELECT 
            country_name,
            AVG(debt_amount) as avg_debt,
            COUNT(*) as debt_records
        FROM international_debt
        GROUP BY country_name
        ORDER BY avg_debt DESC
        """
        return self.execute_query(query)
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

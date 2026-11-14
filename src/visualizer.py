"""
Visualization utilities for CrediGlobe project.
Creates charts and plots for debt analysis using Matplotlib and Seaborn.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Optional, List


class DebtVisualizer:
    """Handles creation of visualizations for debt analysis."""
    
    def __init__(self, output_dir: str = "visualizations"):
        """
        Initialize the visualizer.
        
        Args:
            output_dir: Directory to save generated plots
        """
        self.output_dir = output_dir
        
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
    
    def plot_top_countries_by_debt(self, df: pd.DataFrame, 
                                   country_col: str = "country_name",
                                   debt_col: str = "total_debt",
                                   top_n: int = 10,
                                   save: bool = True) -> None:
        """
        Create a bar chart of top countries by total debt.
        
        Args:
            df: DataFrame containing country and debt data
            country_col: Name of the country column
            debt_col: Name of the debt amount column
            top_n: Number of top countries to display
            save: Whether to save the plot
        """
        plt.figure(figsize=(12, 6))
        
        # Sort and select top N
        data = df.nlargest(top_n, debt_col)
        
        # Create bar plot
        ax = sns.barplot(data=data, x=debt_col, y=country_col, palette="viridis")
        
        plt.title(f"Top {top_n} Countries by Total Debt", fontsize=16, fontweight='bold')
        plt.xlabel("Total Debt (USD)", fontsize=12)
        plt.ylabel("Country", fontsize=12)
        
        # Format x-axis to show values in billions
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e9:.1f}B'))
        
        plt.tight_layout()
        
        if save:
            filepath = os.path.join(self.output_dir, "top_countries_debt.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Plot saved: {filepath}")
        
        plt.show()
    
    def plot_debt_distribution(self, df: pd.DataFrame,
                               debt_col: str = "debt_amount",
                               save: bool = True) -> None:
        """
        Create a histogram showing the distribution of debt amounts.
        
        Args:
            df: DataFrame containing debt data
            debt_col: Name of the debt amount column
            save: Whether to save the plot
        """
        plt.figure(figsize=(12, 6))
        
        # Create histogram with KDE
        sns.histplot(data=df, x=debt_col, kde=True, bins=50, color='steelblue')
        
        plt.title("Distribution of Debt Amounts", fontsize=16, fontweight='bold')
        plt.xlabel("Debt Amount (USD)", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        
        plt.tight_layout()
        
        if save:
            filepath = os.path.join(self.output_dir, "debt_distribution.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Plot saved: {filepath}")
        
        plt.show()
    
    def plot_debt_by_indicator(self, df: pd.DataFrame,
                               indicator_col: str = "indicator_name",
                               debt_col: str = "total_debt",
                               top_n: int = 10,
                               save: bool = True) -> None:
        """
        Create a horizontal bar chart of debt by indicator type.
        
        Args:
            df: DataFrame containing indicator and debt data
            indicator_col: Name of the indicator column
            debt_col: Name of the debt amount column
            top_n: Number of top indicators to display
            save: Whether to save the plot
        """
        plt.figure(figsize=(12, 8))
        
        # Sort and select top N
        data = df.nlargest(top_n, debt_col)
        
        # Create horizontal bar plot
        ax = sns.barplot(data=data, y=indicator_col, x=debt_col, palette="rocket")
        
        plt.title(f"Top {top_n} Debt Indicators by Total Amount", fontsize=16, fontweight='bold')
        plt.xlabel("Total Debt (USD)", fontsize=12)
        plt.ylabel("Debt Indicator", fontsize=12)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e9:.1f}B'))
        
        plt.tight_layout()
        
        if save:
            filepath = os.path.join(self.output_dir, "debt_by_indicator.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Plot saved: {filepath}")
        
        plt.show()
    
    def plot_country_comparison(self, df: pd.DataFrame,
                                countries: List[str],
                                country_col: str = "country_name",
                                indicator_col: str = "indicator_name",
                                debt_col: str = "debt_amount",
                                save: bool = True) -> None:
        """
        Create a grouped bar chart comparing debt across specific countries.
        
        Args:
            df: DataFrame containing debt data
            countries: List of country names to compare
            country_col: Name of the country column
            indicator_col: Name of the indicator column
            debt_col: Name of the debt amount column
            save: Whether to save the plot
        """
        # Filter for specified countries
        data = df[df[country_col].isin(countries)]
        
        if data.empty:
            print("No data found for the specified countries.")
            return
        
        plt.figure(figsize=(14, 6))
        
        # Create grouped bar plot
        sns.barplot(data=data, x=indicator_col, y=debt_col, hue=country_col, palette="Set2")
        
        plt.title("Debt Comparison Across Selected Countries", fontsize=16, fontweight='bold')
        plt.xlabel("Debt Indicator", fontsize=12)
        plt.ylabel("Debt Amount (USD)", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.legend(title="Country", bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        
        if save:
            filepath = os.path.join(self.output_dir, "country_comparison.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Plot saved: {filepath}")
        
        plt.show()
    
    def plot_correlation_heatmap(self, df: pd.DataFrame,
                                 numeric_cols: Optional[List[str]] = None,
                                 save: bool = True) -> None:
        """
        Create a correlation heatmap for numeric columns.
        
        Args:
            df: DataFrame containing numeric data
            numeric_cols: List of numeric column names (if None, auto-detect)
            save: Whether to save the plot
        """
        if numeric_cols is None:
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        if len(numeric_cols) < 2:
            print("Not enough numeric columns for correlation analysis.")
            return
        
        plt.figure(figsize=(10, 8))
        
        # Calculate correlation matrix
        corr_matrix = df[numeric_cols].corr()
        
        # Create heatmap
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                    square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        
        plt.title("Correlation Heatmap", fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save:
            filepath = os.path.join(self.output_dir, "correlation_heatmap.png")
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Plot saved: {filepath}")
        
        plt.show()

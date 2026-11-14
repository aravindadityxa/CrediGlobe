# CrediGlobe - Global Debt Analysis & Financial Insights

**Tagline:** Making Sense of Global Debt Through Data

## Overview

CrediGlobe is a comprehensive data analytics project that analyzes international debt data to provide insights into global financial patterns, country-wise debt distributions, and debt indicator trends.

## Technology Stack

- **Python 3.x** - Core programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Matplotlib** - Data visualization
- **Seaborn** - Statistical data visualization
- **SQLite** - Database for data storage and querying
- **Jupyter Notebook** - Interactive analysis environment

## Project Structure

```
CrediGlobe/
│
├── data/                          # Data directory
│   └── raw/                       # Raw dataset files
│       ├── IDSData.csv            # Primary data (to be added by user)
│       ├── IDSCountry.csv         # Country metadata (to be added)
│       ├── IDSCountry-Series.csv  # Mappings (to be added)
│       ├── IDSSeries.csv          # Series metadata (to be added)
│       ├── IDSFootNote.csv        # Footnotes (to be added)
│       └── IDSSeries-Time.csv     # Time metadata (to be added)
│
├── src/                           # Source code
│   ├── data_loader.py             # Data loading and inspection
│   ├── data_cleaner.py            # Data cleaning and preprocessing
│   ├── database.py                # Database operations
│   ├── visualizer.py              # Visualization functions
│   └── main.py                    # Main application entry point
│
├── notebooks/                     # Jupyter notebooks
│   └── debt_analysis.ipynb        # Interactive analysis notebook
│
├── visualizations/                # Generated charts and plots
│
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

## Installation

### Prerequisites

**Python Installation Required:**
This project requires Python 3.8 or higher. If you don't have Python installed:

**Windows:**
- Download Python from: https://www.python.org/downloads/
- During installation, **check "Add Python to PATH"**
- Verify installation: `python --version` or `py --version`

**Alternative:** Use Anaconda/Miniconda if you prefer: https://www.anaconda.com/

### Setup Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd c:\projects\CrediGlobe
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Dataset Setup

⚠️ **IMPORTANT: World Bank IDS Dataset Required**

This project uses the **World Bank International Debt Statistics** dataset, which consists of multiple CSV files.

### Where to Add the Dataset:

1. **Download the World Bank IDS dataset** (containing multiple CSV files)
2. **Place all CSV files** in the `data/raw/` folder
3. **Required files:**
   - `IDSData.csv` (primary data file with debt statistics)
   - `IDSCountry.csv` (country metadata)
   - `IDSCountry-Series.csv` (country-series relationships)
   - `IDSSeries.csv` (series/indicator metadata)
   - `IDSFootNote.csv` (footnotes and notes)
   - `IDSSeries-Time.csv` (time-series metadata)

4. **Full path structure should be:**
   ```
   C:\projects\CrediGlobe\data\raw\
   ├── IDSData.csv
   ├── IDSCountry.csv
   ├── IDSCountry-Series.csv
   ├── IDSSeries.csv
   ├── IDSFootNote.csv
   └── IDSSeries-Time.csv
   ```

### Dataset Information:

**Primary Data File:** `IDSData.csv` contains the main debt statistics

**Supporting Files:** Other CSV files provide metadata about countries, indicators, and time periods

The code will automatically detect all files and load them appropriately. Column names will be inspected from the actual CSV files - no assumptions are made about the data structure.

## Usage

### Option 1: Run the Main Python Application

```bash
cd src
python main.py
```

This will:
- Check for the dataset
- Load and clean the data
- Store it in SQLite database
- Perform SQL analysis
- Generate visualizations

### Option 2: Use Jupyter Notebook (Interactive)

1. **Start Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```

2. **Open the notebook:**
   - Navigate to `notebooks/debt_analysis.ipynb`
   - Run cells sequentially

3. **Follow the analysis steps:**
   - Data loading and exploration
   - Data cleaning
   - Database operations
   - Visualizations
   - Key findings

## Features

### Data Processing
- Automated data loading with validation
- Comprehensive data cleaning (missing values, duplicates)
- Data type conversions and standardization
- Outlier detection and handling

### Database Operations
- SQLite database creation and management
- Efficient data storage
- Pre-built SQL queries for common analyses:
  - Top countries by total debt
  - Debt by indicator type
  - Average debt per country
  - Country-specific debt details

### Visualizations
- Top countries by debt (bar chart)
- Debt distribution (histogram with KDE)
- Debt by indicator type (horizontal bar chart)
- Country comparison charts
- Correlation heatmaps

### Analysis
- Country-wise debt analysis
- Debt indicator trends
- Statistical summaries
- Comparative analysis

## Code Structure

### data_loader.py
Handles loading World Bank IDS dataset (multiple CSV files), basic inspection, and dataset validation.

### data_cleaner.py
Provides functions for cleaning data, handling missing values, removing duplicates, and managing outliers.

### database.py
Manages SQLite database operations including table creation, data insertion, and SQL queries.

### visualizer.py
Creates professional visualizations using Matplotlib and Seaborn.

### main.py
Orchestrates the complete analysis pipeline from loading multiple CSV files to visualization generation.

## Output

After running the analysis, you will find:

1. **Database file:** `data/crediglobe.db` - SQLite database with cleaned data
2. **Visualizations:** `visualizations/` folder - PNG charts and plots
3. **Console output:** Analysis results and statistics

## Troubleshooting

### "Dataset Not Found" Error
- Ensure all CSV files are in the `data/raw/` folder
- Required files: IDSData.csv, IDSCountry.csv, IDSCountry-Series.csv, IDSSeries.csv, IDSFootNote.csv, IDSSeries-Time.csv
- Check file names match exactly (case-sensitive on some systems)

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment if using one

### Visualization Issues
- Close plot windows to proceed to the next visualization
- Check that the `visualizations/` folder exists

## Next Steps

After adding your dataset:

1. Run `python src/main.py` to perform the complete analysis
2. Review generated visualizations in the `visualizations/` folder
3. Explore the Jupyter notebook for interactive analysis
4. Query the SQLite database for custom insights

## Contributing

This is a learning project. Feel free to extend it with:
- Additional visualizations
- More complex SQL queries
- Time-series analysis (if year data is available)
- Predictive modeling
- Interactive dashboards

## License

See LICENSE file for details.

---

**Project Status:** Ready for dataset integration
**Last Updated:** 2026-11-13
Global Debt Analysis using Python, SQL, Data Cleaning, Exploratory Data Analysis (EDA), and Data Visualization.

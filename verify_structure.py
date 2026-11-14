"""
Simple structure verification script.
Checks project structure without requiring any dependencies.
"""

import os

print("=" * 60)
print("CrediGlobe - Structure Verification")
print("=" * 60)
print()

# Get project root
project_root = os.path.dirname(os.path.abspath(__file__))

# Check directory structure
print("Checking directory structure...")
required_dirs = {
    'data': 'Dataset directory',
    'data/raw': 'Raw dataset files',
    'src': 'Source code',
    'notebooks': 'Jupyter notebooks',
    'visualizations': 'Output charts'
}

all_dirs_ok = True
for directory, description in required_dirs.items():
    path = os.path.join(project_root, directory)
    if os.path.exists(path) and os.path.isdir(path):
        print(f"  ✓ {directory}/ - {description}")
    else:
        print(f"  ✗ {directory}/ - MISSING")
        all_dirs_ok = False

print()

# Check required files
print("Checking required files...")
required_files = {
    'README.md': 'Project documentation',
    'requirements.txt': 'Python dependencies',
    'src/data_loader.py': 'Data loading module',
    'src/data_cleaner.py': 'Data cleaning module',
    'src/database.py': 'Database operations',
    'src/visualizer.py': 'Visualization module',
    'src/main.py': 'Main application',
    'notebooks/debt_analysis.ipynb': 'Analysis notebook'
}

all_files_ok = True
for filepath, description in required_files.items():
    full_path = os.path.join(project_root, filepath)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        print(f"  ✓ {filepath} - {description}")
    else:
        print(f"  ✗ {filepath} - MISSING")
        all_files_ok = False

print()

# Check for dataset
print("Checking for dataset...")
dataset_dir = os.path.join(project_root, 'data', 'raw')
dataset_files = [
    'IDSData.csv',
    'IDSCountry.csv',
    'IDSCountry-Series.csv',
    'IDSSeries.csv',
    'IDSFootNote.csv',
    'IDSSeries-Time.csv'
]

if not os.path.exists(dataset_dir):
    print(f"  ⚠️  Dataset directory not found")
    print(f"     Expected: {dataset_dir}")
else:
    found_files = []
    missing_files = []
    
    for filename in dataset_files:
        filepath = os.path.join(dataset_dir, filename)
        if os.path.exists(filepath):
            found_files.append(filename)
            print(f"  ✓ {filename} found")
        else:
            missing_files.append(filename)
            print(f"  ⚠️  {filename} not found")
    
    if missing_files:
        print(f"\n  Missing {len(missing_files)} file(s). Place them in:")
        print(f"  {dataset_dir}")
    else:
        print("\n  ✓ All dataset files present!")

print()
print("=" * 60)

if all_dirs_ok and all_files_ok:
    print("✓ Project structure is complete and ready!")
    print()
    dataset_ready = all(os.path.exists(os.path.join(dataset_dir, f)) for f in dataset_files)
    if not dataset_ready:
        print("Next steps:")
        print("1. Install Python dependencies: pip install -r requirements.txt")
        print("2. Add World Bank IDS dataset files to:")
        print(f"   {dataset_dir}")
        print("   Required files:")
        for f in dataset_files:
            print(f"     - {f}")
        print("3. Run analysis from src folder:")
        print("   cd src")
        print("   python main.py")
else:
    print("✗ Project structure has missing components")
    print("Please ensure all required files and directories exist")

print("=" * 60)

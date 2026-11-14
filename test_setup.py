"""
Test script to verify CrediGlobe project setup.
Run this to check if all components are properly configured.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("CrediGlobe Setup Test")
print("=" * 60)
print()

# Test 1: Check directory structure
print("Test 1: Checking directory structure...")
required_dirs = ['data', 'src', 'notebooks', 'visualizations']
for directory in required_dirs:
    path = os.path.join(os.path.dirname(__file__), directory)
    if os.path.exists(path):
        print(f"  ✓ {directory}/ exists")
    else:
        print(f"  ✗ {directory}/ missing")

print()

# Test 2: Check source files
print("Test 2: Checking source files...")
required_files = [
    'src/data_loader.py',
    'src/data_cleaner.py',
    'src/database.py',
    'src/visualizer.py',
    'src/main.py'
]
for filepath in required_files:
    path = os.path.join(os.path.dirname(__file__), filepath)
    if os.path.exists(path):
        print(f"  ✓ {filepath} exists")
    else:
        print(f"  ✗ {filepath} missing")

print()

# Test 3: Try importing modules
print("Test 3: Testing module imports...")
try:
    from data_loader import DataLoader
    print("  ✓ DataLoader imported successfully")
except ImportError as e:
    print(f"  ✗ Failed to import DataLoader: {e}")

try:
    from data_cleaner import DataCleaner
    print("  ✓ DataCleaner imported successfully")
except ImportError as e:
    print(f"  ✗ Failed to import DataCleaner: {e}")

try:
    from database import DebtDatabase
    print("  ✓ DebtDatabase imported successfully")
except ImportError as e:
    print(f"  ✗ Failed to import DebtDatabase: {e}")

try:
    from visualizer import DebtVisualizer
    print("  ✓ DebtVisualizer imported successfully")
except ImportError as e:
    print(f"  ✗ Failed to import DebtVisualizer: {e}")

print()

# Test 4: Check for dataset
print("Test 4: Checking for dataset...")
dataset_path = os.path.join(os.path.dirname(__file__), 'data', 'international_debt.csv')
if os.path.exists(dataset_path):
    print(f"  ✓ Dataset found at: {dataset_path}")
else:
    print(f"  ⚠️  Dataset not found (expected)")
    print(f"     Place your CSV file at: {dataset_path}")

print()

# Test 5: Test DataLoader with missing dataset
print("Test 5: Testing DataLoader with missing dataset...")
try:
    from data_loader import DataLoader
    loader = DataLoader(data_dir=os.path.join(os.path.dirname(__file__), "data", "raw"))
    readiness = loader.check_dataset_readiness()
    
    if not readiness['ready']:
        print("  ✓ DataLoader correctly detected missing dataset")
        print(f"     Message: {readiness['message']}")
    else:
        print("  ⚠️  Dataset appears to be present")
        print("     All required files found")
except Exception as e:
    print(f"  ✗ Error testing DataLoader: {e}")

print()
print("=" * 60)
print("Setup test complete!")
print()
print("Next steps:")
print("1. Install dependencies: pip install -r requirements.txt")
print("2. Add World Bank IDS dataset files to: data\\raw\\")
print("   Required files:")
print("     - IDSData.csv")
print("     - IDSCountry.csv")
print("     - IDSCountry-Series.csv")
print("     - IDSSeries.csv")
print("     - IDSFootNote.csv")
print("     - IDSSeries-Time.csv")
print("3. Run the analysis from src folder:")
print("   cd src")
print("   python main.py")
print("=" * 60)

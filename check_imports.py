"""
Check if Python modules can be imported.
This verifies the code structure without requiring a dataset.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("CrediGlobe - Import Check")
print("=" * 60)
print()

errors = []

# Test standard library imports
print("Testing standard library imports...")
try:
    import os
    import sys
    print("  ✓ os, sys")
except ImportError as e:
    errors.append(f"Standard library error: {e}")
    print(f"  ✗ Error: {e}")

print()

# Test if pandas is available
print("Testing required packages...")
try:
    import pandas
    print(f"  ✓ pandas ({pandas.__version__})")
except ImportError:
    errors.append("pandas not installed")
    print("  ✗ pandas - NOT INSTALLED")
    print("     Run: pip install -r requirements.txt")

try:
    import numpy
    print(f"  ✓ numpy ({numpy.__version__})")
except ImportError:
    errors.append("numpy not installed")
    print("  ✗ numpy - NOT INSTALLED")

try:
    import matplotlib
    print(f"  ✓ matplotlib ({matplotlib.__version__})")
except ImportError:
    errors.append("matplotlib not installed")
    print("  ✗ matplotlib - NOT INSTALLED")

try:
    import seaborn
    print(f"  ✓ seaborn ({seaborn.__version__})")
except ImportError:
    errors.append("seaborn not installed")
    print("  ✗ seaborn - NOT INSTALLED")

print()

# Test custom module imports
print("Testing custom module imports...")
try:
    from data_loader import DataLoader
    print("  ✓ data_loader.DataLoader")
except ImportError as e:
    errors.append(f"data_loader import error: {e}")
    print(f"  ✗ data_loader - {e}")

try:
    from data_cleaner import DataCleaner
    print("  ✓ data_cleaner.DataCleaner")
except ImportError as e:
    errors.append(f"data_cleaner import error: {e}")
    print(f"  ✗ data_cleaner - {e}")

try:
    from database import DebtDatabase
    print("  ✓ database.DebtDatabase")
except ImportError as e:
    errors.append(f"database import error: {e}")
    print(f"  ✗ database - {e}")

try:
    from visualizer import DebtVisualizer
    print("  ✓ visualizer.DebtVisualizer")
except ImportError as e:
    errors.append(f"visualizer import error: {e}")
    print(f"  ✗ visualizer - {e}")

print()
print("=" * 60)

if not errors:
    print("✓ All imports successful!")
    print()
    print("The project is ready to use.")
    print("Add your dataset and run: cd src && python main.py")
else:
    print(f"✗ Found {len(errors)} issue(s):")
    for error in errors:
        print(f"  - {error}")
    print()
    if any("not installed" in e for e in errors):
        print("Install dependencies with: pip install -r requirements.txt")

print("=" * 60)

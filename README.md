# Antenna export scripts

This repo includes some simple Python scripts that can be used to export data from [Antenna](https://antenna.insectai.org) to CSV files. Checkout https://api.antenna.insectai.org/api/v2/docs/ for different fetch options and feel free to tweak the scripts as needed 🦋

## Setup environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate environment
source .venv/bin/activate

# Install requirements
pip3 install -r requirements.txt
```

## Export data

```bash
# Export occurrence
python3 export-occurrences.py
```

# Antenna help scripts

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

## Export scripts

```bash
# Export occurrences
python3 export-occurrences.py

# Export taxa stats (top taxon for each project)
python3 export-taxa-stats.py
```

## Cateogry map scripts

```bash
# Collect data from Fieldguide based on a category map
python3 collect-fg-data.py

# Update a species list with data from Fieldguide
python3 update-species-list.py
```

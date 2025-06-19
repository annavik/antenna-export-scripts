# Antenna help scripts

This repo includes some simple Python scripts that can be used to export data from [Antenna](https://antenna.insectai.org). Checkout https://api.antenna.insectai.org/api/v2/docs/ for different fetch options and feel free to tweak the scripts as needed 🦋

## Setup environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate environment
source .venv/bin/activate

# Install requirements
pip3 install -r requirements.txt
```

## Scripts

```bash
# Export occurrences
python3 export-occurrences.py

# Export taxa stats (top taxon for each project)
python3 export-taxa-stats.py
```

### Scripts to extend taxa

```bash
# Collect labels from algorithms avaible on Antenna
python3 extend-taxa/collect-labels.py

# Extend labels with data from Antenna, GBIF and Fieldguide
python3 extend-taxa/collect-label-data.py
```

### Scripts for Totumas

```bash
# Collect data from Fieldguide based on a category map
python3 totumas/collect-fg-data.py

# Update a species list with data from Fieldguide
python3 totumas/update-species-list.py

# Export data (including images) from a taxa list
python3 totumas/export-taxa-list.py

# Resize exported images
python3 totumas/resize-images.py
```

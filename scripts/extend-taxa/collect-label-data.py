import csv
import requests

# Input config
labels_path = "labels.csv"
antenna_taxa_api_url = "https://api.antenna.insectai.org/api/v2/taxa/?name=%s"
gbif_taxon_api_url = "https://api.gbif.org/v1/species/search?datasetKey=d7dddbf4-2cf0-4f39-9b2a-bb099caae36c&q=%s&limit=10"
fieldguide_categories_api_url = "https://fieldguide.ai/api2/search/search?category=5926f024fd89783b2a721ba8&keywords=%s&limit=10"
fieldguide_category_api_url = (
    "https://fieldguide.ai/api2/categories/category_details?category_id=%s"
)
start_index = 0

# Output config
csv_output = "labels-extended.csv"  # Expected CSV format: label,antenna_id,gbif_key,fieldguide_id,cover_image_url,cover_image_credit


def collect_label_data(label, csvwriter):
    print("fetching data for label: ", label)

    antenna_id = None
    gbif_key = None
    fieldguide_id = None
    cover_image_url = None
    cover_image_credit = None

    antenna_taxon = get_antenna_taxon(label)
    if antenna_taxon is not None:
        antenna_id = antenna_taxon["id"]

    gbif_taxon = get_gbif_taxon(label)
    if gbif_taxon is not None:
        gbif_key = gbif_taxon["key"]

    fieldguide_category = get_fieldguide_category(label)
    if fieldguide_category is not None:
        if label == fieldguide_category["scientific_name"]:  # Require exact match
            fieldguide_id = fieldguide_category["id"]

            if "cover_image" in fieldguide_category:
                cover_image_url = fieldguide_category["cover_image"]["image_url"]
                cover_image_credit = fieldguide_category["cover_image"]["copyright"]

    csvwriter.writerow(
        [
            label,
            antenna_id,
            gbif_key,
            fieldguide_id,
            cover_image_url,
            cover_image_credit,
        ]
    )


# Based on a label, search Antenna for a matching taxon
def get_antenna_taxon(label):
    taxa_response = requests.get(antenna_taxa_api_url % (label))
    taxa_data = taxa_response.json()

    if len(taxa_data["results"]):
        for taxon in taxa_data["results"]:
            if label == taxon["name"]:  # Require exact match
                return taxon

    return None


# Based on a label, search GBIF for a matching taxon
def get_gbif_taxon(label):
    taxa_response = requests.get(gbif_taxon_api_url % (label))
    taxa_data = taxa_response.json()

    if len(taxa_data["results"]):
        for taxon in taxa_data["results"]:
            if "canonicalName" in taxon:
                if label == taxon["canonicalName"]:  # Require exact match
                    return taxon

    return None


# Based on a label, search Fieldguide for a matching category
def get_fieldguide_category(label):
    categories_response = requests.get(fieldguide_categories_api_url % (label))
    categories_data = categories_response.json()

    if len(categories_data):
        category = categories_data[0]

        if category["object_type"] != "category":
            return None

        category_details_response = requests.get(
            fieldguide_category_api_url % (category["id"])
        )
        category_details_data = category_details_response.json()

        if category_details_data is not None:
            if label == category_details_data["scientific_name"]:  # Require exact match
                return category_details_data

    return None


# Read data
labels = []
with open(labels_path, "r") as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)

    for row in csvreader:
        labels.append(row[0])

# Write data
with open(csv_output, "a") as csvfile:
    csvwriter = csv.writer(csvfile)

    for index, label in enumerate(labels):
        if index >= start_index:
            collect_label_data(label, csvwriter=csvwriter)

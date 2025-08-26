import csv
import requests

# Input config
labels_fetch_url = "https://api.antenna.insectai.org/api/v2/ml/labels/337/"
taxa_fetch_url = "https://api.antenna.insectai.org/api/v2/taxa/?name=%s"
taxon_details_fetch_url = "https://api.antenna.insectai.org/api/v2/taxa/%s/"

# Output config
csv_output = "panama-2023.csv"


# Collect data about taxa based on a label map
def get_taxa():
    print("fetching labels")
    labels_response = requests.get(labels_fetch_url)
    labels_data = labels_response.json()
    taxa = []

    if len(labels_data["labels"]):
        for label in labels_data["labels"]:
            print("fetching data for label ", label)

            taxon = get_taxon(label)
            if taxon is not None:

                def get_parent_label(rank):
                    for item in taxon["parents"]:
                        if item["rank"] == rank:
                            return item["name"]

                taxa.append(
                    [
                        get_parent_label("PHYLUM"),  # PHYLUM
                        get_parent_label("CLASS"),  # CLASS
                        get_parent_label("ORDER"),  # ORDER
                        get_parent_label("SUPERFAMILY"),  # SUPERFAMILY
                        get_parent_label("FAMILY"),  # FAMILY
                        get_parent_label("SUBFAMILY"),  # SUBFAMILY
                        get_parent_label("TRIBE"),  # TRIBE
                        get_parent_label("GENUS"),  # GENUS
                        label,  # SPECIES
                        None,  # COMMON_NAME
                        taxon["gbif_taxon_key"],  # GBIF_TAXON_KEY
                        None,  # INAT_TAXON_KEY
                        taxon["id"],  # ANTENNA_TAXON_ID
                    ]
                )
            else:
                taxa.append(
                    [
                        None,  # PHYLUM
                        None,  # CLASS
                        None,  # ORDER
                        None,  # SUPERFAMILY
                        None,  # FAMILY
                        None,  # SUBFAMILY
                        None,  # TRIBE
                        None,  # GENUS
                        label,  # SPECIES
                        None,  # COMMON_NAME
                        None,  # GBIF_TAXON_KEY
                        None,  # INAT_TAXON_KEY
                        None,  # ANTENNA_TAXON_ID
                    ]
                )

    return taxa


# Based on a label, search Antenna for a matching taxon
def get_taxon(label):
    taxa_response = requests.get(taxa_fetch_url % (label))

    if not taxa_response.ok:
        print("error fetching, trying again...")
        return get_taxon(label)

    taxa_data = taxa_response.json()

    if len(taxa_data["results"]):
        for taxon in taxa_data["results"]:
            if label == taxon["name"]:  # Require exact match
                taxon_details_response = requests.get(
                    taxon_details_fetch_url % (taxon["id"])
                )

                if not taxon_details_response.ok:
                    print("error fetching, trying again...")
                    return get_taxon(label)

                return taxon_details_response.json()

    return None


with open(csv_output, "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(
        [
            "PHYLUM",
            "CLASS",
            "ORDER",
            "SUPERFAMILY",
            "FAMILY",
            "SUBFAMILY",
            "TRIBE",
            "GENUS",
            "SPECIES",
            "COMMON_NAME",
            "GBIF_TAXON_KEY",
            "INAT_TAXON_ID",
            "ANTENNA_TAXON_ID",
        ]
    )
    csvwriter.writerows(get_taxa())

import csv
import requests

# Input config
fetch_url = "https://antenna.insectai.org/api/v2/projects"
fieldguide_api_url = "https://fieldguide.ai/api2"
fieldguide_parent_category = "5926f024fd89783b2a721ba8"  # Lepidoptera

# Output config
csv_output = "taxa-stats.csv"


# Summarize taxa stats for all projects
def get_taxa_stats():
    print("fetching projects")
    projects_response = requests.get(fetch_url)
    projects_data = projects_response.json()
    taxa_stats = []

    if len(projects_data["results"]):
        for project in projects_data["results"]:
            taxon = get_top_taxon(project["id"])

            if taxon is None:
                taxa_stats.append(
                    [
                        project["id"],
                        project["name"],
                    ]
                )
                continue

            fieldguide_category = get_fieldguide_category(taxon["name"])

            if fieldguide_category is None:
                taxa_stats.append(
                    [
                        project["id"],
                        project["name"],
                        taxon["id"],
                        taxon["name"],
                        taxon["rank"].upper(),
                        taxon["occurrences_count"],
                    ]
                )
                continue

            taxa_stats.append(
                [
                    project["id"],
                    project["name"],
                    taxon["id"],
                    taxon["name"],
                    taxon["rank"].upper(),
                    taxon["occurrences_count"],
                    fieldguide_category["id"],
                    "https://leps.fieldguide.ai/figures?category=%s"
                    % (fieldguide_category["id"]),
                    fieldguide_category["base_image_url"],
                ]
            )

    return taxa_stats


# Get the taxon with most occurrences for a specific project
def get_top_taxon(project_id):
    print("fetching taxa for project ", project_id)
    taxa_response = requests.get(
        "https://antenna.insectai.org/api/v2/taxa/?&project_id=%s&ordering=-occurrences_count&limit=1&offset=0"
        % (project_id)
    )
    taxa_data = taxa_response.json()

    if len(taxa_data["results"]):
        return taxa_data["results"][0]

    return None


# Based on a keyword, search Fieldguide for a matching category
def get_fieldguide_category(keyword):
    print("fetching category from Fieldguide using keyword ", keyword)
    categories_response = requests.get(
        "%s/search/search?category=%s&keywords=%s&limit=1"
        % (fieldguide_api_url, fieldguide_parent_category, keyword)
    )
    categories_data = categories_response.json()

    if len(categories_data):
        category = categories_data[0]

        if category["object_type"] != "category":
            return None

        return category

    return None


with open(csv_output, "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(
        [
            "project_id",
            "project_name",
            "taxon_id",
            "taxon_name",
            "taxon_rank",
            "occurrences_count",
            "fieldguide_category_id",
            "fieldguide_url",
            "fieldguide_cover_image_url",
        ]
    )
    csvwriter.writerows(get_taxa_stats())

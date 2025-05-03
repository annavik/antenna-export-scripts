import json
import os
import re
import requests

# Tweak this based on project and filtering preferences
fetch_url = "https://ood.antenna.insectai.org/api/v2/taxa/?project_id=4&limit=20&offset=0&taxa_list_id=9"
detail_fetch_url = "https://ood.antenna.insectai.org/api/v2/taxa/%s?project_id=4"

# Export results will be saved to this file
json_output = "../output/taxa.json"
images_output = "../output/images/"


# TODO: Skip this when we can get all data from the API list response
def get_selected_occurrence_url(taxon_id):
    print("fetching details for taxon", taxon_id)
    details_response = requests.get(detail_fetch_url % (taxon_id))
    if details_response.ok:
        details_data = details_response.json()
        try:
            return details_data["occurrences"][0]["best_detection"]["url"]
        except Exception:
            print("selected occurrence missing for taxon ", taxon_id)
            return None
    else:
        print("error fetching details for taxon, trying again...")
        return get_selected_occurrence_url(taxon_id)


def save_image(image_url, key, id):
    filename = "%s_%s_crop.jpg" % (key, id)
    print("saving image ", filename)
    img_data = requests.get(image_url).content
    with open(images_output + filename, "wb") as handler:
        handler.write(img_data)
        return filename


def export_taxa(url, page_count, taxa):
    print("fetching page ", page_count)
    response = requests.get(url)
    if not response.ok:
        print("error fetching page, trying again...")
        export_taxa(url, page_count, taxa)
    else:
        data = response.json()
        if len(data["results"]):
            for taxon in data["results"]:
                name = re.sub(
                    r"\(Collection \d+\) \(Job \d+\)", "", taxon["name"]
                ).strip()
                key = re.sub(r"\W+", "_", name.lower())
                selected_occurrence_url = get_selected_occurrence_url(taxon["id"])
                if selected_occurrence_url:
                    selected_occurrence_filename = save_image(
                        selected_occurrence_url, key, str(taxon["id"])
                    )
                else:
                    selected_occurrence_filename = None
                taxa.append(
                    {
                        "id": taxon["id"],
                        "name": name,
                        "rank": taxon["rank"],
                        "occurrences_count": taxon["occurrences_count"],
                        "last_detected": taxon["last_detected"],
                        "parents": [],  # TODO: Update when backend is returning data here
                        "selected_occurrence_url": selected_occurrence_url,
                        "selected_occurrence_filename": selected_occurrence_filename,
                        "cover_image_url": (
                            taxon["cover_image_url"] if "cover_image" in taxon else None
                        ),
                        "cover_image_credit": (
                            taxon["cover_image_credit"]
                            if "cover_image_credit" in taxon
                            else None
                        ),
                        "most_similar_taxon": None,  # TODO: Update when backend is returning data here
                    }
                )

        # Go to next page, if there is one
        if data["next"]:
            export_taxa(data["next"], page_count + 1, taxa)


os.makedirs(images_output, exist_ok=True)
taxa = []
export_taxa(fetch_url, 1, taxa)

with open(json_output, "w") as outfile:
    outfile.write(json.dumps(taxa, indent=4))

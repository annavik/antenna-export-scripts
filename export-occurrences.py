import csv
import requests


fetch_url = "https://antenna.insectai.org/api/v2/occurrences/?project_id=107&ordering=-created_at&limit=20&offset=0&classification_threshold=0&deployment=280&date_end=2024-08-01&date_start=2024-07-31"

csv_output = "occurrences.csv"


def export_occurrences(url, page_count, csvwriter):
    print("fetching page ", page_count)
    response = requests.get(url)
    data = response.json()

    if len(data["results"]):
        write_occurrences_to_csv(csvwriter, data["results"])

    if data["next"]:
        # Go to next page
        export_occurrences(data["next"], page_count + 1, csvwriter)


def write_occurrences_to_csv(csvwriter, occurrences):
    for occurrence in occurrences:
        id = occurrence["id"]
        timestamp = occurrence["first_appearance_timestamp"]
        taxon_id = occurrence["determination_details"]["taxon"]["id"]
        taxon_label = occurrence["determination_details"]["taxon"]["name"]
        binary_label = "Non-Moth" if taxon_id == 11613 else "Moth"
        score = occurrence["determination_score"]

        csvwriter.writerow(
            [
                id,
                timestamp,
                taxon_id,
                taxon_label,
                binary_label,
                score,
            ]
        )


with open(csv_output, "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(
        [
            "id",
            "timestamp",
            "taxon_id",
            "taxon_label",
            "binary_label",
            "score",
        ]
    )
    export_occurrences(fetch_url, 1, csvwriter)

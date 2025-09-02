import csv
import requests

# Input config
antenna_algorithms_api_url = "https://api.antenna.insectai.org/api/v2/ml/algorithms/"
antenna_labels_api_url = "https://api.antenna.insectai.org/api/v2/ml/labels/%s/"

# Output config
csv_output = "labels.csv"


# Collect labels for all algorithms
def get_labels():
    print("fetching algorithms")
    algorithms_response = requests.get(antenna_algorithms_api_url)
    algorithms_data = algorithms_response.json()
    labels = []

    if len(algorithms_data["results"]):
        for algorithm in algorithms_data["results"]:
            print("fetching labels for algorithm ", algorithm["id"])
            labels_response = requests.get(antenna_labels_api_url % (algorithm["id"]))
            labels_data = labels_response.json()
            for label in labels_data["labels"]:
                if label not in labels:
                    labels.append(label)

    return labels


with open(csv_output, "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(
        [
            "label",
        ]
    )
    labels = get_labels()
    for label in labels:
        csvwriter.writerow([label])

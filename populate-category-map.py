import csv
import requests

category_map_url = "https://object-arbutus.cloud.computecanada.ca/ami-models/moths/classification/panama_plus_category_map-with_names.json"  # Category map will be fetched from this URL
csv_output = "populated-category-map.csv"  # Export results will be saved to this file
fieldguide_api_url = "https://fieldguide.ai/api2"
fieldguide_parent_category = "5926f024fd89783b2a721ba8"  # Lepidoptera


# Fetch category map and populate records with reference data from Fieldguide
def populate_category_map(start_index, end_index, csvwriter):
    print("fetching category map")
    category_map_response = requests.get(category_map_url)
    category_map_data = category_map_response.json()
    category_map = [
        {"index": value, "label": key} for key, value in category_map_data.items()
    ]

    if len(category_map):
        for item in category_map:
            if item["index"] < start_index or item["index"] > end_index:
                continue

            print("fetching data for category: ", item["index"], item["label"])
            fieldguide_category = get_fieldguide_category(item["label"])

            # Fieldguide data not present
            if fieldguide_category is None:
                csvwriter.writerow(
                    [
                        item["label"],
                        item["index"],
                    ]
                )
                continue

            # Fieldguide data present, but no cover image
            if "cover_image" not in fieldguide_category:
                csvwriter.writerow(
                    [
                        item["label"],
                        item["index"],
                        fieldguide_category["id"],
                        fieldguide_category["scientific_name"],
                        None,
                        None,
                        None,
                        fieldguide_category["common_name"],
                    ]
                )
                continue

            # Fieldguide data present
            csvwriter.writerow(
                [
                    item["label"],
                    item["index"],
                    fieldguide_category["id"],
                    fieldguide_category["scientific_name"],
                    fieldguide_category["cover_image"]["base_image_url"],
                    fieldguide_category["cover_image"]["image_url"],
                    fieldguide_category["cover_image"]["copyright"],
                    fieldguide_category["common_name"],
                ]
            )


# Based on a keyword, search Fieldguide for a matching category
def get_fieldguide_category(keyword):
    categories_response = requests.get(
        "%s/search/search?category=%s&keywords=%s&limit=1"
        % (fieldguide_api_url, fieldguide_parent_category, keyword)
    )
    categories_data = categories_response.json()

    if len(categories_data):
        category = categories_data[0]

        if category["object_type"] != "category":
            return None

        category_details_response = requests.get(
            "%s/categories/category_details?category_id=%s"
            % (fieldguide_api_url, category["id"])
        )
        category_details_data = category_details_response.json()

        return category_details_data

    return None


with open(csv_output, "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(
        [
            "label",
            "index",
            "fieldguide_id",
            "fieldguide_label",
            "cover_image_base_url",
            "cover_image_url",
            "cover_image_copyright",
            "common_name_en",
        ]
    )

    populate_category_map(start_index=0, end_index=2359, csvwriter=csvwriter)

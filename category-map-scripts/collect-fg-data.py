import csv
import requests

category_map_url = "https://object-arbutus.cloud.computecanada.ca/ami-models/moths/classification/panama_plus_category_map-with_names.json"  # Category map will be fetched from this URL
csv_output = "fg-data.csv"  # Export results will be saved to this file
fieldguide_api_url = "https://fieldguide.ai/api2"
fieldguide_parent_category = "5926f024fd89783b2a721ba8"  # Lepidoptera


# Fetch category map and populate records with data from Fieldguide
def collect_fg_data(start_index, end_index, csvwriter):
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
            fieldguide_id = None
            fieldguide_label = None
            cover_image_base_url = None
            cover_image_url = None
            cover_image_copyright = None
            common_name_en = None
            exact_math = None

            if fieldguide_category is not None:
                fieldguide_id = fieldguide_category["id"]
                fieldguide_label = fieldguide_category["scientific_name"]
                common_name_en = fieldguide_category["common_name"]

                if "cover_image" in fieldguide_category:
                    cover_image_base_url = fieldguide_category["cover_image"][
                        "base_image_url"
                    ]
                    cover_image_url = fieldguide_category["cover_image"]["image_url"]
                    cover_image_copyright = fieldguide_category["cover_image"][
                        "copyright"
                    ]

                if fieldguide_label == item["label"]:
                    exact_math = True

            csvwriter.writerow(
                [
                    item["label"],
                    item["index"],
                    fieldguide_id,
                    fieldguide_label,
                    cover_image_base_url,
                    cover_image_url,
                    cover_image_copyright,
                    common_name_en,
                    exact_math,
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
            "gbif_name",
            "category_map_index",
            "fieldguide_id",
            "fieldguide_label",
            "cover_image_base_url",
            "cover_image_url",
            "cover_image_copyright",
            "common_name_en",
            "exact_match",
        ]
    )

    collect_fg_data(start_index=0, end_index=2359, csvwriter=csvwriter)

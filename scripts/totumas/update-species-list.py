import csv

# Input config
species_list_path = "complete-panama-list.csv"  # Expected CSV format: gbif_name,gbif_key,fieldguide_id,cover_image_url,cover_image_copyright,antenna_id,inat_id,category_map_index,common_name_en,training_images_count,example_occurrence_image_url,genus,family
fg_data_path = "fg-data.csv"  # Expected CSV format: gbif_name,category_map_index,fieldguide_id,fieldguide_label,cover_image_base_url,cover_image_url,cover_image_copyright,common_name_en,exact_match

# Output config
csv_output = "complete-panama-list-updated.csv"


# Read data
species_list = []
with open(species_list_path, "r") as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)

    for row in csvreader:
        species_list.append(row)

fg_data = []
with open(fg_data_path, "r") as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)

    for row in csvreader:
        fg_data.append(row)

# Combine data
updated_species_list = []
for index, row in enumerate(species_list):
    gbif_name = row[0]
    example_occurrence_image_url = row[10]
    fieldguide_id = fg_data[index][2]
    fieldguide_label = fg_data[index][3]
    cover_image_url = fg_data[index][5]
    cover_image_copyright = fg_data[index][6]
    common_name_en = fg_data[index][7]

    # Require exact match on the scientific name
    if gbif_name == fieldguide_label:
        row[2] = fieldguide_id
        row[3] = cover_image_url
        row[4] = cover_image_copyright
        row[8] = common_name_en

    # Use training data image as cover image fallback
    if len(row[3]) == 0:
        row[3] = example_occurrence_image_url

    updated_species_list.append(row)

# Write updated list to CSV
with open(csv_output, "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(updated_species_list)

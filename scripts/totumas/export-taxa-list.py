from slugify import slugify
import json
import os
import requests

# Input config
fetch_url = "https://ood.antenna.insectai.org/api/v2/taxa/?project_id=11&ordering=name&limit=20&offset=0&unknown_species=false&taxa_list_id=25&rank=SPECIES&include_unobserved=true"

# Output config
json_output = "output/taxa/taxa.json"
images_output = "output/taxa/images/"


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
                saved_images = save_images(taxon)
                taxa.append(
                    {
                        **taxon,
                        "saved_images": saved_images,
                    }
                )

        # Go to next page, if there is one
        if data["next"]:
            export_taxa(data["next"], page_count + 1, taxa)


def export_taxa_list():
    os.makedirs(images_output, exist_ok=True)
    taxa = []
    export_taxa(fetch_url, 1, taxa)

    with open(json_output, "w") as outfile:
        outfile.write(json.dumps(taxa, indent=4))


def save_image(image_url, filename):
    print("saving image ", filename)
    img_data = requests.get(image_url).content
    with open(images_output + filename, "wb") as handler:
        handler.write(img_data)
        return filename


# TODO: Save more images from this method when avaiblable from API
def save_images(taxon):
    slug = slugify(taxon["name"])

    # Save cover image
    cover_image_url = taxon["cover_image_url"]
    if cover_image_url:
        cover_image_filename = save_image(
            cover_image_url, "%s_%s_cover_image.jpg" % (slug, str(taxon["id"]))
        )
    else:
        cover_image_filename = None

    # Return all saved images
    return {"cover_image_filename": cover_image_filename}


export_taxa_list()

from PIL import Image
import os

# Input config
input_directory = "output/taxa/images/"

# Output config
image_max_width = 1024
output_directory = "output/taxa/images_resized"


os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(input_directory):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
        print("resizing image: ", filename)
        image_path = os.path.join(input_directory, filename)
        img = Image.open(image_path)

        if img.size[0] > image_max_width:
            width_percent = image_max_width / float(img.size[0])
            new_image_height = int((float(img.size[1]) * float(width_percent)))
            img = img.resize((image_max_width, new_image_height), Image.LANCZOS)

        if img.mode == "RGBA":
            img = img.convert("RGB")

        img.save(os.path.join(output_directory, filename))

print("images resized!")

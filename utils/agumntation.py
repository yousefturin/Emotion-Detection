from PIL import Image
import os
import numpy as np
from random import randint


def augment_and_save(
    image_path, output_folder, folder_name, image_number, zoom_factor=0.9
):
    try:
        # Open image
        img = Image.open(image_path)

        # Get image dimensions
        width, height = img.size

        # Calculate dimensions for square crop
        min_dim = min(width, height)
        zoomed_dim = min_dim * zoom_factor
        left = (width - zoomed_dim) / 2
        top = (height - zoomed_dim) / 2
        right = (width + zoomed_dim) / 2
        bottom = (height + zoomed_dim) / 2

        # Crop image
        img_cropped = img.crop((left, top, right, bottom))

        # Apply augmentation (rotation and zoom)
        # Random rotation
        angle = randint(-5, 5)
        img_augmented = img_cropped.rotate(angle, resample=Image.BICUBIC, expand=True)

        # Apply zoom
        # Calculate dimensions for zoomed crop
        width_zoomed, height_zoomed = img_augmented.size
        zoomed_width = width_zoomed * zoom_factor
        zoomed_height = height_zoomed * zoom_factor
        left_zoom = (width_zoomed - zoomed_width) / 2
        top_zoom = (height_zoomed - zoomed_height) / 2
        right_zoom = (width_zoomed + zoomed_width) / 2
        bottom_zoom = (height_zoomed + zoomed_height) / 2
        img_augmented = img_augmented.crop(
            (left_zoom, top_zoom, right_zoom, bottom_zoom)
        )
        # Extract original file extension
        _, ext = os.path.splitext(image_path)

        # Construct new filenames with original and augmented extensions
        original_filename = f"{folder_name}_{image_number}_original{ext}"
        augmented_filename = f"{folder_name}_{image_number}_augmented{ext}"

        # Create output directory structure if it doesn't exist
        output_path_original = os.path.join(
            output_folder, folder_name, original_filename
        )
        output_path_augmented = os.path.join(
            output_folder, folder_name, augmented_filename
        )
        os.makedirs(os.path.dirname(output_path_original), exist_ok=True)
        os.makedirs(os.path.dirname(output_path_augmented), exist_ok=True)

        # Save original and augmented images to output folder
        img_cropped.save(output_path_original)
        img_augmented.save(output_path_augmented)

        print(f"{output_path_original} processed successfully.")
        print(f"{output_path_augmented} processed successfully.")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")


def augment_images_in_folder(input_folder, output_folder):
    # Iterate through folders in input folder
    for root, dirs, files in os.walk(input_folder):
        for folder_name in dirs:
            folder_path = os.path.join(root, folder_name)
            image_number = 1
            # Iterate through files in folder
            for file in os.listdir(folder_path):
                if not file.startswith("."):
                    file_path = os.path.join(folder_path, file)
                    # Check if file is an image
                    if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                        try:
                            augment_and_save(
                                file_path, output_folder, folder_name, image_number
                            )
                            image_number += 1
                        except Exception as e:
                            print(f"Error processing {file_path}: {e}")


if __name__ == "__main__":
    input_folder = "dataSet"
    output_folder = "agumented_images"
    augment_images_in_folder(input_folder, output_folder)

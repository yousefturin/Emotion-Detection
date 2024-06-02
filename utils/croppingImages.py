from PIL import Image
import os

def crop_and_save(image_path, output_folder, folder_name, image_number, target_size=48, zoom_factor=0.7):
    try:
        # Open image
        img = Image.open(image_path)
        
        # Resize image to target size while maintaining aspect ratio
        img.thumbnail((target_size, target_size))
        
        # Get image dimensions after resizing
        width, height = img.size
        
        # Calculate dimensions for square crop with zoom
        min_dim = min(width, height)
        zoomed_dim = min_dim * zoom_factor
        left = (width - zoomed_dim) / 2
        top = (height - zoomed_dim) / 2
        right = (width + zoomed_dim) / 2
        bottom = (height + zoomed_dim) / 2
        
        # Crop image
        img_cropped = img.crop((left, top, right, bottom))
        
        # Resize cropped image to 128x128
        img_resized = img_cropped.resize((target_size, target_size))
        # Extract original file extension
        _, ext = os.path.splitext(image_path)
        
        # Construct new filename with original extension
        new_filename = f"{folder_name}_{image_number}{ext}"
        
        # Create output directory structure if it doesn't exist
        output_path = os.path.join(output_folder, folder_name, new_filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save cropped image to output folder with new filename
        img_resized.save(output_path)
        print(f"{output_path} processed successfully.")
        
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def crop_images_in_folder(input_folder, output_folder):
    # Iterate through folders in input folder
    for root, dirs, files in os.walk(input_folder):
        for folder_name in dirs:
            folder_path = os.path.join(root, folder_name)
            image_number = 1
            # Iterate through files in folder
            for file in os.listdir(folder_path):
                if not file.startswith('.'):
                    file_path = os.path.join(folder_path, file)
                    # Check if file is an image
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                        try:
                            crop_and_save(file_path, output_folder, folder_name, image_number)
                            image_number += 1
                        except Exception as e:
                            print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    input_folder = "100EachClass"
    output_folder = "100EachClassReal48"
    crop_images_in_folder(input_folder, output_folder)

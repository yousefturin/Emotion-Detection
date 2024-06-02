from PIL import Image
import os
import cv2

def crop_and_save(image_path, output_folder, folder_name, image_number, target_size=64):
    try:
        # Load image using OpenCV for face detection
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Load Haar cascade classifier for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # If faces are detected, crop and save them
        for i, (x, y, w, h) in enumerate(faces):
            # Calculate square bounding box around the face
            max_dim = max(w, h)
            center_x = x + w // 2
            center_y = y + h // 2
            half_size = max_dim // 2
            left = center_x - half_size
            top = center_y - half_size
            right = center_x + half_size
            bottom = center_y + half_size
            
            # Crop face region
            face_img = img[top:bottom, left:right]
            # Resize face image to target size
            face_img_resized = cv2.resize(face_img, (target_size, target_size))
            # Convert OpenCV image to PIL Image
            face_img_pil = Image.fromarray(cv2.cvtColor(face_img_resized, cv2.COLOR_RGB2GRAY))
            
            # Construct filename
            new_filename = f"{folder_name}_{image_number}_{i}.jpg"
            # Create output directory structure if it doesn't exist
            output_path = os.path.join(output_folder, folder_name, new_filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            # Save cropped face image to output folder
            face_img_pil.save(output_path)
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
    output_folder = "DatasetOFaces"
    crop_images_in_folder(input_folder, output_folder)

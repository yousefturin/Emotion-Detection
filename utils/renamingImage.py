import os

def rename_files_in_subdirectories(parent_dir):
    # Iterate through each subdirectory
    for subdir_name in os.listdir(parent_dir):
        subdir_path = os.path.join(parent_dir, subdir_name)
        # Check if the item is a directory
        if os.path.isdir(subdir_path):
            # Iterate through each file in the subdirectory
            files = os.listdir(subdir_path)
            for i, filename in enumerate(files):
                # Formulate the new filename
                new_filename = f"{i+1}_{subdir_name}" + os.path.splitext(filename)[1]
                # Check if the new filename already exists
                new_filepath = os.path.join(subdir_path, new_filename)
                if not os.path.exists(new_filepath):
                    # Rename the file
                    os.rename(os.path.join(subdir_path, filename), new_filepath)
                    print(f"Renamed {filename} to {new_filename}")
                    
if __name__ == "__main__":
    parent_directory_path = 'voiceEmotion'
    rename_files_in_subdirectories(parent_directory_path)
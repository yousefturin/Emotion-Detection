import os
import shutil

def split_data(source_dir, destination_dir):
    # Create destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Create 'Val' and 'Train' directories within the destination directory
    val_dir = os.path.join(destination_dir, "Val")
    train_dir = os.path.join(destination_dir, "Train")
    os.makedirs(val_dir)
    os.makedirs(train_dir)

    # Iterate through sub-directories in the source directory
    for subdir in os.listdir(source_dir):
        sub_source_dir = os.path.join(source_dir, subdir)

        # Create corresponding sub-directories in 'Val' and 'Train'
        sub_destination_dir_val = os.path.join(val_dir, subdir)
        sub_destination_dir_train = os.path.join(train_dir, subdir)
        os.makedirs(sub_destination_dir_val, exist_ok=True)
        os.makedirs(sub_destination_dir_train, exist_ok=True)

        # Get list of files in the sub-directory
        files = os.listdir(sub_source_dir)
        num_files = len(files)

        # Calculate number of files for validation (20%)
        num_files_val = int(0.2 * num_files)

        print(f"Sub-directory: {subdir}")
        print(f"Total files: {num_files}")

        # Copy 20% of the files to the 'Val' directory
        for file_name in files[:num_files_val]:
            source_file = os.path.join(sub_source_dir, file_name)
            destination_file = os.path.join(sub_destination_dir_val, file_name)
            print(f"Copying file {file_name} to Val directory")
            shutil.copy(source_file, destination_file)

        # Copy 80% of the files to the 'Train' directory
        for file_name in files[num_files_val:]:
            source_file = os.path.join(sub_source_dir, file_name)
            destination_file = os.path.join(sub_destination_dir_train, file_name)
            print(f"Copying file {file_name} to Train directory")
            shutil.copy(source_file, destination_file)


if __name__ == "__main__":
    source_directory = "DatasetOFaces"
    destination_directory = "DatasetOFacesSplit"
    split_data(source_directory, destination_directory)
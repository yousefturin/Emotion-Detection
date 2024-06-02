import os
import shutil

# Define the two parent directories to merge
parent_dir1 = 'voice_emotions1'
parent_dir2 = 'voice_emotions2'

# Define the target parent directory where everything will be merged
target_parent_dir = 'voiceEmotion'

# Ensure the target parent directory exists
os.makedirs(target_parent_dir, exist_ok=True)

# Function to merge files from a source directory into a target directory
def merge_directories(source_dir, target_dir):
    # Ensure the target subdirectory exists
    os.makedirs(target_dir, exist_ok=True)

    # Iterate through the files in the source directory
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.wav'):  # Only process .wav files
                # Source file path
                src_file_path = os.path.join(root, file)
                
                # Target file path
                dest_file_path = os.path.join(target_dir, file)
                
                # Move the file to the target directory
                shutil.copy(src_file_path, dest_file_path)
                print(f'Moved {src_file_path} to {dest_file_path}')

# Get the list of subdirectories in the first parent directory
subdirectories = [d for d in os.listdir(parent_dir1) if os.path.isdir(os.path.join(parent_dir1, d))]

# Merge the subdirectories and their contents from both parent directories into the target parent directory
for subdirectory in subdirectories:
    source_dir1 = os.path.join(parent_dir1, subdirectory)
    source_dir2 = os.path.join(parent_dir2, subdirectory)
    target_dir = os.path.join(target_parent_dir, subdirectory)
    
    # Merge files from the first source subdirectory
    if os.path.exists(source_dir1):
        merge_directories(source_dir1, target_dir)
    
    # Merge files from the second source subdirectory
    if os.path.exists(source_dir2):
        merge_directories(source_dir2, target_dir)

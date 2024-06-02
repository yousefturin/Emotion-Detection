import os
import shutil

# Base directory containing the files
base_dir = r'/Users/yusefturin/EmotionDetection/datasets/archive'

# Destination base directory where sorted files will be placed
dest_base_dir = 'voice_emotions'

# Ensure destination base directory exists
os.makedirs(dest_base_dir, exist_ok=True)

# Emotion labels based on the given convention
emotions = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

# Loop through each file in the base directory
for root, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.wav'):
            # Split the filename to get identifiers
            parts = file.split('-')
            
            # Check if the file matches the required modality and emotion
            if parts[0] == '03' and parts[1] == '01' and parts[2] in emotions:
                # Get the emotion directory name
                emotion_dir = emotions[parts[2]]
                
                # Create the emotion directory if it doesn't exist
                emotion_dir_path = os.path.join(dest_base_dir, emotion_dir)
                os.makedirs(emotion_dir_path, exist_ok=True)
                
                # Source and destination file paths
                src_file_path = os.path.join(root, file)
                dest_file_path = os.path.join(emotion_dir_path, file)
                
                # Move the file to the corresponding emotion directory
                shutil.copy(src_file_path, dest_file_path)
                
                print(f'Moved {src_file_path} to {dest_file_path}')   
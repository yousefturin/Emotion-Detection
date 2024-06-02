# Emotion Detection Application Using Python

**By student** : Yousef Rayyan

**Id**:1904010031

## Installation Instructions

### create environment and download requirements.txt

1. Open a terminal or command prompt.
2. Navigate to the directory where you want to create the Python environment.
3. Run the following command to create a virtual environment:

   `python3 -m venv env`

    This will create a new directory named "env" that contains the Python environment.

4. Activate the virtual environment by running the appropriate command based on your operating system:

    - For macOS/Linux:
  
        `source env/bin/activate`
    - For Windows:
  
        `.\env\Scripts\activate`

5. Once the virtual environment is activated, you should see "(env)" in your command prompt.
6. Now, you can install the dependencies listed in the requirements.txt file. run the following command:

   `pip install -r requirements.txt`

   This will install all the required packages specified in the requirements.txt file into your virtual environment.

### Dataset Installation

The dataset is stored on the cloud, to download the datasets, follow the steps:

1. Navigate to **datasets** Directory, in each sub-directory there is a **README.md** file that contain the url for the data set.
2. Navigate to each sub-directory and install the data.

> 💡 **Only School email will be allowed to access the dataset**.

### Models Installation

The models are stored on the cloud, due to file upload limitations, Please download the models from the README.md file that is located in **`./assets/models`**. or from [here](https://drive.google.com/drive/folders/1Re8a9kwVcoko2DN3PNo52hOrA9cf6Y9T?usp=drive_link)
> 💡 **Only School email will be allowed to access the Models.**

## Files Layout

The structure of the application as follow:

- assets
  - Models
    - model.h5 **(Best model for the face emotions)**
    - model72.h5 **(Best model for the voice emotions)**
  - Face Cascade
- datasets
  - DatasetImages7Classes **(This contains the dataset for 7 classes of faces, source Kaggel)**
    - train
    - validation
  - DatasetOFacesSplit **(This contains the dataset for 10 classes of faces, source self collected)**
    - Train
    - Val
  - DatasetVoiceEmotions **(This contains the dataset for 7 classes of voice, source Kaggel)**
- trainingData **(This contains the code files for training and processing the data with creating the models)**
  
  - trainFaceEmotions7Classes.ipynb **( The code for training the model of 7 classes of face emotions *-DatasetImages7Classes-*)**.(successful)
  - trainFaceEmotions10Classes.ipynb **( The code for training the model of 10 classes of face emotions *-DatasetOFacesSplit-*)**.(failed)
  - trainVoiceEmotions7Classes.ipynb **( The code for training the model of 7 classes of voice emotions *-DatasetVoiceEmotions-*)**.(unknown)
- utils **(This Directory contains different code files for processing the data, such augmentation, cropping the images, renaming the images, split the data, etc..)**
  
- FaceAndVoiceDetection **(This file is the actual program for this project that will detect the face and voice emotions)**
  
- FaceOnlyDetection **(This file is the program for only detecting the face emotions)**

> 💡 The report of the application is under **P1_YousefRayyan_1904010031_report.pages**

## About the Models

- **Face Model**: The images were processed as follow:
  - Data Processing:
  
    - all images were resized to (48,64,128) pixels to find the best output of each iteration.
    - Images were converted to black and white.
    - One iteration of modeling the data was processed to only crop the face of the un-cleaned dataset, then deep cleaning of data was performed to ensure the output image are clean and don't have wrong images in each class.
    - Data was split into 2 parts as (train, Validation).
  - Modeling:
  
    - Model was built using different approaches such using **Sequential Model**, then using only **CNN** nurals (layer).
    - Both approaches had the same building as **(Conv2D, BatchNormalization, Activation, MaxPooling, dropout, and flatten)**
    - All parameters were change and tested to find out the best setup for the model and the data such that changing **the learning rates, batch size, epochs, adding more patience to let the model train on more data but same time it might over fit, changing the Conv2D of each nurals(layer), increasing the Dropout of each nurals (layer), adding more pixels** and more other changes.
  - Training  Data:
  
    - The model was implement to ensure it does not over fit on the training, such data **(optimizer like Adam, and early stopping, reducing learning rate, and saving only best model out of all)**

- **Voice Model**: The waves were processed as follow:
  - Data Processing:

    - All files were split to extract labels from each path,
    then DataFrame was create to split the speech and labels.
    - Count and distribution of each class was analyzed, to ensure each class is correctly distributed.
    - Extracting feature is done using **librosa MFCC**, to convert the wav file into an array of data, then each array was reshaped into a correct form.
    - Data was spilt into train and validation.
  - Modeling:

    - The modeling process used is **Sequential** with adding **LSTM** **layer, dropouts, Dense**, and then convert it into the original 7 classes.
    - All parameters were change and tested to find out the best setup for the model and the data such that **changing the learning rates, batch size, epochs, adding more patience to let the model train on more data but same time it might over fit, changing the Dense of each nurals(layer), increasing the Dropout of each nurals (layer), adding more pixels** and more other changes.
  - Training:

    - The model was implement to ensure it does not over fit on the training, such data **(optimizer like Adam, and early stopping, reducing learning rate, and saving only best model out of all)**

## Running the application

- The application will run with default models which are **model.h5** and **model72.h5**, other model will not perform well.
- This application will not use any external sources such that APIs, it runs locally using tk UI and it is a window application.
- MacOS
  - If the application will be run on MacOS (M1,M2,M3) operating system then Python must be **3.10.11**.
    >
    > ⚠️ **Warning:** The application will only run on **v3.10.11**.
    >
- Windows  
  - If the application will be run on Windows operating system then Python must be **3.8.9**.
    >
    > ⚠️ **Warning:** The application will only run on **v3.8.9**.
    >
## 📝 Outcomes

The application is created only to detect 7 emotions, the 10 emotions was impossible to create due to the dataset, where dataset was impossible to find any Features that will then give the model an accuracy higher than 0.4. Different approaches where test such that:

- **Generating synthetic dataset using AI image models**.(This approach did fail because the generated data was not consisted, which will make feature extraction almost impossible).
- **Collecting data from stock image websites**.(This approach also fail because the images are not consistent, where some images of some categories will be similar to others and that made the model get best accuracy as 0.4)
- **Creating Model with 7 classes then add the left 3 classes**.(This approach did fail because the distribution of data labels across the model will not be the same and there is no way to collect data for the left 3 classes with a number of 5 thousand images peer class, which will make the model perform lower than it must be due to the lack of data on the remaining 3 classes).

For those issues the model was create only using Kaggel dataset that has 7 classes of emotions.

> 💡 The application model is not working correct for voice detection, even it did give 0.72 validation accuracy, but it will still give wrong and delayed output. Only face model is performing almost 100 correct and it detect only one face at the time.
>
> 🗣️ The output of the FaceAndVoiceDetection will be shown in the screen of the application as for the face output, where the voice will be shown in the **Terminal**.

> The application was made more than 10 time to do my best for creating the 10 emotion **but I was unsuccessful achieving this project**, and I have tried my best to give some sort of output for this project.

For more information you can check the source code [here](https://github.com/yousefturin/Emotion-Detection)

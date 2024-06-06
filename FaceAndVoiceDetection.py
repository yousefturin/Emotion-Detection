import cv2
import sounddevice as sd
import numpy as np
import librosa
from keras.models import load_model
from sklearn.preprocessing import OneHotEncoder
from keras.utils import img_to_array
from PIL import Image, ImageTk
import threading
import tkinter as tk
from keras.optimizers.legacy import Adam

class CreateApp:
    def __init__(self):
        # Paths to models
        self.AUDIO_MODEL_PATH = r'/Users/yusefturin/EmotionDetection/assets/models/model72.h5'
        self.FACE_MODEL_PATH = r'/Users/yusefturin/EmotionDetection/assets/models/model.h5'
        self.FACE_CASCADE_PATH = r"/Users/yusefturin/EmotionDetection/assets/haarcascade_frontalface_default.xml"

        # Emotion labels
        self.EMOTION_LABELS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

        # Load audio model and encoder
        self.audio_model = load_model(self.AUDIO_MODEL_PATH)
        # did not disable the warning
        self.audio_model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
        self.enc = OneHotEncoder()
        self.enc.fit(np.array(self.EMOTION_LABELS).reshape(-1, 1))


        # Load face model and cascade classifier
        self.face_classifier = cv2.CascadeClassifier(self.FACE_CASCADE_PATH)
        self.face_emotion_model = load_model(self.FACE_MODEL_PATH)
        # did not disable the warning
        self.face_emotion_model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

        # Flags for controlling threads
        self.recording = False
        self.running = False  # Initially set to False

        # Start video capture
        self.cap = cv2.VideoCapture(1) # Use 0 for built-in webcam on Windows and 1 for built-in webcam on Mac

        # Create Tkinter window
        self.root = tk.Tk()
        self.root.title("Emotion Detection App")
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)

        # Create video frame
        self.video_frame = tk.Label(self.root)
        self.video_frame.pack()

        # Create control frame
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack()

        # Create buttons
        self.start_button = tk.Button(self.control_frame, text="Start Video", command=self.start_video)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        self.stop_button = tk.Button(self.control_frame, text="Stop Video", command=self.stop_video)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)
        self.start_audio_button = tk.Button(self.control_frame, text="Start Audio", command=self.start_audio)
        self.start_audio_button.grid(row=0, column=2, padx=5, pady=5)
        self.stop_audio_button = tk.Button(self.control_frame, text="Stop Audio", command=self.stop_audio)
        self.stop_audio_button.grid(row=0, column=3, padx=5, pady=5)

        # Create label to display audio emotion prediction
        self.audio_label = tk.Label(self.root, text="Audio Emotion: None", font=("Helvetica", 16))
        self.audio_label.pack(pady=10)

        # Create label to display face emotion prediction
        self.face_label = tk.Label(self.root, text="Face Emotion: None", font=("Helvetica", 16))
        self.face_label.pack(pady=10)

        self.root.mainloop()

    def record_audio(self, duration=3, sr=22050):
        """Record audio and return it."""
        print("Recording...")
        audio = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='float32')
        sd.wait()  # Wait until recording is finished
        audio = audio.flatten()
        return audio, sr

    def start_audio(self):
        """Start audio recording and prediction in a loop."""
        if not self.recording:
            self.recording = True
            threading.Thread(target=self.predict_audio_emotion).start()

    def stop_audio(self):
        """Stop audio recording."""
        self.recording = False

    def extract_mfcc(self, audio, sr):
        """Extract MFCC features from audio."""
        mfcc = np.mean(librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40).T, axis=0)
        return mfcc

    def calculate_rms(self, audio):
        """Calculate the RMS energy of the audio signal."""
        return np.sqrt(np.mean(np.square(audio)))

    def predict_audio_emotion(self):
        """Predict emotion from audio data in a loop."""
        while self.recording:
            audio, sr = self.record_audio()
            rms = self.calculate_rms(audio)
            print(f"RMS energy: {rms}")

            # Set a threshold for RMS energy to detect significant sound
            rms_threshold = 0.01
            if rms > rms_threshold:
                print("Significant sound detected. Extracting features...")
                mfcc_features = self.extract_mfcc(audio, sr)
                mfcc_features = np.expand_dims(mfcc_features, axis=0)
                mfcc_features = np.expand_dims(mfcc_features, axis=-1)

                print("Making prediction...")
                prediction = self.audio_model.predict(mfcc_features, verbose=0)
                predicted_label = self.enc.inverse_transform(prediction)
                predicted_emotion = predicted_label[0][0]
                print(f"Predicted audio emotion: {predicted_emotion}")

                # Update the audio emotion label on the Tkinter screen
                self.audio_label.config(text=f"Audio Emotion: {predicted_emotion}")
            else:
                print("No significant sound detected. Skipping prediction.")

    def update_video(self):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                # Detect faces in the frame
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)

                # Process each detected face
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                    if np.sum([roi_gray]) != 0:
                        roi = roi_gray.astype("float") / 255.0
                        roi = img_to_array(roi)
                        roi = np.expand_dims(roi, axis=0)

                        prediction = self.face_emotion_model.predict(roi, verbose=0)[0]
                        label = self.EMOTION_LABELS[prediction.argmax()]
                        
                        # Update the face emotion label on the Tkinter screen
                        self.face_label.config(text=f"Face Emotion: {label}")
                    else:
                        cv2.putText(frame, "No Faces", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Display the video frame
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                self.video_frame.img = img
                self.video_frame.config(image=img)
            self.video_frame.after(10, self.update_video)

    def start_video(self):
        """Start video processing."""
        if not self.running:
            self.running = True
            self.update_video()

    def stop_video(self):
        """Stop video processing."""
        self.running = False

    def on_close(self):
        # Release the video capture object and close windows
        self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    # Create the application instance
    app = CreateApp()
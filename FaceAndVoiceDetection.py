import cv2
import sounddevice as sd
import numpy as np
import librosa
from keras.models import load_model
from sklearn.preprocessing import OneHotEncoder
from keras.utils import img_to_array
from PIL import Image, ImageTk
import threading
import queue
import tkinter as tk

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
        self.enc = OneHotEncoder()
        self.enc.fit(np.array(self.EMOTION_LABELS).reshape(-1, 1))

        # Load face model and cascade classifier
        self.face_classifier = cv2.CascadeClassifier(self.FACE_CASCADE_PATH)
        self.face_emotion_model = load_model(self.FACE_MODEL_PATH)

        # Queue to store audio data
        self.audio_queue = queue.Queue()

        # Flags for controlling threads
        self.recording = False
        self.running = True

        # Start video capture
        self.cap = cv2.VideoCapture(0)

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
        self.start_button = tk.Button(self.control_frame, text="Start", command=self.start)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        self.stop_button = tk.Button(self.control_frame, text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)
        self.start_audio_button = tk.Button(self.control_frame, text="Start Audio", command=self.start_audio)
        self.start_audio_button.grid(row=0, column=2, padx=5, pady=5)
        self.stop_audio_button = tk.Button(self.control_frame, text="Stop Audio", command=self.stop_audio)
        self.stop_audio_button.grid(row=0, column=3, padx=5, pady=5)

        self.update_video()

        self.root.mainloop()

    def record_audio(self, duration=3, sr=22050):
        """Record audio and store it in the queue."""
        while self.recording:
            print("Recording...")
            audio = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='float32')
            sd.wait()  # Wait until recording is finished
            audio = audio.flatten()
            self.audio_queue.put((audio, sr))

    def start_audio(self):
        """Start audio recording."""
        self.recording = True
        threading.Thread(target=self.record_audio).start()

    def stop_audio(self):
        """Stop audio recording."""
        self.recording = False

    def extract_mfcc(self, audio, sr):
        """Extract MFCC features from audio."""
        mfcc = np.mean(librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40).T, axis=0)
        return mfcc

    def predict_audio_emotion(self):
        """Predict emotion from audio data."""
        while self.running:
            if not self.audio_queue.empty():
                audio, sr = self.audio_queue.get()
                print("Extracting features...")
                mfcc_features = self.extract_mfcc(audio, sr)
                mfcc_features = np.expand_dims(mfcc_features, axis=0)
                mfcc_features = np.expand_dims(mfcc_features, axis=-1)

                print("Making prediction...")
                prediction = self.audio_model.predict(mfcc_features)
                predicted_label = self.enc.inverse_transform(prediction)
                print(f"Predicted audio emotion: {predicted_label[0][0]}")

    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            # Detect faces in the frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)

            # Process each detected face
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype("float") / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    prediction = self.face_emotion_model.predict(roi)[0]
                    label = self.EMOTION_LABELS[prediction.argmax()]
                    label_position = (x, y)
                    cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "No Faces", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display the video frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            self.video_frame.img = img
            self.video_frame.config(image=img)
        if self.running:
            self.video_frame.after(10, self.update_video)

    def start(self):
        """Start the application."""
        self.running = True

    def stop(self):
        """Stop the application."""
        self.running = False

    def on_close(self):
        # Release the video capture object and close windows
        self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    # Create the application instance
    app = CreateApp()

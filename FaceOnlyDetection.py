import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import cv2
import numpy as np
from keras.models import load_model
from keras.utils import img_to_array

class EmotionDetectorApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.video_source = 1  # Camera index (1 for default camera)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas to display the video feed
        self.canvas = tk.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Create Start and Stop buttons
        self.btn_start = tk.Button(window, text="Start Detection", width=20, command=self.start_video, bg="green", fg="black", font=('Helvetica', 12, 'bold'))
        self.btn_start.pack(anchor=tk.CENTER, expand=True)
        
        self.btn_stop = tk.Button(window, text="Stop Detection", width=20, command=self.stop_video, bg="red", fg="black", font=('Helvetica', 12, 'bold'))
        self.btn_stop.pack(anchor=tk.CENTER, expand=True)

        # Create a label to display the detected emotion
        self.label_text = tk.StringVar()
        self.label_text.set("Emotion: None")
        self.label = Label(window, textvariable=self.label_text, font=('Helvetica', 24), fg="white")
        self.label.pack(anchor=tk.CENTER, expand=True)

        # Load face detection and emotion recognition models
        self.face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.classifier = load_model(r"/Users/yusefturin/EmotionDetection/assets/models/model.h5")
        self.emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

        self.delay = 15  # Delay between frame updates (in milliseconds)
        self.running = False  # Flag to control video loop
        self.update()  # Start the update loop
        self.window.mainloop()  # Start the Tkinter main loop

    def start_video(self):
        """Start the video detection."""
        self.running = True

    def stop_video(self):
        """Stop the video detection."""
        self.running = False

    def update(self):
        """Update the video feed and perform emotion detection."""
        if self.running:
            ret, frame = self.vid.get_frame()

            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_classifier.detectMultiScale(gray)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                    if np.sum([roi_gray]) != 0:
                        roi = roi_gray.astype("float") / 255.0
                        roi = img_to_array(roi)
                        roi = np.expand_dims(roi, axis=0)

                        prediction = self.classifier.predict(roi)[0]
                        label = self.emotion_labels[prediction.argmax()]
                        self.label_text.set(f"Emotion: {label}")
                    else:
                        self.label_text.set("Emotion: None")

                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

class MyVideoCapture:
    def __init__(self, video_source=0):
        """Initialize the video capture object."""
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        """Get a single frame from the video source."""
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (None, None)

    def __del__(self):
        """Release the video capture object."""
        if self.vid.isOpened():
            self.vid.release()

if __name__ == "__main__":
    EmotionDetectorApp(tk.Tk(), "Emotion Detector")

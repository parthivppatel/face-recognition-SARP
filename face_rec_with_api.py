import face_recognition
import os, sys
import cv2
import numpy as np
import math
import subprocess
import os, sys
from face_data_api import send_api_request, get_latest_timestamp
from dotenv import load_dotenv
from datetime import datetime


# Loding environment variables
load_dotenv()
time_interval = int(os.getenv("TIME_INTERVAL"))

# Name and ID mapping
name_and_id = {"sarma": 1, "abhi": 2, "ravin": 3, "parthiv": 4}


# Helper function
def face_confidence(face_distance, face_match_threshold=0.6):
    range = 1.0 - face_match_threshold
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + "%"
    else:
        value = (
            linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))
        ) * 100
        return str(round(value, 2)) + "%"


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir("faces"):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names)

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit("Video source not found...")

        while True:
            ret, frame = video_capture.read()

            # Only process every other frame of video to save time
            if self.process_current_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, self.face_locations
                )

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(
                        self.known_face_encodings, face_encoding
                    )
                    name = "Unknown"
                    confidence = "???"

                    # Calculate the shortest distance to face
                    face_distances = face_recognition.face_distance(
                        self.known_face_encodings, face_encoding
                    )

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        name = name.split(".")[0].lower()
                        confidence = face_confidence(face_distances[best_match_index])
                        if name in name_and_id:
                            id = name_and_id[name]

                        device_id = subprocess.check_output("hostname").decode().strip()
                        current_time_stamp = datetime.now()
                        prev_time_stamp = get_latest_timestamp(device_id, id)
                        if prev_time_stamp:
                            try:
                                prev_time_stamp = datetime.fromisoformat(
                                    prev_time_stamp
                                ).strftime("%H:%M:%S")
                                str_time = datetime.strptime(
                                    prev_time_stamp, "%H:%M:%S"
                                ).time()
                                actual_time = datetime.combine(
                                    datetime.today().date(), str_time
                                )
                                time_diff = int(
                                    (current_time_stamp - actual_time).total_seconds()
                                )

                                if time_interval * 60 > time_diff:
                                    sys.exit()

                            except Exception as e:
                                print(f"Error: {str(e)}")

                        api_response = send_api_request(device_id, id)
                        if api_response:
                            video_capture.release()
                            cv2.destroyAllWindows()
                            sys.exit()

                    self.face_names.append(f"{name} ({confidence})")

            self.process_current_frame = not self.process_current_frame

            # Display the results
            for (top, right, bottom, left), name in zip(
                self.face_locations, self.face_names
            ):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Create the frame with the name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(
                    frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
                )
                cv2.putText(
                    frame,
                    name.capitalize(),
                    (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.8,
                    (255, 255, 255),
                    1,
                )

            # Display the resulting image
            cv2.imshow("Face Recognition", frame)

            # Hit 'ESC' on the keyboard to quit!
            k = cv2.waitKey(10) & 0xFF  # Press 'ESC' for exiting video
            if k == 27:
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    fr = FaceRecognition()
    fr.run_recognition()

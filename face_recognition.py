import cv2
from face_data_api import send_api_request, get_latest_timestamp
import subprocess
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

time_interval = int(os.getenv("TIME_INTERVAL"))
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/trainer.yml")
cascadePath = "cascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

# iniciate id counter
id = 0

# API call status
api_call = False

# names related to ids: example ==> Marcelo: id=1,  etc
names = ["None", "Sarma", "Abhi", "Ravin", "Parthiv"]

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video widht
cam.set(4, 480)  # set video height

# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)
while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y : y + h, x : x + w])

        # If confidence is less than 100 ==> "0" : perfect match
        if confidence < 50:
            user_name = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
            device_id = subprocess.check_output("hostname").decode().strip()
            current_time_stamp = datetime.now()
            prev_time_stamp = get_latest_timestamp(id)
            print(prev_time_stamp)
            # time_diff = int((current_time_stamp - prev_time_stamp).total_seconds())
            # api_call = time_interval * 60 > time_diff

            if not api_call:
                api_response = send_api_request(device_id, id)
                api_call = True

        else:
            user_name = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(img, user_name, (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    cv2.imshow("camera", img)
    k = cv2.waitKey(10) & 0xFF  # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()

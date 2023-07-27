import cv2
import dlib

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/trainer.yml")

# Initialize dlib face detector
face_detector = dlib.get_frontal_face_detector()

font = cv2.FONT_HERSHEY_SIMPLEX

# Names related to ids: example ==> John: id=1,  etc
names = ["None", "Sarma", "Abhi", "Ravin", "Parthiv"]

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces using the dlib detector
    faces = face_detector(gray)

    for face in faces:
        # Convert dlib rectangle to OpenCV rectangle format
        x, y, w, h = face.left(), face.top(), face.width(), face.height()

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y : y + h, x : x + w])

        # Face match basis the confidence level
        if confidence < 60:
            user_name = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
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

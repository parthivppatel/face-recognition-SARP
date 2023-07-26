import cv2
import numpy as np
from PIL import Image
import os
import dlib

# Path for face image database
path = "dataset"
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Initialize dlib face detector
face_detector = dlib.get_frontal_face_detector()


# function to get the images and label data
def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for image_path in image_paths:
        PIL_img = Image.open(image_path).convert("L")  # grayscale
        img_numpy = np.array(PIL_img, "uint8")

        # Extract user_id from the image filename
        filename = os.path.basename(image_path)
        user_id = int(filename.split(".")[0])

        # Detect faces using the dlib detector
        faces = face_detector(img_numpy)

        for face in faces:
            # Convert dlib rectangle to OpenCV rectangle format
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            faceSamples.append(img_numpy[y : y + h, x : x + w])
            ids.append(user_id)

    return faceSamples, ids


print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces, ids = get_images_and_labels(path)
recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
recognizer.write("trainer/trainer.yml")

# Print the number of faces trained and end the program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))

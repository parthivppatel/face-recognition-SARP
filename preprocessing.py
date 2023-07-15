import dlib
import cv2
import os


def preprocess_images(input_folder, output_folder):
    detector = dlib.get_frontal_face_detector()
    predictor_path = "shape_predictor_68_face_landmarks.dat"
    predictor = dlib.shape_predictor(predictor_path)

    target_size = (224, 224)

    for filename in os.listdir(input_folder):
        image_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        if os.path.isfile(image_path):
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = detector(gray)
            for face in faces:
                landmarks = predictor(gray, face)
                aligned_face = dlib.get_face_chip(image, landmarks)

            resized_face = cv2.resize(aligned_face, target_size)

            cv2.imwrite(output_path, resized_face)


# Usage:
input_folder = "input_images"
output_folder = "processed_images"
preprocess_images(input_folder, output_folder)

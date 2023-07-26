import cv2
import os
import dlib


# Function to capture and save face images
def capture_faces(user_id, max_samples=50):
    cam = cv2.VideoCapture(0)

    # Initialize dlib face detector
    face_detector = dlib.get_frontal_face_detector()

    dataset_directory = "dataset"
    if not os.path.exists(dataset_directory):
        os.makedirs(dataset_directory)

    print("\n [INFO] Initializing face capture. Look at the camera and wait ...")

    # Initialize individual sampling face count
    count = 0
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces using the dlib detector
        faces = face_detector(gray)

        for face in faces:
            # Convert dlib rectangle to OpenCV rectangle format
            x, y, w, h = face.left(), face.top(), face.width(), face.height()

            # Save the captured image into the dataset directory
            face_image_path = os.path.join(dataset_directory, f"{user_id}.{count}.jpg")
            cv2.imwrite(face_image_path, gray[y : y + h, x : x + w])

            count += 1
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("image", img)

        # Press 'ESC' for exiting video or reach the desired number of face samples
        if cv2.waitKey(100) & 0xFF == 27 or count >= max_samples:
            break

    # Do a bit of cleanup
    print(f"\n [INFO] Captured {count} face samples for user {user_id}.")
    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # For each person, enter one numeric face id
    face_id = input("\n Enter user id and press <return> ==> ")

    try:
        face_id = int(face_id)
        capture_faces(face_id)
    except ValueError:
        print("\n [ERROR] Invalid user ID. Please enter a numeric ID.")

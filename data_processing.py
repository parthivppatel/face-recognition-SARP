import cv2


def capture_images(person_name, num_images):
    camera = cv2.VideoCapture(0)  # Open the camera

    image_count = 0

    while True:
        ret, frame = camera.read()  # Capture a frame from the camera
        cv2.imshow("Capture", frame)  # Show the frame

        key = cv2.waitKey(1) & 0xFF

        if key == ord("c"):
            cv2.imwrite(f"{person_name}_{image_count}.jpg", frame)  # Save the image
            image_count += 1
            print(f"Image {image_count}/{num_images} captured.")

        if key == ord("q") or image_count == num_images:
            break

    camera.release()  # Release the camera
    cv2.destroyAllWindows()  # Close all windows


# Usage:
capture_images("Abhi", 10)

# face-recognition-SARP

An application that will recognize "face" and fire an API to the backend with 3 parameters - Device ID, Recognized FaceID, Datetime stamp (UTC / GMT)

> **Note:** Windows OS users to use "python" and "pip" and MAC OS users to use "python3" and "pip3"

## PREREQUISITES

1. Create a virtual enviroment and activate it

   ```python
   python -m venv .venv

   # Windows
   source .venv/scripts/activate

   # Mac
   source .venv/bin/activate
   ```

2. Install required modules

   ```python
   pip install -r requirements.txt
   ```

## CORE PROCESS

1. Capture the required person face images as part of data processing activity

   ```python
   python face_data_capture.py
   ```

2. Train the model using the newly captured images

   ```python
   python face_data_training.py
   ```

3. Main script to identify the person and show their name (if identified)
   ```python
   python face_recognition.py
   ```

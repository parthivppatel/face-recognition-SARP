# face-recognition-SARP 🤖

An application that will recognize "face" and fire an API to the backend with 3 parameters - Device ID, Recognized FaceID, Datetime stamp (UTC / GMT)

> **Note:** Windows OS users to use "python" and "pip" and MAC OS users to use "python3" and "pip3"

## PREREQUISITES ✅

1. Create a virtual enviroment and activate it

   ```python
   python -m venv .venv

   # Windows 🪟
   source .venv/scripts/activate

   # Mac 💻
   source .venv/bin/activate
   ```

2. Install required modules

   ```python
   # Windows 🪟
   pip install -r requirements_win.txt

   # Mac 💻
   pip install -r requirements_mac.txt
   ```

## APP INSTANTIATION 🚀

1. Run the FASTAPI APP instance

   ```python
   # Recommended
   uvicorn app.main:app --reload --host 0.0.0.0 --port 5000

   # host and port are optional, if omitted port will default to 8000
   uvicorn app.main:app --reload
   ```

2. Ensure localhost connectivity (port - 3306), then run the below to perform migration(s)

   ```python
   alembic upgrade head
   ```

## CORE PROCESS 📲

1. Capture the required person face image and place them inside the folder "**faces**""

2. Main script to identify the person and fire the respective API calls (if face identified)

   ```python
   python face_rec_with_api.py
   ```

3. To skip firing the API calls and just test the face recognition functionality

   ```python
   python face_rec_without_api.py
   ```

import requests

api_url_post = "http://localhost:8000/face-data"
api_url_get = "http://localhost:8000/get-time-stamp"
headers = {"Content-Type": "application/json"}


def send_api_request(device_id, face_id):
    data = {"device_id": device_id, "face_id": face_id}

    try:
        response = requests.post(api_url_post, json=data, headers=headers)
        response.raise_for_status()  # Check for any HTTP errors
        print("Face capture details posted successfully.")
    except requests.exceptions.RequestException as e:
        print("Error sending API Request:", str(e))

    return response


def get_latest_timestamp(device_id, face_id):
    data = {"device_id": device_id, "face_id": face_id}
    try:
        response = requests.post(api_url_get, json=data, headers=headers)
        response.raise_for_status()  # Check for any HTTP errors
        print("Latest timestamp extracted successfully.")
    except requests.exceptions.RequestException as e:
        print("Error sending API Request:", str(e))

    return response.text


if __name__ == "__main__":
    pass

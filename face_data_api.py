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
        return response
    except requests.exceptions.RequestException as e:
        print("Error sending API Request:", str(e))

    return None


def get_latest_timestamp(device_id, face_id):
    data = {"device_id": device_id, "face_id": face_id}
    try:
        response = requests.post(api_url_get, json=data, headers=headers)
        response.raise_for_status()  # Check for any HTTP errors
        print("Latest timestamp extracted successfully.")

        try:
            json_data = response.json()
            timestamp = json_data.get("timestamp")
            return timestamp
        except ValueError:
            print("Error: Invalid JSON response from the API.")
            return None

    except requests.exceptions.RequestException as e:
        print("Error sending API Request:", str(e))

    return None


if __name__ == "__main__":
    pass

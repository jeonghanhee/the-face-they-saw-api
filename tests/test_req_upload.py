import time
import hashlib
import requests
import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read("test.ini")

BASE_URL = config["server"]["base_url"]
SIGN_SECRET = config["x_header"]["sign_secret"]
GAME_KEY = config["x_header"]["game_key"]
CLIENT_ID = config["x_header"]["client_id"]


def make_headers():
    timestamp = int(time.time())
    raw = f"{SIGN_SECRET}{timestamp}"
    signature = hashlib.sha256(raw.encode()).hexdigest()

    return {
        "X-Game-Key": GAME_KEY,
        "X-Timestamp": str(timestamp),
        "X-Signature": signature,
        "X-Language": "ko",
    }


def test():
    headers = make_headers()

    payload = {
        "client_id": CLIENT_ID
    }

    image_path = Path(__file__).parent / "samples" / "round_face_shape_sample.jpeg"

    with open(image_path, "rb") as f:
        files = {
            "file": ("round_face_shape_sample.jpeg", f, "image/jpeg")
        }

        response = requests.post(
            f"{BASE_URL}/api/upload",
            data=payload,
            files=files,
            headers=headers
        )

    print("status:", response.status_code)
    print("response:", response.json())
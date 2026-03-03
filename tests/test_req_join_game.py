import time
import hashlib
import requests
import configparser

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
        "Content-Type": "application/json",
    }

def test():
    headers = make_headers()
    payload = {
        "client_id": CLIENT_ID
    }

    response = requests.post(
        f"{BASE_URL}/join_game",
        json=payload,
        headers=headers,
        timeout=5,
    )

    print("status:", response.status_code)
    print("response:", response.json())

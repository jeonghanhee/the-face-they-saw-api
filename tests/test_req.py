import time
import hashlib
import requests

BASE_URL = "http://127.0.0.1:8000"
GAME_KEY = "tfts-game-key-v1"
SIGN_SECRET = "tfts-sign-secret"

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

def send_join(client_id: str):
    headers = make_headers()
    payload = {
        "client_id": client_id
    }

    response = requests.post(
        f"{BASE_URL}/join_game",
        json=payload,
        headers=headers,
        timeout=5,
    )

    print("STATUS :", response.status_code)
    print("RESPONSE:", response.json())

if __name__ == "__main__":
    send_join("test-client-001")
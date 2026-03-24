import os, time, hashlib
from fastapi import Header, HTTPException, Depends
from dotenv import load_dotenv

load_dotenv()

GAME_KEY = os.getenv("GAME_KEY")
SIGN_SECRET = os.getenv("SIGN_SECRET")

def verify_game_key(x_game_key: str = Header(...)):
    if x_game_key != GAME_KEY:
        raise HTTPException(401, "Invalid Game Key")

def verify_signature(x_signature: str = Header(...),x_timestamp: int = Header(...)):
    now = int(time.time())
    if abs(now - x_timestamp) > 30:
        raise HTTPException(401, "Expired Request")

    raw = f"{SIGN_SECRET}{x_timestamp}"
    expected = hashlib.sha256(raw.encode()).hexdigest()

    if x_signature != expected:
        raise HTTPException(401, "Invalid Signature")

def secure_gate(game_key: str = Depends(verify_game_key),  signature: str = Depends(verify_signature)):
    return True
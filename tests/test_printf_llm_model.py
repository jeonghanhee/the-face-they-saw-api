import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.llm.gemini_client import client

for model in client.models.list():
    print(model.name)
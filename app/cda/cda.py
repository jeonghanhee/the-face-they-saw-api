import asyncio
from typing import Optional, List
from app.cda.client import Client

class CDA:
    def __init__(self):
        self._clients: dict[str, Client] = {}
        self._lock = asyncio.Lock()

    async def get_client(self, client_id: str) -> Optional[Client]:
        async with self._lock:
            return self._clients.get(client_id)

    async def add_client(self, client_id: str) -> bool:
        async with self._lock:
            if client_id in self._clients:
                return False
            self._clients[client_id] = Client(client_id)
            return True

    async def remove_client(self, client_id: str) -> bool:
        async with self._lock:
            return self._clients.pop(client_id, None) is not None

    async def clients(self) -> List[Client]:
        async with self._lock:
            return list(self._clients.values())
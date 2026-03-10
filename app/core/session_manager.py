import asyncio
from typing import Optional, List, Dict
from dataclasses import dataclass
from app.models import Scenario

@dataclass
class UserSession:
    id: str
    scenario: Optional[Scenario] = None

    def set_scenario(self, scenario: Scenario):
        self.scenario = scenario
    
    def clear(self):
        self.scenario = None

class SessionManager:
    def __init__(self):
        self._sessions: Dict[str, UserSession] = {}
        self._lock = asyncio.Lock()

    async def get_session(self, client_id: str) -> Optional[UserSession]:
        return self._sessions.get(client_id)

    async def add_session(self, client_id: str) -> bool:
        async with self._lock:
            if client_id in self._sessions:
                return False
            self._sessions[client_id] = UserSession(id=client_id)
            return True

    async def remove_session(self, client_id: str) -> bool:
        async with self._lock:
            return self._sessions.pop(client_id, None) is not None

    async def get_all_sessions(self) -> List[UserSession]:
        return list(self._sessions.values())
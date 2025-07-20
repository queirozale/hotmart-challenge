from typing import Dict


class Database:
    def _init_(self, credentials: Dict[str, str] = {}):
        self.credentials = credentials
        self.client = None

    def _auth(self):
        pass

    def get_user_revenue(user_id: 34) -> float:
        return 1000000

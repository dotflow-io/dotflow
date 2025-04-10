"""ServerDefault"""

from uuid import UUID

from httpx import Client

from dotflow.core.context import Context


class ServerDefault:
    """ServerDefault"""

    SERVER_STATUS = False
    SERVER_HOST = "http://127.0.0.1:8000"

    def __init__(self, token: str = None, host: str = None):
        self.client = Client(
            base_url=host or self.SERVER_HOST,
            headers={"Authorization": token or "key"}
        )
        self.ping()

    def ping(self) -> bool:
        try:
            self.client.get("/ping")
            self.SERVER_STATUS = True
            print("Connected.")
        except Exception:
            pass

        return True

    def create_task(self, id: int) -> None:
        if self.SERVER_STATUS:
            self.client.post("/tasks/")
        return None

    def create_workflow(self, id: UUID) -> None:
        if self.SERVER_STATUS:
            self.client.post("/workflows/")
        return None

    def create_context(self, context: Context) -> None:
        if self.SERVER_STATUS:
            self.client.post("/contexts/")
        return None

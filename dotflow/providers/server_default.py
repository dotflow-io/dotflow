"""ServerDefault"""

from uuid import UUID
from http import HTTPStatus

from httpx import Client

from dotflow.core.context import Context
from dotflow.logging import logger


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

    def ping(self) -> None:
        try:
            response = self.client.get("/ping")
            if response.status_code == HTTPStatus.OK:
                self.SERVER_STATUS = True

        except Exception:
            pass
        return None

    def create_task(self, id: int) -> None:
        if self.SERVER_STATUS:
            try:
                self.client.post("/v1/tasks")
            except Exception as err:
                logger.error(f"Internal problem: {str(err)}")
        return None

    def create_workflow(self, id: UUID) -> None:
        if self.SERVER_STATUS:
            try:
                self.client.post("/v1/workflows")
            except Exception as err:
                logger.error(f"Internal problem: {str(err)}")
        return None

    def create_context(self, context: Context) -> None:
        if self.SERVER_STATUS:
            self.client.post("/v1/contexts")
        return None

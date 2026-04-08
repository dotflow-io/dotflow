"""Deploy ABCs."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Registry(ABC):
    """Base class for container registries (ECR, Artifact Registry, Docker Hub, etc.)."""

    @abstractmethod
    def push(self, name: str) -> str:
        """Build and push the Docker image. Returns the image URI."""

    @abstractmethod
    def login(self) -> None:
        """Authenticate with the registry."""


class RoleManager(ABC):
    """Base class for IAM/service account management."""

    @abstractmethod
    def ensure_role(self, name: str, service: str, policy: str) -> str:
        """Create or get a role for the given service. Returns the role ARN/ID."""


class LogManager(ABC):
    """Base class for log group/resource management."""

    @abstractmethod
    def ensure_log_group(self, name: str) -> None:
        """Create log group if it doesn't exist."""


class ObjectStorage(ABC):
    """Base class for object storage (S3, GCS, Azure Blob, etc.)."""

    @abstractmethod
    def read(self, key: str) -> list:
        """Read data from a key. Returns empty list if not found."""

    @abstractmethod
    def write(self, key: str, data: list) -> None:
        """Write data to a key."""


class Queue(ABC):
    """Base class for message queues (SQS, Pub/Sub, Azure Queue, etc.)."""

    @abstractmethod
    def create(self, name: str) -> str:
        """Create queue. Returns queue URL/ID."""

    @abstractmethod
    def get_arn(self, name: str) -> str:
        """Get queue ARN/ID."""


class EventScheduler(ABC):
    """Base class for event schedulers (EventBridge, Cloud Scheduler, etc.)."""

    @abstractmethod
    def create_schedule(
        self, name: str, expression: str, target_arn: str
    ) -> None:
        """Create a scheduled rule targeting a resource."""


class Deployer(ABC):
    """Base class for all cloud deployers."""

    @abstractmethod
    def deploy(self, name: str, **kwargs) -> None:
        """Deploy the pipeline to the target platform."""

    def setup(self, name: str) -> None:
        """Create required cloud resources (roles, log groups, etc.).

        Optional — override when the platform needs pre-deploy setup.
        No-op by default.
        """

    def teardown(self, name: str) -> None:
        """Remove cloud resources created by deploy.

        Optional — override when the platform supports cleanup.
        No-op by default.
        """

import sys
from unittest.mock import MagicMock

sys.modules.setdefault("cookiecutter", MagicMock())
sys.modules.setdefault("cookiecutter.main", MagicMock())

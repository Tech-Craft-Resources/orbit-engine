from collections.abc import Generator
from typing import Any
from unittest.mock import MagicMock

import pytest


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Any, None, None]:
    # Overrides the parent conftest db fixture so script tests run without a real DB.
    yield MagicMock()

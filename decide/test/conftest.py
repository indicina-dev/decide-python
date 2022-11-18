from typing import Any

import pytest as pytest


@pytest.fixture(scope="session", autouse=True)
def before_all(request: Any) -> None:
	"""test setup"""

	print("Testing Decide...")
	request.addfinalizer(after_all)


def after_all() -> None:
	...

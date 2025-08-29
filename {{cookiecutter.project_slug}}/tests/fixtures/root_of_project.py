from pathlib import Path

import pytest


@pytest.fixture()
def root_of_project():
    return Path(__file__).parent.parent.parent
import sys

import pytest


@pytest.fixture
def clean_modules():
    """Cleans modules after each test"""
    modules_to_clean = [
        'common.constants.paths',
        'common.constants.environment'
    ]

    def cleanup():
        for module in modules_to_clean:
            if module in sys.modules:
                del sys.modules[module]

    cleanup()  # Clean up before the test
    yield
    cleanup()  # Clean up after the test
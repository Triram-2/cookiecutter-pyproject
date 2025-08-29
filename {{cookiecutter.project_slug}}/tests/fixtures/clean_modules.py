import sys

import pytest


@pytest.fixture
def clean_modules():
    """Очищает модули после каждого теста"""
    modules_to_clean = [
        'common.constants.paths',
        'common.constants.environment'
    ]

    def cleanup():
        for module in modules_to_clean:
            if module in sys.modules:
                del sys.modules[module]

    cleanup()  # Очищаем перед тестом
    yield
    cleanup()  # Очищаем после теста
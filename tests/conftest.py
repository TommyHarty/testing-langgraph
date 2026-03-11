import os
import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "integration: real external API test")


@pytest.fixture
def require_openai_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        pytest.skip("OPENAI_API_KEY not set")
    return key
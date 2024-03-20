import pytest

from src.aggregator.auth_credentials import access_token, token_type


@pytest.fixture()
def vendor():
    return "Vendor A"


@pytest.fixture()
def get_headers():
    return {'Authorization': f'{token_type}  {access_token}'}

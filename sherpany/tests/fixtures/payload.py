from datetime import datetime, timedelta

import pytest
from django.utils import timezone


@pytest.fixture
def login_payload():
    return {"username": "test_a@test.com", "password": "test1234"}


@pytest.fixture
def register_payload():
    return {
        "email": "test@test.com",
        "password1": "test1234!@",
        "password2": "test1234!@",
    }


@pytest.fixture
def create_event_payload():
    return {
        "title": "Test",
        "description": "Test",
        "start_at": datetime.strftime(timezone.now() + timedelta(days=1), "%Y-%m-%d"),
    }

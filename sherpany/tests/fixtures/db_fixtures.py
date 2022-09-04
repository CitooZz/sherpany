from datetime import timedelta

import pytest
from django.test import Client
from django.utils import timezone

from accounts.models import User
from events.models import Event, EventRSVP


@pytest.fixture(autouse=True)
def user_a():
    """Initialize test user."""
    return User.objects.create_user(
        "test_a@test.com",
        "test1234",
    )


@pytest.fixture(autouse=True)
def user_b():
    """Initialize test user."""
    return User.objects.create_user(
        "test_b@test.com",
        "test1234",
    )


@pytest.fixture
def client():
    """Initialize test client."""
    return Client()


@pytest.fixture
def event(user_a):
    return Event.objects.create(
        title="test",
        description="description",
        start_at=timezone.now() + timedelta(days=1),
        creator=user_a,
    )


@pytest.fixture
def event_rsvp(event, user_b):
    return EventRSVP.objects.create(event=event, user=user_b)


@pytest.fixture
def setup_multiple_events(user_a):
    for i in range(15):
        Event.objects.create(
            title=f"test {i}",
            description="description",
            start_at=timezone.now(),
            creator=user_a,
        )

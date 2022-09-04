import pytest
from django.urls import reverse


@pytest.fixture
def login_url():
    return reverse("accounts:login")


@pytest.fixture
def register_url():
    return reverse("accounts:register")


@pytest.fixture
def create_event_url():
    return reverse("events:create_event")


@pytest.fixture
def detail_event_url(event):
    return reverse(
        "events:detail_event",
        kwargs={"pk": event.id},
    )


@pytest.fixture
def delete_event_url(event):
    return reverse(
        "events:delete_event",
        kwargs={"pk": event.id},
    )


@pytest.fixture
def update_event_url(event):
    return reverse(
        "events:update_event",
        kwargs={"pk": event.id},
    )


@pytest.fixture
def reserve_event_url(event):
    return reverse(
        "events:reserve_event",
        kwargs={"pk": event.id},
    )


@pytest.fixture
def withdraw_event_url(event):
    return reverse(
        "events:withdraw_event_reservation",
        kwargs={
            "pk": event.id,
        },
    )


@pytest.fixture
def my_events_url(setup_multiple_events):
    return reverse(
        "events:my_events",
    )


@pytest.fixture
def public_events_url(setup_multiple_events):
    return reverse(
        "events:public_events",
    )

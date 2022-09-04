import pytest


@pytest.fixture
def login_error_content():
    return "Incorrect email or password. Please try again."


@pytest.fixture
def create_event_success_content():
    return "Event has been saved"


@pytest.fixture
def delete_event_success_content():
    return "Event has been deleted"


@pytest.fixture
def rsvp_success_content():
    return "You have successfully reserved to the event"


@pytest.fixture
def rsvp_error_passed_event_content():
    return "You can&#x27;t do reservation to passed event."


@pytest.fixture
def rsvp_error_owner_event_content():
    return "You can&#x27;t do reservation to your own event."


@pytest.fixture
def rsvp_already_reserved_event_content():
    return "You already reserved this event."


@pytest.fixture
def withdraw_rsvp_success_content():
    return "You have successfully withdraw reservation to the event"

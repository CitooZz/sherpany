from datetime import datetime
from http import HTTPStatus

import pytest
from django.urls import reverse

from events.models import Event


@pytest.mark.django_db
def test_update_event_success(
    client,
    user_a,
    update_event_url,
    create_event_payload,
    create_event_success_content,
):
    client.force_login(user_a)
    response = client.post(update_event_url, create_event_payload, follow=True)
    assert response.status_code == HTTPStatus.OK
    assert create_event_success_content in str(response.content)

    event = Event.objects.get(id=1)
    for field, value in create_event_payload.items():
        if field == "start_at":
            value = datetime.strptime(value, "%Y-%m-%d").date()

        assert getattr(event, field) == value


@pytest.mark.parametrize(
    "field, value, expected_error",
    [
        ("title", "", "This field is required."),
        ("description", "", "This field is required."),
        ("start_at", "2000-2-22", "Start at must greater than today."),
    ],
)
@pytest.mark.django_db
def test_update_event_failed(
    client,
    user_a,
    update_event_url,
    create_event_payload,
    field,
    value,
    expected_error,
):
    create_event_payload[field] = value
    client.force_login(user_a)
    response = client.post(update_event_url, create_event_payload)
    assert expected_error in str(response.content)


@pytest.mark.django_db
def test_update_other_user_event(
    client,
    user_b,
    update_event_url,
    create_event_payload,
):
    client.force_login(user_b)
    response = client.post(update_event_url, create_event_payload)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_update_event_not_found(
    client,
    user_a,
):
    client.force_login(user_a)
    response = client.delete(reverse("events:delete_event", kwargs={"pk": 12}))
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_update_event_unauthorized(
    client,
    update_event_url,
    create_event_payload,
):
    response = client.post(update_event_url, create_event_payload)
    # Should be redirect to login url
    assert reverse("accounts:login") in response["Location"]

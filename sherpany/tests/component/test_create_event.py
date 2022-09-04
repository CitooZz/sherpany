from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_event_success(
    client,
    user_a,
    create_event_url,
    create_event_payload,
    create_event_success_content,
):
    client.force_login(user_a)
    response = client.post(create_event_url, create_event_payload, follow=True)
    assert response.status_code == HTTPStatus.OK
    assert create_event_success_content in str(response.content)


@pytest.mark.parametrize(
    "field, value, expected_error",
    [
        ("title", "", "This field is required."),
        ("description", "", "This field is required."),
        ("start_at", "2000-2-22", "Start at must greater than today."),
    ],
)
@pytest.mark.django_db
def test_create_event_failed(
    client,
    user_a,
    create_event_url,
    create_event_payload,
    field,
    value,
    expected_error,
):
    create_event_payload[field] = value
    client.force_login(user_a)
    response = client.post(create_event_url, create_event_payload)
    assert expected_error in str(response.content)


@pytest.mark.django_db
def test_create_event_unauthorized(
    client,
    create_event_url,
    create_event_payload,
):
    response = client.post(create_event_url, create_event_payload)
    # Should be redirect to login url
    assert reverse("accounts:login") in response["Location"]

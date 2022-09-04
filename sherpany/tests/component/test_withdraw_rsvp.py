from http import HTTPStatus

import pytest
from django.urls import reverse
from django.utils import timezone

from events.models import EventRSVP


@pytest.mark.django_db
def test_withdraw_rsvp_success(
    client,
    user_b,
    event_rsvp,
    withdraw_event_url,
    withdraw_rsvp_success_content,
):
    client.force_login(user_b)
    response = client.post(withdraw_event_url, follow=True)
    assert EventRSVP.objects.count() == 0
    assert withdraw_rsvp_success_content in str(response.content)


@pytest.mark.django_db
def test_withdraw_rsvp_not_participant(
    client,
    user_b,
    withdraw_event_url,
):
    client.force_login(user_b)
    response = client.post(withdraw_event_url)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_reserve_event_unauthorized(
    client,
    withdraw_event_url,
):
    response = client.post(withdraw_event_url)
    # Should be redirect to login url
    assert reverse("accounts:login") in response["Location"]

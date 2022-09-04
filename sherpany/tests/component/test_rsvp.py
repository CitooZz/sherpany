import pytest
from django.urls import reverse
from django.utils import timezone

from events.models import EventRSVP


@pytest.mark.django_db
def test_reserve_event(client, user_b, reserve_event_url, rsvp_success_content):
    client.force_login(user_b)
    response = client.post(reserve_event_url, follow=True)
    assert EventRSVP.objects.count() == 1
    assert rsvp_success_content in str(response.content)


@pytest.mark.django_db
def test_reserve_passed_event(
    client, user_b, reserve_event_url, event, rsvp_error_passed_event_content
):
    # Set event start_at to passed
    event.start_at = timezone.now()
    event.save()

    client.force_login(user_b)
    response = client.post(reserve_event_url, follow=True)
    assert rsvp_error_passed_event_content in str(response.content)
    assert EventRSVP.objects.count() == 0


@pytest.mark.django_db
def test_reserve_owner_event(
    client, user_a, reserve_event_url, rsvp_error_owner_event_content
):
    client.force_login(user_a)
    response = client.post(reserve_event_url, follow=True)
    assert rsvp_error_owner_event_content in str(response.content)
    assert EventRSVP.objects.count() == 0


@pytest.mark.django_db
def test_reserved_event(
    client,
    user_b,
    reserve_event_url,
    event,
    rsvp_already_reserved_event_content,
):
    # Set event rsvp
    EventRSVP.objects.create(event=event, user=user_b)

    client.force_login(user_b)
    response = client.post(reserve_event_url, follow=True)
    assert rsvp_already_reserved_event_content in str(response.content)
    assert EventRSVP.objects.count() == 1


@pytest.mark.django_db
def test_reserve_event_unauthorized(
    client,
    reserve_event_url,
):
    response = client.post(reserve_event_url)
    # Should be redirect to login url
    assert reverse("accounts:login") in response["Location"]

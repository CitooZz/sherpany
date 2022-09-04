from http import HTTPStatus
from typing import Final

import pytest
from pytest_django.asserts import assertTemplateUsed

from events.models import Event

NEXT_PAGE_KEYWORD: Final = "Next Page"


@pytest.mark.django_db
def test_retrieve_my_events(
    client,
    user_a,
    my_events_url,
):
    client.force_login(user_a)
    response = client.get(my_events_url)
    assert response.status_code == HTTPStatus.OK
    response_content = str(response.content)
    assert NEXT_PAGE_KEYWORD in response_content

    event = Event.objects.first()
    assert event.title in response_content
    assertTemplateUsed(response, "events/my_events.html")


@pytest.mark.django_db
def test_retrieve_events_by_user_b(
    client,
    user_b,
    my_events_url,
):
    client.force_login(user_b)
    response = client.get(my_events_url)
    assert response.status_code == HTTPStatus.OK
    response_content = str(response.content)
    assert NEXT_PAGE_KEYWORD not in response_content
    assert " No events yet" in response_content


@pytest.mark.django_db
def test_retrieve_public_events(
    client,
    user_a,
    public_events_url,
):
    client.force_login(user_a)
    response = client.get(public_events_url)
    assert response.status_code == HTTPStatus.OK
    response_content = str(response.content)
    assert NEXT_PAGE_KEYWORD in response_content

    event = Event.objects.first()
    assert event.title in response_content
    assertTemplateUsed(response, "events/public_events.html")


@pytest.mark.django_db
def test_retrieve_detail_event(
    client,
    user_a,
    detail_event_url,
):
    client.force_login(user_a)
    response = client.get(detail_event_url)
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "events/detail_event.html")
    response_content = str(response.content)
    # Edit button should exist
    assert "Edit" in response_content
    # Only other use can see reserve event button
    assert "Reserve" not in response_content

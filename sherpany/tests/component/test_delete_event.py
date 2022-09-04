from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_delete_event_success(
    client,
    user_a,
    delete_event_url,
    delete_event_success_content,
):
    client.force_login(user_a)
    response = client.delete(delete_event_url, follow=True)
    assert response.status_code == HTTPStatus.OK
    assert delete_event_success_content in str(response.content)


@pytest.mark.django_db
def test_delete_other_user_event(
    client,
    user_b,
    delete_event_url,
):
    client.force_login(user_b)
    response = client.delete(delete_event_url)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_delete_event_not_found(
    client,
    user_a,
):
    client.force_login(user_a)
    response = client.delete(reverse("events:delete_event", kwargs={"pk": 12}))
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_delete_event_unauthorized(
    client,
    delete_event_url,
):
    response = client.delete(delete_event_url)
    # Should be redirect to login url
    assert reverse("accounts:login") in response["Location"]

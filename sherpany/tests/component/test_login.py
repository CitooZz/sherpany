from http import HTTPStatus

import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_login_success(client, login_url, login_payload):
    response = client.post(login_url, login_payload, follow=True)
    assert response.status_code == HTTPStatus.OK
    assert "Logout" in str(response.content)


@pytest.mark.django_db
def test_login_failed(client, login_url, login_payload, login_error_content):
    login_payload["password"] = "invalid"  # noqa: S105
    response = client.post(login_url, login_payload)
    assert response.status_code == HTTPStatus.OK
    assert login_error_content in str(response.content)
    assertTemplateUsed(response, "accounts/login.html")

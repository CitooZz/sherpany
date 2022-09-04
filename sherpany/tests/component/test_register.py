from http import HTTPStatus

import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_register_success(client, register_url, register_payload):
    response = client.post(register_url, register_payload, follow=True)
    assert response.status_code == HTTPStatus.OK
    assert "Login" in str(response.content)


@pytest.mark.parametrize(
    "field, value",
    [
        ("password1", "invalid"),
        ("password2", "invalid"),
        ("email", "invalid-email"),
    ],
)
@pytest.mark.django_db
def test_register_failed(
    client,
    register_url,
    register_payload,
    field,
    value,
):
    register_payload[field] = value
    response = client.post(register_url, register_payload)
    assert response.status_code == HTTPStatus.OK
    assert "Please correct your data and try again." in str(response.content)
    assertTemplateUsed(response, "accounts/register.html")

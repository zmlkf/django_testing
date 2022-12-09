import pytest


@pytest.mark.django_db(transaction=True)
def test_get(client):
    response = client.get('')
    assert response.status_code == 200, 'Не Ok'

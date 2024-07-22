from http import HTTPStatus

from sqlalchemy import select

from fast_zero.models import ToDo, User


def test_create_todo(client, token):
    response = client.post(
        '/todo/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Todo',
            'description': 'Test Description',
            'state': 'draft',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'Test Description',
        'state': 'draft',
    }

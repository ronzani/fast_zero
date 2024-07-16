from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'test_user',
            'email': 'user_teste@testemail.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'test_user',
        'email': 'user_teste@testemail.com',
    }


def test_create_user_username_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': f'{user.username}',
            'email': 'user_teste_alterado@testemail.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'test_user_alterado',
            'email': f'{user.email}',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_list_users(client, user_public_schema):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_public_schema]}


def test_get_user_ok(client, user_public_schema):
    response = client.get(f'/users/{user_public_schema["id"]}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_public_schema


def test_get_user_not_found(client):
    response = client.get('/users/456')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user_ok(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test_user_alterado',
            'email': 'user_alterado@testmail.com',
            'password': '654321',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'test_user_alterado',
        'email': 'user_alterado@testmail.com',
    }


def test_update_user_not_found(client, token):
    response = client.put(
        '/users/456',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test_user_alterado',
            'email': 'user_alterado@testmail.com',
            'password': '654321',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_user(client, user, token):
    response_delete = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response_delete.status_code == HTTPStatus.OK
    assert response_delete.json() == {'message': 'User deleted'}


def test_delete_user_forbidden(client, user, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}

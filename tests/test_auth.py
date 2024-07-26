from http import HTTPStatus

from freezegun import freeze_time

from fast_zero.security import create_access_token


def test_login_token_ok(client, user):
    response = client.post(
        'auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )

    response_token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_token['token_type'] == 'bearer'
    assert 'access_token' in response_token


def test_login_token_invalid_password(client, user):
    response = client.post(
        'auth/token',
        data={
            'username': user.email,
            'password': 'wrong_password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_login_token_invalid_username(client, user):
    response = client.post(
        'auth/token',
        data={
            'username': 'wrong@email.com',
            'password': user.clean_password,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_delete_user_unauthorized_invalid_token(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': 'Bearer invalid_token'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_delete_user_unauthorized_invalid_token_user(client, user):
    data = {'sub': 'wrong_email@email.com'}
    _token = create_access_token(data)

    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {_token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_delete_user_unauthorized_invalid_token_sub(client, user):
    _token = create_access_token({})

    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {_token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_expired_after_time(client, user):
    with freeze_time('2024-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        _token = response.json()['access_token']

    with freeze_time('2024-07-14 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {_token}'},
            json={
                'username': 'wrongwrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Token has expired'}


def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        _token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {_token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Token has expired'}

from http import HTTPStatus


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
            'password': 'senha_invalida',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_login_token_invalid_username(client, user):
    response = client.post(
        'auth/token',
        data={
            'username': 'ivalid',
            'password': user.clean_password,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}

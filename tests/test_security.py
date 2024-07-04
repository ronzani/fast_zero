from http import HTTPStatus

from jwt import decode

from fast_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {'sub': 'test@email.com'}
    _token = create_access_token(data)

    decoded = decode(_token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded['sub'] == data['sub']
    assert decoded['exp']  # Testa se o valor de exp foi adicionado ao toke


def test_login_token_ok(client, user):
    response = client.post(
        '/token',
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
        '/token',
        data={
            'username': user.email,
            'password': 'senha_invalida',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_login_token_invalid_username(client, user):
    response = client.post(
        '/token',
        data={
            'username': 'ivalid',
            'password': user.clean_password,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}

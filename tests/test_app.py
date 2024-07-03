from http import HTTPStatus


def test_root_helo_word(client):
    response = client.get('/api')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_root_html(client):
    response = client.get('/')

    _html = """
    <html>
        <head>
            <title>Olá mundo!</title>
        </head>
        <body>
            <h1> Olá Mundo! </h1>
        </body>
    </html>
    """

    assert response.status_code == HTTPStatus.OK
    assert response.text == _html


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
            'username': 'test_user',
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
            'email': 'user_teste@testemail.com',
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
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_public_schema


def test_get_user_not_found(client):
    response = client.get('/users/456')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user_ok(client, user):
    response = client.put(
        f'/users/{user.id}',
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


def test_update_user_not_found(client):
    response = client.put(
        '/users/456',
        json={
            'username': 'test_user_alterado',
            'email': 'user_alterado@testmail.com',
            'password': '654321',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_and_check_deleted(client, user):
    response_delete = client.delete(f'/users/{user.id}')
    response_get = client.get(f'/users/{user.id}')

    assert response_delete.status_code == HTTPStatus.OK
    assert response_delete.json() == {'message': 'User deleted'}
    assert response_get.status_code == HTTPStatus.NOT_FOUND
    assert response_get.json() == {'detail': 'User not found'}


def test_delete_user_not_found(client):
    response = client.delete('/users/456')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_login_token_ok(client, user):
    response = client.post(
        '/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'bearer'
    assert 'access_token' in token


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

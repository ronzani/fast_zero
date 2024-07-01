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
            'username': 'testeuser',
            'email': 'teste@email.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'testeuser',
        'email': 'teste@email.com',
    }


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


#
# def test_update_user_ok(client):
#     response = client.put(
#         '/users/1',
#         json={
#             'username': 'testeuser_alterado',
#             'email': 'user_alterado@example.com',
#             'password': '654321',
#         },
#     )
#
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {
#         'id': 1,
#         'username': 'testeuser_alterado',
#         'email': 'user_alterado@example.com',
#     }
#
#
# def test_update_user_not_found(client):
#     response = client.put(
#         '/users/456',
#         json={
#             'username': 'testeuser_alterado',
#             'email': 'user_alterado@example.com',
#             'password': '654321',
#         },
#     )
#
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}
#
#
# def test_delete_user_ok(client):
#     response = client.delete('/users/1')
#
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {'message': 'User deleted'}
#
#
# def test_delete_user_not_found(client):
#     response = client.delete('/users/456')
#
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}

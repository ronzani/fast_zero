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

from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_helo_word():
    client = TestClient(app)

    response = client.get('/api')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_root_html():
    client = TestClient(app)

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

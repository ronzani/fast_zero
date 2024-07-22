from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routers import auth, todo, users
from fast_zero.schemas import Message

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todo.router)


@app.get('/api', status_code=HTTPStatus.OK, response_model=Message)
def root_api():
    return {'message': 'Olá Mundo!'}


@app.get('/', response_class=HTMLResponse)
def root_html():
    return """
    <html>
        <head>
            <title>Olá mundo!</title>
        </head>
        <body>
            <h1> Olá Mundo! </h1>
        </body>
    </html>
    """

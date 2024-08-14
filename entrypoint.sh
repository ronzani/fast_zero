#!/bin/sh

# Executa as migrações do banco de dados
poetry run alembic upgrade head

# Inicia a aplicação
#poetry run uvicorn --host 0.0.0.0 --port 8000 fast_zero.app:app
poetry run fastapi run fast_zero/app.py --host 0.0.0.0
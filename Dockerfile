FROM python:3.10

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install

COPY . .

ENTRYPOINT ["python3", "-m", "main"]

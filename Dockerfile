FROM python:3.10

RUN mkdir /hexagonal

COPY alembic.ini /hexagonal/
COPY migrations /hexagonal/

COPY poetry.lock /hexagonal/
COPY pyproject.toml /hexagonal/

RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry install --no-dev

COPY app /hexagonal/

CMD ["poetry", "run", "python", "-m", "app", "web"]
EXPOSE 5000
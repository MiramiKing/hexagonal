.PHONY: lint test test-cov infra app install-deps web cli

lint:
		poetry run flake8 app/

test:
		poetry run pytest app/

test-cov:
		poetry run pytest app/ --cov=app --cov-report=xml

infra:
		docker-compose -f local/docker-compose.infra.yaml up --remove-orphans

app:
		docker build . -t hexagonal:latest
		docker-compose -f local/docker-compose.app.yaml up --remove-orphans

web:
		poetry run python -m app web

cli:
		poetry run python -m app cli

install-deps:
		pip3 install --upgrade pip
		pip install poetry
		poetry install

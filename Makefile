.PHONY: install reset-db run-playground test-playground

build:
	poetry build

install:
	pip install --upgrade pip==19.0.3
	pip install poetry==1.0.5
	poetry install -vvv

run-playground:
	python playground/main.py

reset-db:
	python playground/manage.py app initialize-db --force

test-playground:
	pyresttest http://127.0.0.1:6543 playground/tests/pyresttest_api_scenarios.yaml

publish: build
	# Using twine because of poetry issue https://github.com/python-poetry/poetry/issues/1999
	twine upload --repository-url https://geru-pypi.geru.com.br/ dist/*

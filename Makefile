.PHONY: install reset-db run-playground test-playground

install:
	pip install --upgrade pip==19.0.3
	pip install poetry==0.12.17
	poetry install

run-playground:
	python playground/main.py

reset-db:
	python playground/manage.py app initialize-db --force

test-playground:
	pyresttest http://127.0.0.1:6543 playground/tests/pyresttest_api_scenarios.yaml

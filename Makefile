.PHONY: install reset-db run-playground test-playground

install:
	pip install -e .
	pip install -e .[dev]
	pip install -e .[test]
	pip install -e .[ci]
	pip install -e .[sqla]

run-playground:
	python playground/main.py

reset-db:
	python playground/manage.py app initialize-db --force

test-playground:
	pyresttest http://127.0.0.1:6543 playground/tests/pyresttest_api_scenarios.yaml

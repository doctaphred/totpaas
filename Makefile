default: lint test runserver

lint:
	flake8
	mypy .

test:
	pytest

runserver:
	uvicorn totpaas.main:app --reload

.PHONY: default lint test runserver

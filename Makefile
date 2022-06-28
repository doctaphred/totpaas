default: lint test runserver

lint:
	flake8 src tests
	mypy src tests

test:
	pytest

runserver:
	-open http://localhost:8000
	uvicorn totpaas.main:app --reload

.PHONY: default lint test runserver

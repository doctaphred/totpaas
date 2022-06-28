default: lint test runserver

lint:
	flake8 src tests
	mypy src tests

test:
	pytest

runserver:
	-open http://localhost:8000
	uvicorn totpaas.app:from_environ --factory --reload

.PHONY: default lint test runserver

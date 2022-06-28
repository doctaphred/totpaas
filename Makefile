default: lint test runserver

lint:
	flake8 src tests
	mypy src tests

test:
	pytest

runserver:
	# Export the RUNSERVER_OPEN_PATH env var if desired:
	# otherwise, the root path `/` will be opened.
	-open http://localhost:8000${RUNSERVER_OPEN_PATH}
	uvicorn totpaas.app:from_environ --factory --reload

.PHONY: default lint test runserver

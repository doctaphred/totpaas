default: lint test open start

lint:
	flake8 src tests
	mypy src tests

test:
	pytest

open:
	# Export the MAKE_OPEN_PATH env var if desired:
	# otherwise, the root path `/` will be opened.
	open http://localhost:8000${MAKE_OPEN_PATH}

start:
	uvicorn totpaas.app:from_environ --factory --reload

prod-build:
	poetry install --no-dev

prod-start:
	uvicorn totpaas.app:from_environ --factory --host 0.0.0.0

.PHONY: default lint test open start prod-build prod-start

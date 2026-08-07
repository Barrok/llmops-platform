.PHONY: lint format run

lint:
	uv run ruff check .

format:
	uv run ruff format .

test:
	uv run pytest

check: lint test

run:
	uv run uvicorn app.main:app --reload
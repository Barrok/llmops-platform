.PHONY: lint format run

lint:
	uv run ruff check .

format:
	uv run ruff format .

run:
	uv run uvicorn app.main:app --reload
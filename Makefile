.PHONY: dev test test-integration test-unit

dev:
	uv run uvicorn app.main:app --reload --log-config=./app/log_config.yaml

test:
	uv run pytest ./tests -v --log-cli-level=INFO

test-integration:
	uv run pytest ./tests/integration/ -v --log-cli-level=INFO

test-unit:
	uv run pytest ./tests/unit/ -v --log-cli-level=INFO

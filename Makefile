.PHONY: run

dev:
	uv run uvicorn app.main:app --reload --log-config=./app/log_config.yaml



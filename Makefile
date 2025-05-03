.PHONY: dev run-dev test test-integration test-unit

DATABASE_URL ?= unset
KUBECONFIG ?= unset

dev:
	@if [ "$(DATABASE_URL)" == "unset" ]; then \
		echo "DATABASE_URL is not set."; \
		exit 1; \
	fi
	uv run uvicorn app.main:app --reload --log-config ./app/log_config.yaml

run-dev:
	docker-compose up

test:
	DATABASE_URL="sqlite://" uv run pytest ./tests -v --log-cli-level=INFO

test-integration:
	DATABASE_URL="sqlite://" uv run pytest ./tests/integration/ -v --log-cli-level=INFO

test-unit:
	uv run pytest ./tests/unit/ -v --log-cli-level=INFO

build-container:
	docker buildx build --tag hello-app:0.1.0 .

deploy:
	@if [ "$(KUBECONFIG)" == "unset" ]; then \
		echo "KUBECONFIG is not set."; \
		exit 1; \
	fi

	helm install hello-app ./k8s/hello-app

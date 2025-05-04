.PHONY: build-container check-env deploy dev expose-nodeport-minikube publish-minikube run-dev test-integration test-unit test

DATABASE_URL ?= unset
KUBECONFIG ?= unset

build-container:
	docker buildx build --tag hello-app:0.1.0 .

check-env:
	@echo "Check if the enviroment variables are installed";
	@if [ "$(KUBECONFIG)" == "unset" ]; then \
		echo "KUBECONFIG is not set."; \
		exit 1; \
	fi

deploy: check-env
	helm install hello-app ./k8s/hello-app

dev:
	@if [ "$(DATABASE_URL)" == "unset" ]; then \
		echo "DATABASE_URL is not set."; \
		exit 1; \
	fi
	uv run uvicorn app.main:app --reload --log-config ./app/log_config.yaml

expose-nodeport-minikube: check-env
	minikube service hello-app --url

publish-minikube: check-env
	minikube image load hello-app:0.1.0

run-dev:
	docker-compose up

test:
	DATABASE_URL="sqlite://" uv run pytest ./tests -v --log-cli-level=INFO

test-integration:
	DATABASE_URL="sqlite://" uv run pytest ./tests/integration/ -v --log-cli-level=INFO

test-unit:
	uv run pytest ./tests/unit/ -v --log-cli-level=INFO

SHELL := /bin/bash
TESTING ?= 0
DEPLOY ?= 0


run-local:
	pipenv lock -r > requirements.txt
	docker build --tag example-fastapi-gql .
	@echo Delete old container
	docker rm -f example-fastapi-gql-c
	@echo Run new container
	rm requirements.txt
	docker run --rm \
	-p 9090:8080 \
	-e PORT=8080 \
	-e WORKERS=1 \
	-e API_KEY=TEST \
	-e LOGGER_LEVEL=DEBUG \
	--name example-fastapi-gql-c \
	example-fastapi-gql

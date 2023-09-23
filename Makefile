# Define the shell to use
SHELL := /bin/bash

# Define the name of the Docker image
IMAGE_NAME := sql-translation-api

# Define the shell command
shell:
	poetry shell

run:
	flask run

.PHONY: docker-run docker run
docker-run:
	docker compose up -d

.PHONY: docker-stop docker stop
docker-stop:
	docker compose down	

# Define the build command
build:
	docker build -t $(IMAGE_NAME):prod .

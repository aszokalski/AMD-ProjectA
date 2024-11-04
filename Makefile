# Makefile for Docker Compose Services

# Default target: help
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make up               Start all services"
	@echo "  make down             Stop all services"
	@echo "  make restart          Restart all services"
	@echo "  make rebuild          Rebuild all services"
	@echo "  make logs             View logs for all services"
	@echo "  make logs-<service>   View logs for a specific service"
	@echo "  make healthcheck      Check health status of services"
	@echo "  make medknow          Open Medknow API documentation"
	@echo "  make softknow         Open Softknow API documentation"
	@echo "  make test             Run tests"

# Start all services
.PHONY: up
up:
	docker-compose up -d

# Stop all services
.PHONY: down
down:
	docker-compose down

# Restart all services
.PHONY: restart
restart: down up

# Rebuild all services
.PHONY: rebuild
rebuild:
	docker-compose up -d --build

# View logs for all services
.PHONY: logs
logs:
	docker-compose logs -f

.PHONY: medknow
medknow:
	python3 -m webbrowser -t "http://localhost:2000/docs"

.PHONY: softknow
softknow:
	python3 -m webbrowser -t "http://localhost:3000/docs"


.PHONY: test
test:
	chmod +x test.sh
	./test.sh


# View logs for specific services (postgres, medknow, softknow, mlflow)
.PHONY: logs-postgres logs-medknow logs-softknow logs-mlflow
logs-%:
	docker-compose logs -f $*
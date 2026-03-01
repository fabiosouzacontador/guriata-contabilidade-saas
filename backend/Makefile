.PHONY: help install dev test lint format clean docker-up docker-down docker-logs

help:
	@echo "Guriata Contabilidade - Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make dev           - Run development server"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linter"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean cache files"
	@echo "  make docker-up     - Start Docker containers"
	@echo "  make docker-down   - Stop Docker containers"
	@echo "  make docker-logs   - View Docker logs"
	@echo "  make migrate       - Run database migrations"

install:
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest tests/ -v --cov=app

test-watch:
	pytest-watch tests/ -v

lint:
	flake8 app tests
	pylint app tests

format:
	black app tests --line-length 100

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov

docker-up:
	docker-compose up -d
docker-down:
	docker-compose down
docker-logs:
	docker-compose logs -f
docker-build:
	docker-compose build

migrate:
	alembic upgrade head

migrate-create:
	alembic revision --autogenerate -m "$(name)"
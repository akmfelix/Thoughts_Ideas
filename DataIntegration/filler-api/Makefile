VENV := venv


# variables that will be accessible by child processes
.EXPORT_ALL_VARIABLES:
PYTHONPATH := ./
APPPATH := ./app
SERVICE_PORT := 8000
HTTP_PROXY := http://proxy.halykbank.nb:8080
HTTPS_PROXY := http://proxy.halykbank.nb:8080
# Collector Database
COLLECTOR_DATABASE_HOST := localhost
COLLECTOR_DATABASE_PORT := 5432
COLLECTOR_DATABASE_NAME := filler_db
COLLECTOR_DATABASE_LOGIN := user
COLLECTOR_DATABASE_PASSWORD := pass
# legal-entity-reports Database
LEGAL_ENTITY_REPORTS_DATABASE_HOST := localhost
LEGAL_ENTITY_REPORTS_DATABASE_PORT := 5432
LEGAL_ENTITY_REPORTS_DATABASE_NAME := filler_db
LEGAL_ENTITY_REPORTS_DATABASE_LOGIN := user
LEGAL_ENTITY_REPORTS_DATABASE_PASSWORD := pass
# Guarantee Database
GUARANTEE_DATABASE_HOST := localhost
GUARANTEE_DATABASE_PORT := 5432
GUARANTEE_DATABASE_NAME := filler_db
GUARANTEE_DATABASE_LOGIN := user
GUARANTEE_DATABASE_PASSWORD := pass
# Kafka
BOOTSTRAP_SERVERS := localhost:9092
TOPIC := offers-interest

# environments below you need to fill by yourself. Don't push to Git
GOSZAKUP_TOKEN :=

# change base on your needs
NO_PROXY := localhost

.DEFAULT_GOAL := help


help:
	@echo "Description: CLI for filler service management"
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  help        Show this help message"
	@echo "  venv        Setup Virtual Environment & Install project dependencies"
	@echo "  lint        Lint source code ( \`flake8\` will be used under the hood )"
	@echo "  run         Run application with all dependencies needed"
	@echo "  clean       Delete all created directories & installed libraries"


# default target, when make executed without arguments
all: venv


$(VENV)/bin/activate: requirements.txt .EXPORT_ALL_VARIABLES
	@python3 -m venv $(VENV)
	@./$(VENV)/bin/python -m pip install --upgrade pip setuptools
	@./$(VENV)/bin/pip install -r requirements.txt


linter-dependencies: venv
	@./$(VENV)/bin/pip install flake8 isort


lint: linter-dependencies .flake8 isort.cfg
	@./$(VENV)/bin/python -m isort $(APPPATH) --settings-path ./isort.cfg
	@./$(VENV)/bin/python -m flake8 $(APPPATH)


venv: $(VENV)/bin/activate


database:
	@docker-compose up -d filler-postgres


migrate:
	@docker-compose up filler-flyway


run: venv database migrate
	@./$(VENV)/bin/python -m uvicorn "app.main:init_app" --host localhost --port $(SERVICE_PORT) --log-level debug --reload --factory

run-gunicorn: venv database migrate
	@./$(VENV)/bin/gunicorn -c "app/gunicorn.conf.py" --reload --log-level debug "app.main:init_app()"

stop:
	@docker-compose down


clean:
	@./$(VENV)/bin/python -m pip cache purge
	@rm -rf $(VENV)
	@docker-compose down -v


.PHONY: all venv run clean lint help

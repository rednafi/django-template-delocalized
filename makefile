path := .

define Comment
	- Run `make help` to see all the available options.
	- Run `make testall` to run all the tests.
	- Run `make lint` to run the linter.
	- Run `make lint-check` to check linter conformity.
	- Run `make publish` to publish to PYPI.
endef


.PHONY: lint
lint: black isort flake mypy	## Apply all the linters.


.PHONY: lint-check
lint-check:  ## Check whether the codebase satisfies the linter rules.
	@echo
	@echo "Checking linter rules..."
	@echo "========================"
	@echo
	@black --check $(path)
	@isort --check $(path)
	@flake8 $(path)
	@mypy $(path)


.PHONY: black
black: ## Apply black.
	@echo
	@echo "Applying black..."
	@echo "================="
	@echo
	@black --fast $(path)
	@echo


.PHONY: isort
isort: ## Apply isort.
	@echo "Applying isort..."
	@echo "================="
	@echo
	@isort $(path)


.PHONY: flake
flake: ## Apply flake8.
	@echo
	@echo "Applying flake8..."
	@echo "================="
	@echo
	@flake8 $(path)


.PHONY: mypy
mypy: ## Apply mypy.
	@echo
	@echo "Applying mypy..."
	@echo "================="
	@echo
	@mypy $(path)


.PHONY: help
help: ## Show this help message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: create_topology
create_topology: ## Creates topology diagram from docker compose file.
	@docker run \
	--rm -it \
	--name dcv \
	-v /home/rednafi/workspace/personal/django-template-delocalized:/input pmsipilot/docker-compose-viz \
	render -m image \
	--force docker-compose.yml \
	--output-file=topology.png \
	--no-volumes \
	--no-networks


.PHONY: start_servers
start_servers: ## Start the Django servers.
	docker-compose up --build -d


.PHONY: stop_servers
stop_servers: ## Stop the Django servers.
	docker-compose down && docker system prune -f

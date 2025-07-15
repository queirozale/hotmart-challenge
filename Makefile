.PHONY: clean data

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PYTHON_INTERPRETER = python3
CONFIG_FILE = pyproject.toml
CONFIG_KEY_NAME = requires-python

#################################################################################
# BLOCK TO TEST PYTHON INSTALLATION                                             #
#################################################################################

# Test if python is installed

ifeq (,$(shell $(PYTHON_INTERPRETER) --version))
$(error "Python is not installed!")
endif


#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Verify Python Version
check_installed_python:
	$(eval INSTALLED := $(shell $(PYTHON_INTERPRETER) --version | tr -cd '[[:digit:][:punct:]]'))
	$(eval REQUIRED := $(shell [ -f $(CONFIG_FILE) ] && cat $(CONFIG_FILE) | grep -w $(CONFIG_KEY_NAME) | grep -oP '\d+(\.\d+)+'))

	@if [ -z "$(REQUIRED)" ] | [ $(shell echo -n "$(REQUIRED)" | wc -c ) -lt 3 ]; then \
		echo "Missing configurarion file or key"; \
		return 1; \
	fi

	@if { echo "$(REQUIRED)" ; echo "$(INSTALLED)"; } | sort --version-sort --check=quiet; then \
		echo "Python interpreter is up to date: required Python '$(REQUIRED)' found Python '$(INSTALLED)'"; \
	else \
		echo "Python version error: required Python '$(REQUIRED)' found Python '$(INSTALLED)'" ; \
		exit 1; \
	fi


# Install uv for dependency management
install-uv: check_installed_python
	pip install uv
	uv pip install pip

## Install Python Dependencies & Install pre-commit hooks
requirements: check_installed_python
	uv add -r requirements.in
	uv add --optional dev -r requirements-dev.in
	uv add --optional test -r requirements-test.in
	@pre-commit install --hook-type commit-msg

## Synchronize the Python Dependencies & Virtual Env
sync-env: check_installed_python
	uv sync --all-extras --all-groups

## Delete all compiled Python files
clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name ".tox" -exec rm -r "{}" +
	@find . -type d -name ".pytest_cache" -exec rm -r "{}" +
	@find . -type d -name ".mypy_cache" -exec rm -r "{}" +

test:
	@python -m pytest

build:
	@docker build -f Dockerfile -t support-bot .
	@docker run -it -p 500:500 support-bot
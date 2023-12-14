recursive-wildcard=$(foreach d,$(wildcard $(1:=/*)),$(call recursive-wildcard,$d,$2) $(filter $(subst *,%,$2),$d))

PYTHON := python3.12
VENV_DIR := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python
PYPROJECT_FILES := $(call recursive-wildcard,., *pyproject.toml)
PYTHON_FILES := $(call recursive-wildcard,., *.py)
DOCKERFILES := $(call recursive-wildcard,., Dockerfile*)

.PHONY: check-format
check-format: init-dev-venv
	$(VENV_PYTHON) -m black  --check --config black.toml .

.PHONY: format
format: init-dev-venv
	$(VENV_PYTHON) -m black  --config black.toml .

.PHONY: check-imports
check-imports: init-dev-venv
	$(VENV_PYTHON) -m isort --check-only --settings isort.toml .

.PHONY: sort-imports
sort-imports: init-dev-venv
	$(VENV_PYTHON) -m isort --settings isort.toml .

.PHONY: check-lint
check-lint: init-dev-venv
	$(VENV_PYTHON) -m pylint --rcfile pylintrc.toml --recursive=y --ignore=.venv,build .

.PHONY: check-types
check-types: init-dev-venv
	$(VENV_PYTHON) -m mypy --config-file mypy.toml . --exclude build

.PHONY: check
check: check-format check-imports check-lint check-types

CREATE_DEV_VENV := $(VENV_DIR)/create_dev_venv_stamp
.PHONY: create-dev-venv
create-dev-venv: $(CREATE_DEV_VENV)
$(CREATE_DEV_VENV):
	$(PYTHON) -m venv --clear $(VENV_DIR)
	$(VENV_PYTHON) -m pip install --upgrade pip
	touch $@

INIT_DEV_VENV := $(VENV_DIR)/init_dev_venv_stamp
.PHONY: init-dev-venv
init-dev-venv: $(INIT_DEV_VENV)
$(INIT_DEV_VENV): $(PYPROJECT_FILES) | create-dev-venv
	$(VENV_PYTHON) -m pip install --editable main_node[dev] --editable chat_node[dev] --editable client[dev]
	touch $@

BUILD_CONTAINERS := tmp/build_containers_stamp
.PHONY: build-containers
build-containers: $(BUILD_CONTAINERS)
$(BUILD_CONTAINERS): $(PYTHON_FILES) $(PYPROJECT_FILES) $(DOCKERFILES)
	docker compose build
	mkdir -p tmp
	touch $@

UP := tmp/up_stamp
.PHONY: up
up: $(BUILD_CONTAINERS)
	docker compose up

BUILD_DEV_CONTAINERS := tmp/build_dev_containers_stamp
.PHONY: build-dev-containers
build-dev-containers: $(BUILD_DEV_CONTAINERS)
$(BUILD_DEV_CONTAINERS): $(PYPROJECT_FILES) $(DOCKERFILES)
	docker compose -f docker-compose-dev.yml build
	mkdir -p tmp
	touch $@

DEV_UP := tmp/dev_up_stamp
.PHONY: dev-up
dev-up: $(BUILD_DEV_CONTAINERS)
	docker compose -f docker-compose-dev.yml up


.PHONY: client
client:
	docker build -t client -f client/Dockerfile client/
	docker run -it --network distributed-systems_chat client

.PHONY: client-dev
client-dev:
	docker build -t client-dev -f client/Dockerfile-dev .
	docker run -it -v ./:/source --network distributed-systems_chat client-dev

.PHONY: clean
clean:
	rm -rf $(VENV_DIR) tmp


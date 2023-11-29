.PHONY: check-format
check-format:
	black  --check --config black.toml .

.PHONY: format
format:
	black  --config black.toml .

.PHONY: isort
check-imports:
	isort --check-only --settings isort.toml .

.PHONY: isort
imports:
	isort --settings isort.toml .

.PHONY: lint
lint:
	pylint --rcfile pylintrc.toml --recursive=y --ignore=.venv,build .

.PHONY: types
types:
	mypy --config-file mypy.toml . --exclude build

.PHONY: check
check: check-format imports lint types
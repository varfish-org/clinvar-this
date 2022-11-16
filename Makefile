.PHONY: default
default:

.PHONY: black
black:
	black -l 100 .

.PHONY: black-check
black-check:
	black -l 100 --check .

.PHONY: isort
isort:
	isort --force-sort-within-sections --profile=black .

.PHONY: isort-check
isort-check:
	isort --force-sort-within-sections --profile=black --check .

.PHONY: flake8
flake8:
	flake8

.PHONY: mypy
mypy: export MYPYPATH=stubs
mypy:
	mypy clinvar_this clinvar_api tests

.PHONY: lint
lint: flake8 isort-check black-check mypy

.PHONY: pytest
pytest:
	pytest .

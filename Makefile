.PHONY: default
default:

.PHONY: format
format: black isort

.PHONY: lint
lint: flake8 isort-check black-check mypy

.PHONY: test
pytest:
	pytest .

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

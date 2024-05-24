.PHONY: default
default:

.PHONY: format
format: black isort protolint-fix

.PHONY: lint
lint: flake8 isort-check black-check mypy protolint-check

.PHONY: test
test:
	pytest .

.PHONY: test-update-snapshots
test-update-snapshots:
	pytest . --snapshot-update

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
	mypy clinvar_this clinvar_api clinvar_data tests

.PHONY: protolint-fix
protolint-fix:
	protolint lint -fix .

.PHONY: protolint-check
protolint-check:
	protolint lint .

# Re-run protoc.
.PHONY: protoc-run
protoc-run:
	mkdir -p clinvar_data/pbs/clinvar_this
	touch clinvar_data/pbs/__init__.py clinvar_data/pbs/clinvar_this/__init__.py
	rm -f \
		clinvar_data/*_pb2.py \
		clinvar_data/*.pyi
	protoc \
		-Iprotos \
			--python_out=. \
			--mypy_out=. \
			protos/clinvar_data/pbs/*.proto

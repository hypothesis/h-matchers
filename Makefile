.PHONY: help
help:
	@echo "make help              Show this help message"
	@echo "make lint              Code quality analysis (pylint)"
	@echo "make format            Correctly format the code"
	@echo "make checkformatting   Crash if the code isn't correctly formatted"

	@echo "make dist              Create package in the dist/ directory"
	@echo "make publish           Publish packages created in the dist/ directory"
	@echo "make test              Run the unit tests"
	@echo "make coverage          Print the unit test coverage report"
	@echo "make clean             Delete development artefacts (cached files, "
	@echo "                       dependencies, etc)"
	@echo "make template          Replay the cookiecutter project template over this"
	@echo "                       project. Warning! This can destroy changes."

.PHONY: lint
lint: python
	@tox -qe py36-lint

.PHONY: format
format: python
	@tox -qe py36-format

.PHONY: checkformatting
checkformatting: python
	@tox -qe py36-checkformatting

.PHONY: dist
dist: python
	@BUILD=$(BUILD) tox -qe py36-package

.PHONY: publish
publish: python
	@tox -qe py36-publish

.PHONY: test
test: python
	@tox -q

.PHONY: coverage
coverage: python
	@tox -qe py36-coverage

.PHONY: template
template: python
	@tox -qe py36-replay-cookiecutter

.PHONY: clean
clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -rf build .eggs dist *.egg-info src/*.egg-info .coverage.* .coverage .pytest_cache

.PHONY: python
python:
	@./bin/install-python.sh

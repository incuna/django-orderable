SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo " make help    -- displays this help"
	@echo " make test    -- runs tests"
	@echo " make release -- pushes to pypi"

test:
	@python orderable/tests/run.py
	@flake8

release:
	python setup.py register -r pypi sdist bdist_wheel upload -r pypi

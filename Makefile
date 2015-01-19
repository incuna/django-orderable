SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo " make help    -- displays this help"
	@echo " make test    -- runs tests"
	@echo " make release -- pushes to pypi"

test:
	@coverage run orderable/tests/run.py
	@coverage report -m
	@flake8

release:
	python setup.py register -r pypi sdist bdist_wheel upload -r pypi

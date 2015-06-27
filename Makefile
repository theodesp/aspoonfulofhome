.PHONY: clean-pyc

current_dir = $(shell pwd)

UI_FOLDER = $(current_dir)/core/static/

help:
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 .
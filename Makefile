.ONESHELL:
SHELL := /bin/bash

all: release
.PHONY: all release conda_release pypi clean dict

release: pypi
	fastrelease_conda_package --upload_user kaushikb11
	fastrelease_bump_version

conda_release:
	fastrelease_conda_package --upload_user kaushikb11

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist
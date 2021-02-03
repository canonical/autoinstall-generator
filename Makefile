
all: default
.PHONY: all

default:
	:
.PHONY: default

dev-setup:
	sudo apt install tox flake8 python3-pep517 python3-testresources
.PHONY: dev-setup

clean:
	rm -fr *.egg-info build dist
.PHONY: clean

distclean: clean
	-find . -type d -name __pycache__ | xargs rm -fr
	rm -fr .tox
.PHONY: distclean

build:
	python3 -m pep517.build .
.PHONY: build

test:
	tox
.PHONY: test

lint:
	flake8
.PHONY: lint

check: lint test
.PHONY: check

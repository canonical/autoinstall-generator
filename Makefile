
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

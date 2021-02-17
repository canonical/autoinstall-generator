
all: default
.PHONY: all

default: check
.PHONY: default

dev-setup:
	sudo apt install tox python3-pep517 python3-testresources
.PHONY: dev-setup

clean:
	rm -fr *.egg-info build dist
.PHONY: clean

distclean: clean
	-find . -type d -name __pycache__ | xargs rm -fr
	rm -fr .tox .coverage
.PHONY: distclean

build:
	python3 -m pep517.build .
.PHONY: build

test:
	tox
.PHONY: test

check: test
.PHONY: check

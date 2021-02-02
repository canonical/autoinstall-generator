
all: default
.PHONY: all

default:
	:
.PHONY: default

dev-setup:
	sudo apt install tox python3-pytest
.PHONY: dev-setup

clean:
	rm -fr *.egg-info
.PHONY: clean

test:
	tox
.PHONY: test

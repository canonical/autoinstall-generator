
default: all

all: check build

new: clean all

install_deps:
	sudo apt install tox python3-pep517 python3-testresources \
		python3-setuptools

clean:
	rm -fr *.egg-info build dist

distclean: clean
	-find . -type d -name __pycache__ | xargs rm -fr
	rm -fr .tox .coverage

build:
	python3 -m pep517.build .

lint:
	tox -e lint

test:
	tox -e test

check:
	tox

invoke:
	@PYTHONPATH=$(shell realpath .) \
		autoinstall_generator/bin/autoinstall_generator \
		autoinstall_generator/tests/data/preseed.txt --debug

.PHONY: default all new install_deps clean distclean build lint test check

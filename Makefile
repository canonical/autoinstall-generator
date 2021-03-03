
default: all

all: check build

new: clean all

install_deps:
	sudo apt install tox python3-testresources python3-setuptools

clean:
	rm -fr *.egg-info build dist README.html

distclean: clean
	-find . -type d -name __pycache__ | xargs rm -fr
	rm -fr .tox .coverage .pytest_cache

build:
	python3 setup.py bdist_wheel

lint:
	tox -e lint

test:
	tox -e test

check:
	tox

snap:
	snapcraft snap --debug

snap-clean:
	snapcraft clean autoinstall-generator

snap-install:
	sudo snap install *.snap --dangerous --devmode

html:
	markdown README.md > README.html

invoke:
	@PYTHONPATH=$(shell realpath .) \
		autoinstall_generator/cmd/autoinstall-generator.py \
		autoinstall_generator/tests/data/preseed.txt --debug

.PHONY: default all new install_deps clean distclean build lint test check
.PHONY: snap invoke snap-clean snap-install html

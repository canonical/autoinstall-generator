
default: all

all: check build

new: clean all

install_deps:
	sudo apt install tox python3-testresources python3-setuptools

clean:
	rm -fr *.egg-info build dist README.html *.tmp

distclean: clean
	-find . -type d -name __pycache__ | xargs rm -fr
	rm -fr .tox .coverage .pytest_cache *.snap

build:
	python3 setup.py bdist_wheel

lint:
	tox -e lint

test:
	tox -e test

check:
	tox

snap:
	snapcraft snap --use-lxd --debug

snap-clean:
	snapcraft clean --use-lxd autoinstall-generator metadata

snap-install:
	sudo snap install *.snap --dangerous --devmode

html:
	markdown README.md > README.html

readme:
	cat README.md | sed -ne '0,/^## Usage/p' > 1.tmp
	echo > 2.tmp
	@PYTHONPATH=$(shell realpath .) \
		autoinstall_generator/cmd/autoinstall-generator.py --help | \
		sed -ne 's/^\(.\+\)$$/    \1/;p' \
		> 3.tmp
	echo > 4.tmp
	cat README.md | sed -ne '/^## Feedback/,$$p' > 5.tmp
	cat ?.tmp > README.md.tmp

invoke:
	@PYTHONPATH=$(shell realpath .) \
		autoinstall_generator/cmd/autoinstall-generator.py \
		autoinstall_generator/tests/data/preseed.txt --debug

.PHONY: default all new install_deps clean distclean build lint test check
.PHONY: snap invoke snap-clean snap-install html

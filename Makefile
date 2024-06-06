.DEFAULT_GOAL := build
ifneq (,$(wildcard /etc/redhat-release))
    GITLIB := /usr/libexec/git-core
else
    GITLIB := /usr/lib/git-core
endif
VERSION := 0.6.2
USRLIB := /usr/local/bin
ADDFILES = aftermerge changelog nextrelease versionupdater
TESTADDFILES = $(addprefix ta-,$(ADDFILES))
REMOVEFILES = $(addprefix rm-,$(ADDFILES))
CWD=$(shell pwd)

fmt:
	poetry run black .  || exit 1

lint:	
	poetry run flake8 . || exit 1

test: clean fmt lint
	poetry run pytest || exit 1

slowtest: clean fmt lint
	poetry run pytest --runslow || exit 1

master:
	git checkout master

testmaster: master test

build: test
	poetry build

deploy: build
	python3 -m pip install gitrelease --index-url https://gitlab.com/api/v4/projects/53741339/packages/pypi/simple

remove:
	python3 -m pip uninstall -y gitrelease

deploylocal: build
	python3 -m pip install --user dist/gitrelease-$(VERSION).tar.gz

gitlab:
	# CURRENT=$(git rev-parse --abbrev-ref HEAD) && git checkout main && git push gitlab && git checkout ${CURRENT}
	bash ./deploy/gitlab.sh

deploytest: build
	python3 -m venv env
	./env/bin/pip install wheel
	./env/bin/pip install dist/gitrelease-$(VERSION).tar.gz
	-echo "source ./env/bin/activate"

patch:
	-git checkout -f
	git aftermerge patch || exit 1

minor:
	-git checkout -f
	git aftermerge minor || exit 1

major:
	-git checkout -f
	git aftermerge major || exit 1

clean:
	-rm -rf dist
	-rm -rf env

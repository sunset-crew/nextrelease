ifneq (,$(wildcard /etc/redhat-release))
    GITLIB := /usr/libexec/git-core
else
    GITLIB := /usr/lib/git-core
endif
VERSION := 0.1.10
USRLIB := /usr/local/bin
CWD=$(shell pwd)
install:
ifneq ($(shell id -u),0)
		@echo "you need to run this as root and build"
		pip3 install dist/pyfocusd-$(VERSION).tar.gz || exit 1
		@test -f $(USRLIB)/git-aftermerge || ( echo "aftermerge didn't install correctly, aborting" && exit 1 )
		@test -f $(GITLIB)/git-aftermerge || ln -s $(USRLIB)/git-aftermerge $(GITLIB)/git-aftermerge
		@echo "git-aftermerge installed"
		@test -f $(USRLIB)/git-changelog || ( echo "changelog didn't install correctly, aborting" && exit 1 )
		@test -f $(GITLIB)/git-changelog || ln -s $(USRLIB)/git-changelog $(GITLIB)/git-changelog
		@echo "git-changelog installed"
		@test -f $(USRLIB)/git-nextrelease || ( echo "nextrelease didn't install correctly, aborting" && exit 1 )
		@test -f $(GITLIB)/git-nextrelease || ln -s $(USRLIB)/git-nextrelease $(GITLIB)/git-nextrelease
		@echo "git-nextrelease installed"
		@test -f $(USRLIB)/git-versionupdater || ( echo "versionupdater didn't install correctly, aborting" && exit 1 )
		@test -f $(GITLIB)/git-versionupdater || ln -s $(USRLIB)/git-versionupdater $(GITLIB)/git-versionupdater
		@echo "git-versionupdater installed"
endif

uninstall:
ifneq ($(shell id -u),0)
		@echo "you need to run this as root"
else
		@test -f $(GITLIB)/git-aftermerge && rm -vf $(GITLIB)/git-aftermerge && echo "git-aftermerge uninstalled"
		@test -f $(GITLIB)/git-changelog && rm -vf $(GITLIB)/git-changelog && echo "git-changelog uninstalled"
		@test -f $(GITLIB)/git-nextrelease && rm -vf $(GITLIB)/git-nextrelease && echo "git-nextrelease uninstalled"
		@test -f $(GITLIB)/git-versionupdater && rm -vf $(GITLIB)/git-versionupdater && echo "git-versionupdater uninstalled"
		pip3 uninstall gitrelease
endif

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

deploytest: build
	python3 -m venv env
	./env/bin/pip install wheel
	./env/bin/pip install dist/gitrelease-$(VERSION).tar.gz
	-echo "source ./env/bin/activate"

testinstall:
ifneq ($(shell id -u),0)
		@echo "you need to run this as root"
else
		@test -f $(CWD)/env/bin/git-aftermerge || ( echo "aftermerge didn't install correctly, aborting" && exit 1 )
		@test -f $(GITLIB)/git-aftermerge || ln -s $(CWD)/env/bin/git-aftermerge $(GITLIB)/git-aftermerge
		@echo "aftermerge installed"
		@test -f $(CWD)/env/bin/git-changelog || ( echo "changelog didn't install correctly, aborting" && exit 1 )
		@test -f $(GITLIB)/git-changelog || ln -s $(CWD)/env/bin/git-changelog $(GITLIB)/git-changelog
		@echo "changelog installed"
		@test -f $(CWD)/env/bin/git-nextrelease || ( echo "nextrelease didn't install correctly, aborting" && exit 1 )
		@test -f $(GITLIB)/git-nextrelease || ln -s $(CWD)/env/bin/git-nextrelease $(GITLIB)/git-nextrelease
		@echo "nextrelease installed"
		@test -f $(CWD)/env/bin/git-versionupdater || ( echo "versionupdater didn't install correctly, aborting" && exit 1 )
		@test -f $(GITLIB)/git-versionupdater || ln -s $(CWD)/env/bin/git-versionupdater $(GITLIB)/git-versionupdater
		@echo "versionupdater installed"
endif

deploy: build
	poetry publish -r focus

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

testenv:
	mkdir ~/etc/systemd/system/
	mkdir ~/var/run/


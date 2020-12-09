ifneq (,$(wildcard /etc/redhat-release))
    GITLIB := /usr/libexec/git-core
else
    GITLIB := /usr/lib/git-core
endif
VERSION := 0.1.0
USRLIB := /usr/local/bin
CWD=$(shell pwd)
install:
ifneq ($(shell id -u),0)
		@echo "you need to run this as roo
		pip3 install gitrelease -i https://joes.focu.site/
		@test -f $(USRLIB)/git-aftermerge || ( echo "something didn't install correctly, aborting" && exit 1 )
		@test -f $(GITLIB)/git-aftermerge || ln -s $(USRLIB)/git-aftermerge $(GITLIB)/git-aftermerge
		@echo "git-aftermerge installed"
		@test -f $(USRLIB)/git-nextrelease || ln -s $(USRLIB)/git-nextrelease $(GITLIB)/git-nextrelease
		@echo "git-nextrelease installed"
endif

uninstall:
ifneq ($(shell id -u),0)
		@echo "you need to run this as root"
else
		@test -f $(GITLIB)/git-aftermerge && rm -vf $(GITLIB)/git-aftermerge && echo "git-aftermerge uninstalled"
		@test -f $(GITLIB)/git-nextrelease && rm -vf $(GITLIB)/git-nextrelease && echo "git-nextrelease uninstalled"
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
	./env/bin/pip install dist/pyfocusd-$(VERSION).tar.gz
	-echo "source ./env/bin/activate"

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


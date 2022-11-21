ifneq (,$(wildcard /etc/redhat-release))
    GITLIB := /usr/libexec/git-core
else
    GITLIB := /usr/lib/git-core
endif
VERSION := 0.4.4
USRLIB := /usr/local/bin
ADDFILES = aftermerge changelog nextrelease versionupdater
TESTADDFILES = $(addprefix ta-,$(ADDFILES))
REMOVEFILES = $(addprefix rm-,$(ADDFILES))
CWD=$(shell pwd)

install: $(ADDFILES)
$(ADDFILES):
ifneq ($(shell id -u),0)
		@echo "you need to run this as root and build"
else
		@test -f $(USRLIB)/git-$@ && ( echo "aftermerge didn't install correctly, aborting" && exit 1 )
		@test -f $(GITLIB)/git-$@ || ln -s $(USRLIB)/git-$@ $(GITLIB)/git-$@
		@echo "git-$@ installed"
endif

uninstall: $(REMOVEFILES)
$(REMOVEFILES):
ifneq ($(shell id -u),0)
		@echo "you need to run this as root"
else
		@test -f "$(GITLIB)/git-$(@:rm-%=%)" && rm -f "$(GITLIB)/git-$(@:rm-%=%)" && echo "git-$(@:rm-%=%) uninstalled" || echo "git-$(@:rm-%=%) not installed"
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

deploy: build
	sudo /usr/bin/pip3 install dist/gitrelease-$(VERSION).tar.gz

remove:
	sudo /usr/bin/pip3 uninstall -y gitrelease
	/usr/bin/pip3 uninstall -y gitrelease

deployuser: build
	/usr/bin/pip3 install --user dist/gitrelease-$(VERSION).tar.gz



deploytest: build
	python3 -m venv env
	./env/bin/pip install wheel
	./env/bin/pip install dist/gitrelease-$(VERSION).tar.gz
	-echo "source ./env/bin/activate"


testinstall: $(TESTADDFILES)
$(TESTADDFILES):
ifneq ($(shell id -u),0)
		@echo "you need to run this as root"
else
		@test -f $(GITLIB)/git-$(@:ta-%=%) && echo "$(@:ta-%=%) already installed" || ln -s "$(CWD)/env/bin/git-$(@:ta-%=%)" "$(GITLIB)/git-$(@:ta-%=%)"
		@echo "git $(@:ta-%=%) installed"
endif 

#deploy: build
#	poetry publish -r focus

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

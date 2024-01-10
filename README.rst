Git NextRelease
=================

This was built to be an easier way to do release branches. 

Install
-------

You'll need poetry and a few other things installed, like make.::

    make deploy # -- all users
    make deployuser # -- current user only
    make remove # -- removes from both current user and system

Thanks to Gitlab, we have an alternative method for you::

    pip install gitrelease --index-url https://gitlab.com/api/v4/projects/53741339/packages/pypi/simple

Let me know if you have any trouble.

Usage
-----

Basic Setup 
^^^^^^^^^^^

Make sure the repo has a remote already.

Once the links are create into your git libexec folder,

create a version file in the repo you want to track::
    
    $ export APPNAME=aftermerge
    $ echo "VERSION=0.1.0" > .version
    $ echo "APPNAME=${APPNAME}" >> .version


or if you have a poetry python project:: 

    $ poetry init or poetry new package; cd package


then give it at least a commit to work with(for either)::
    
    $ git init
    $ git commit -a -m "First Commit"


Next start the first release by typing::

    $ git nextrelease


Standard Maintainer Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will put you into the release branch directly.
As a maintainer, it's you're job to manage the release branch. 
When a task is assigned, create a branch from the release branch 
possibly with the task info::

    $ git checkout release_vx.x.x
    $ git checkout -b add_the_correct_vars_to_file
    $ git push -o origin add_the_correct_vars_to_file

Or::

    $ git current
    $ git feature <feature/fix> <name_of_branch>


Then once the developer is finished, pull and test branch::

    $ git checkout add_the_correct_vars_to_file
    $ git pull
    $ make test # or w.e. test you have
    $ make deploytest # if you have venv setup


Once you are happy with the release, create a merge request or w.e. the systems methods merging task branch with pull requests/merge requests
or do it manually::

    $ git checkout release_vx.x.x
    $ git merge add_the_correct_vars_to_file
    $ git branch -D add_the_correct_vars_to_file
    $ git push --force


Once you have your release ready, merge it into master or main via a system like github, gitlab
or do it manually::

    $ git checkout main
    # you need to force the merge commit --no-ff
    $ git merge --no-ff release_vx.x.x
    $ git branch -D release_vx.x.x
    $ git push --force


After the merge into master/main
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once everything is merged into main you run::

    $ git aftermerge patch # or minor or major


This sets up a tag and everyhing, now we can add the funzies:: 

    $ git versionupdater install
    $ git changelog install


Make sure to review the versionupdater.json to make sure its updating the files you need updated.

Once you finish, test the changelog::

    $ git changelog adds changelog and versionupdater


This should complete and add the commit automagically. 
Now develop and try not to use pre-commit hooks.

Some helpful git commands are::

    $ git rebase -i <a commit>
    $ "edit the commits"
    $ git commit --amend --reset-author
    $ git rebase --continue


Testing
-------

Suite. real, Suite
^^^^^^^^^^^^^^^^^^

Give it a shot, I'm always down to see if it works. 

You'll need a project called: glab. Which also has it's own release system that I haven't tried yet because I don't want to demoralize myself.

All in good time.

It's recommended that you run ::

    make deploytest 
    sudo make testinstall


The second command maps it to a centos or debian install. Let me know of other common locations and I'll add them.

If I didn't say it already, you're gonna need git2 or greater.:: 

    $ ./tests/suite short


It should fail at the various commands to look at. I may add some bright colors too... maybe


Verb Index
----------

Added
^^^^^
added
adds
comments
installs
loads


Changed
^^^^^^^
changed
changes
configures
decouples
deploys
edits
fixes
finishes
moves
prevents
renames
repairs
replaces
refactors
restores
returns
sets
splits
updates
uncouples
wires
wraps


Removed
^^^^^^^
removed
removes
cleans
uncomment

Git NextRelease
=================

This was built to be an easier way to do release branches. 

Usage
-----

Basic Setup 
^^^^^^^^^^^

Make sure the repo has a remote already.

once the links a create into your git libexec folder. 

Create a version file::

    $ cat 'VERSION=0.1.0' > .version

    or if you have a poetry python project, 

    $ poetry init or poetry new package; cd package


Next start the first release by typing::

    $ git nextrelease


Standard Workflow
^^^^^^^^^^^^^^^^^

This will put you into the release branch directly.
As a maintainer, it's you're job to manage the release branch. 
When a task is assigned, create a branch from the release branch 
possibly with the task info::

    $ git checkout release_v0.1.0
    $ git checkout -b add_the_correct_vars_to_file
    $ git push -o origin add_the_correct_vars_to_file


Then once the developer is finished, pull and test branch::

    $ git checkout add_the_correct_vars_to_file
    $ git pull
    $ make test # or w.e. test you have


Once you have happy, create a merge request or w.e. the systems methods merging task branch with release branch
or do it manually::

    $ git checkout release_v0.1.0
    $ git merge add_the_correct_vars_to_file
    $ git branch -D add_the_correct_vars_to_file
    $ git push --force


Once you have your release ready, merge it into master or main via a system
or do it manually::

    $ git checkout main
    $ git merge release_v0.1.0
    $ git branch -D release_v0.1.0
    $ git push --force


After the merge into master/main
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once everything is merged into main you run::

    $ git aftermerge patch # or minor for minor versions, major for major versions


This sets up a tag and everyhing, now we can add the funzies:: 

    $ git versionupdater install
    $ git changelog install


Make sure to review the versionupdater.json to make sure its updating the files you need updated.

Once you finish, test the changelog::

    $ git changelog adds changelog and versionupdater


This should complete and add the commit automagically. 
Now develop and try not to use pre-commit hooks.

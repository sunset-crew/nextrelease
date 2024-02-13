# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[Also based on](https://github.com/conventional-changelog/standard-version/blob/master/CHANGELOG.md) so decending.

## [0.5.7] - 2024-02-13
### Added
- adds separates to change_verb_list

## [0.5.6] - 2024-01-10
### Added
- adds the push tags and the tag only running of the deploy

## [0.5.5] - 2024-01-10
### Changed
- updates the poetry packages

## [0.5.4] - 2024-01-10
### Removed
- removes additional deploy nonsense

## [0.5.3] - 2024-01-10
### Added
- adds minor update to gitlabci

## [0.5.2] - 2024-01-10
### Changed
- changes the limitations of the gitlab deploy

## [0.5.1] - 2024-01-10
### Added
- adds gitlab deploy to makefile
- adds deploy code

## [0.5.0] - 2024-01-10
### Added
- adds gitlab-ci support so we can make these releases public
- adds public registry for the package

### Changed
- changes the gitlab ci script
- changes the gitlab ci script again
- changes the gitlab ci script again 1
- changes the gitlab ci script again 2
- changes the gitlab ci script again 4
- changes the gitlab ci script again 5

## [0.4.10] - 2024-01-10
### Added
- adds support for nodejs repos

## [0.4.9] - 2023-11-18
### Changed
- fixes issue with versionupdater being run after aftermerge

## [0.4.8] - 2023-04-08
### Added
- adds custom spacing configuration via config file
- adds rust repository processing

### Changed
- updates versionupdater to include cargo.toml
- fixes error with rust support add

## [0.4.7] - 2023-02-28
### Added
- adds trunk_branch env var for different trunk to check release out from
- adds feature example in readme
- adds description text to pyproject
- adds config file for default separator of fix and feature

### Changed
- changes fixor to feature
- fixes the fixfeature section adding a blocker if a name is not provided
- updates requests module

## [0.4.6] - 2022-12-21
### Changed
- updates release to match present tags
- fixes issue with changelog repeating data on changelog for first setup
- changes to proper version name

## [0.4.5] - 2022-11-21
### Added
- adds .version json for versionupdater data file

## [0.4.4] - 2022-11-05
### Added
- adds extra git notes for resetting git information

## [0.4.2] - 2022-11-04
### Added
- adds gitea merge commit parsing method
- adds the fixor command to the mix

### Removed
- removes fixorfeat.py file as a clean up action

## [0.4.1] - 2022-02-21
### Changed
- updates the package versioning for 3.7

## [0.4.0] - 2021-12-29
### Added
- adds no-ff to merge command and separates vars for .version in docs

### Removed
- removes the wordplay class since it was unused

### Changed
- refactors the verbs into their own list variables

## [0.3.10] - 2021-11-28
### Added
- adds better deployment getting you up and going
- adds remove and rewrites deploy function for make
- adds additional check for poetry binary in the path

## [0.3.9] - 2021-10-11
### Added
- adds moves word to the changelog system
- adds and organizes the change words
- adds more words to the changelog system
- adds temporary fix section
- adds wires word
- adds uncouples to word list

## [0.3.8] - 2021-08-17
### Added
- adds deploys keyword for changes
- adds captured error for leading verb on changelog messages
- adds verb list to readme

## [0.3.7] - 2021-07-10
### Added
- adds better readme notes and directions
- adds more detailed documentation

### Removed
- removes actual numbers in version examples replaces with xs

### Changed
- fixes bad leading word for the changelog actions

## [0.3.6] - 2021-07-10
### Added
- adds test suite and refactors a lot
- adds better notes to test suite

## [0.3.5] - 2021-06-30
### Added
- adds details to readme.rst

### Changed
- updates the readme.rst with the common workflow

## [0.3.4] - 2021-06-30
### Added
- adds main branch identification for github

## [0.3.3] - 2021-05-18
### Changed
- decouples poetry from the version updater into a .version file

## [0.3.2] - 2021-04-27
### Changed
- fixes the quotes issue with the merge request name

## [0.3.1] - 2021-04-27
### Added
- adds title for the merge request

### Changed
- fixes issue with forming the git command

## [0.3.0] - 2021-04-27
### Added
- adds more descriptions to the various changelog areas
- adds refactors to the changed keywords
- adds auto merge generation

## [0.2.1] - 2021-02-09
### Added
- adds refactored changelog install and uninstall
- adds github support to the application
- adds release branch scanner for other branches

### Changed
- fixes pre and post issue after refactor

## [0.2.0] - 2021-01-08
### Added
- adds release notes for the basics

## [0.1.11] - 2021-01-08
### Added
- adds testrepo scriopt so thta i can test the repo and junk
- adds better testing script that cleans up after itself

## [0.1.10] - 2021-01-07
### Added
- adds no-remotes option to remove push, fetch and pull from running
- adds testrepo tarball

## [0.1.9] - 2021-01-02
### Changed
- fixes issues with aftermerge failure found in 0.1.8

## [0.1.8] - 2021-01-02
### Added
- adds fix for extra quotes in the bump title
- adds fixes for run_update system
- adds fixes to the list of things i can start with

### Changed
- changes cli logic
- changes fixes increment error
- fixes possible install issue

## [0.1.7] - 2021-01-02
### Added
- adds sphinx documentation to the project
- adds formating fixes and moves documentation to dev dep

### Removed
- removes code that ties builds to install in root makefile

### Changed
- changes python version to work on centos

## [0.1.6] - 2020-12-31
### Added
- adds .gitignore update to version updater
- adds gitignore version updater json
- adds fixe for install process

## [0.1.5] - 2020-12-26
### Added
- adds formating to improve commit msg history

## [0.1.4] - 2020-12-26
### Added
- adds automated git commit with changelog

## [0.1.3] - 2020-12-26
### Added
- adds changelog management to this repo

## [0.1.0] - 2020-12-22
### Added
- bot - adds changelog
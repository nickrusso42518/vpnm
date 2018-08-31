# File:    Makefile
# Version: GNU Make 3.81
# Author:  Nicholas Russo (njrusmc@gmail.com)
# Purpose: Phony targets used for linting (YAML/Python) and running
#          the script for some quick testing. Unit tests may be
#          added in the future. See .travis.yml for invocation.
.PHONY: all
all:	lint unit pb

.PHONY: lint
lint:
	@echo "Starting  lint"
	find . -name "*.yml" | xargs yamllint -s
	find . -name "*.py" | xargs pylint
	find . -name "*.py" | xargs bandit
	@echo "Completed lint"

.PHONY: unit
unit:
	@echo "Starting  unit tests"
	ansible-playbook tests/unittest_playbook.yml
	@echo "Completed unit tests"

.PHONY: pb
pb:
	@echo "Starting  playbook tests"
	ansible-playbook tests/test_playbook.yml
	@echo "Completed playbook tests"

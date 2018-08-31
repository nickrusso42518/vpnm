# File:    Makefile
# Version: GNU Make 3.81
# Author:  Nicholas Russo (njrusmc@gmail.com)
# Purpose: Phony targets used for linting (YAML/Python) and running
#          the script for some quick testing. The 'test' target runs
#          the lint, unit testing, and playbook testing in series.
#          Individual targets can be run as well, typically for CI.
#          See .travis.yml for the individual target invocations.
.PHONY: test
test:	lint unit pb

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
	ansible-playbook tests/test_playbook.yml --skip-tags "do_ssh"
	@echo "Completed playbook tests"

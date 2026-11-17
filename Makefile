# SPDX-License-Identifier: Apache-2.0
PYTHON ?= python3

.PHONY: check citations style links findings claims leaks history hooks test
check: style links findings claims leaks history test

style:
	$(PYTHON) scripts/style_check.py

links:
	$(PYTHON) scripts/check_links.py

findings:
	$(PYTHON) scripts/validate_findings.py
	$(PYTHON) scripts/render_findings.py --check

claims:
	$(PYTHON) scripts/validate_claims.py

leaks:
	$(PYTHON) scripts/leak_guard.py

history:
	$(PYTHON) scripts/check_commit_msg.py --range HEAD

# Turn on the commit hooks in this clone.
hooks:
	git config core.hooksPath .githooks

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

# Needs a kernel checkout at the commit in targets/verified-at.txt: make citations KERNEL_DIR=../microkernel
citations:
	@test -n "$(KERNEL_DIR)" || { echo "set KERNEL_DIR to a kernel checkout"; exit 2; }
	$(PYTHON) scripts/check_citations.py ours "$(KERNEL_DIR)"

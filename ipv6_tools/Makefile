# Makefile targets simplify daily operatons

.DEFAULT_GOAL := all
.PHONY: all
all:	clean lint run

.PHONY: lint
lint:
	@echo "Starting  lint"
	find . -name "*.yml" | xargs yamllint --strict
	find . -name "*.py" | xargs pylint
	find . -name "*.py" | xargs black -l 80 --check
	@echo "Completed lint"

.PHONY: run
run:
	@echo "Starting  test runs"
	python ans_inv_from_eui64.py
	python ans_inv_from_eui64.py fc00::
	@echo "Completed test runs"

.PHONY: clean
clean:
	@echo "Starting  clean"
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -f hosts.yml
	@echo "Completed clean"

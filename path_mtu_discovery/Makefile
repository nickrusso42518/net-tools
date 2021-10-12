# Makefile targets simplify daily operatons

.DEFAULT_GOAL := all
.PHONY: all
all:	clean lint run

.PHONY: run
run:	run4 run6

.PHONY: lint
lint:
	@echo "Starting  lint"
	find . -name "*.yml" | xargs yamllint --strict
	find . -name "*.py" | xargs pylint
	find . -name "*.py" | xargs black -l 80 --check
	@echo "Completed lint"

.PHONY: run4
run4:
	@echo "Starting  IPv4 test runs"
	python pmtud.py -e 1500
	python pmtud.py -d 8.8.4.4 -l 1402 -u 1549 -r 2 -t 2 -e 1500
	@echo "Completed IPv4 test runs"

.PHONY: run6
run6:
	@echo "Starting  IPv6 test runs"
	python pmtud.py -d 2001:4860:4860::8888 e 1500
	python pmtud.py -d 2001:4860:4860::8844 -u 2000 -r 3 -t 2 -e 1500
	@echo "Completed IPv6 test runs"

.PHONY: clean
clean:
	@echo "Starting  clean"
	find . -name "*.pyc" -exec rm -rf {} \;
	@echo "Completed clean"

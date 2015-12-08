.PHONY: all pep8 pyflakes clean test check

all:
	@echo 'pep8              check pep8 compliance'
	@echo 'pyflakes          check for unused imports (requires pyflakes)'
	@echo 'clean             cleanup the source tree'
	@echo 'test              run the unit tests'
	@echo 'check             make sure you are ready to commit'

pep8:
	@pep8 drip.py drip_tests.py

pyflakes:
	@pyflakes drip.py drip_tests.py

clean:
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete

test: clean
	@PYTHONPATH=. py.test --cov-report term-missing --cov drip.py drip_tests.py

check: pep8 pyflakes test
	@coverage report | grep 100% >/dev/null || { echo 'Unit tests coverage is incomplete.'; exit 1; }

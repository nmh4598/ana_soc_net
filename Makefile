install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv test_hello.py

format:
	black .

lint:
	pylint $(git ls-files '*.py')

all: install lint test
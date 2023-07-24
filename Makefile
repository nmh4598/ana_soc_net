install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	black .
	pylint **/*.py
	flake8 **/*.py

test:
	python -m pytest /test

all: install lint test
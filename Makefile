run:
	pipenv run python RuleNameGen.py

format:
	pipenv run isort .
	pipenv run black .

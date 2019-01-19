.PHONY: pip-compile pip-install lint type

setup:
	$(shell which python3.7) -m venv venv; pip install pip-tools

pip-compile:
	source venv/bin/activate; pip-compile requirements.in

pip-install:
	source venv/bin/activate; pip install -r requirements.txt; pip install -r requirements-e.txt

lint:
	source venv/bin/activate; flake8 apophis/
	
type:
	source venv/bin/activate; mypy --ignore-missing-imports apophis/;

build: pip-install lint type

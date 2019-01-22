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
	source venv/bin/activate; mypy --ignore-missing-imports apophis/

db-migrate:
	flyway -url=jdbc:postgresql://localhost:15432/apophis -locations=filesystem:./migrations -user=postgres -password=postgres migrate

db-clean:
	flyway -url=jdbc:postgresql://localhost:15432/apophis -locations=filesystem:./migrations -user=postgres -password=postgres clean

build: pip-install lint type

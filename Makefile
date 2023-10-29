.PHONY: local

# Generate an image of the models in the system.
graph:
	./manage.py graph_models

coverage:
	pytest --cov=social --migrations -n 2 --dist loadfile

# fcov == "fast coverage" by skipping migrations checking. Save that for CI.
fcov:
	@echo "Running fast coverage check"
	@pytest --cov=social -n 4 --dist loadfile -q

install:
	pip install --upgrade pip && pip-compile requirements.in && pip install -r requirements.txt

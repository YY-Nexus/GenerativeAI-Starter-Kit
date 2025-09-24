init:
    python3.11 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

check:
    python check-deps.py

test:
    pytest

build:
    python setup.py sdist bdist_wheel

publish:
    twine upload dist/

release:
    bump-my-version patch && make build && make publish

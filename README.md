Create a new virtual environment and install the dependencies

```
py -3.8 -m venv .venv
.venv\scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install
```
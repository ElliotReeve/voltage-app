# Voltage App


## Getting started

We use Poetry to manage dependencies and virtual environments. If you don't have it yet:

- on macOS, you can just run `brew install poetry`;
- on other platforms, consult [Poetry Installation](https://python-poetry.org/docs/#installation).

Then:

```sh
git clone git@github.com:ElliotReeve/voltage-app.git
cd voltage-app
cp .env.example .env
# Modify .env to suit your needs, in particular, specify DATABASE_URL
poetry install
```

Run the server:

```sh
poetry run uvicorn app.main:app --reload
```

Your API documentation should show up at <http://127.0.0.1:8000/docs>. Server will automatically reload when you save your code – no need to restart it by hand.

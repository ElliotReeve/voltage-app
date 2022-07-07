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

Deploy:
```ssh
# Build docker image
docker build --force-rm -t voltage_app .
# Save docker image
docker save -o <path for generated tar file> <image name>
# Transfer docker image to server
scp file.txt remote_username@10.10.0.2:/remote/directory
# Load docker image
docker load -i <path to image tar file>
# Run docker container
docker run \
-itd \
--name voltage_app \
--restart=always \
-e 'DATABASE_URL=mysql+mysqldb://root@127.0.0.1/voltage' \
-p 4000:4000 \
--network=host \
voltage_app:latest
```
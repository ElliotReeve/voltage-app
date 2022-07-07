FROM python:3.10
WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /app/

# poetry-core needs the package to exist, so we add an empty __init__.py temporarily:
RUN mkdir ./app && \
    touch ./app/__init__.py && \
    pip install --no-cache-dir . && \
    rm ./app/__init__.py

COPY ./ /app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4000"]
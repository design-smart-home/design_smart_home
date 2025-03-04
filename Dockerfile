FROM python:3.11.9-slim

COPY pyproject.toml pyproject.toml
RUN pip install poetry
RUN poetry install

COPY . .

CMD [ "python", "main.py" ]
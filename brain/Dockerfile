FROM python:3.12-slim

WORKDIR /app

ENV PIPENV_VENV_IN_PROJECT=true
COPY brain/Pipfile ./brain/
RUN pip install pipenv && cd brain && pipenv install

COPY . .

EXPOSE 8000

CMD ["uvicorn", "brain.main:app", "--host", "0.0.0.0", "--port", "8000"]

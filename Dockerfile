FROM python:3.9

WORKDIR /app

# COPY requirements.txt .
COPY ./app .
RUN pip install -r requirements.txt

COPY ./config.yml .


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

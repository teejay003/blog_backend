FROM python:3-alpine

WORKDIR /app

RUN apk add --no-cache gcc libffi-dev musl-dev postgresql-dev py3-virtualenv

COPY requirements.txt . 

RUN python -m venv venv && \
    source venv/bin/activate && \
    venv/bin/pip install --no-cache-dir -r requirements.txt

COPY app app/

COPY .env .

EXPOSE 8000

CMD ["venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
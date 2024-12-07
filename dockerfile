FROM python:3.11-alpine


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    build-base \
    bash

WORKDIR /usr/app/

COPY requirements.txt /usr/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
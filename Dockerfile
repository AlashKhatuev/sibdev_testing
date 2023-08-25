FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install -r requirements.txt

WORKDIR /app/sibdevtesting

RUN python manage.py migrate

EXPOSE 8000

# RUN gunicorn --workers=3 sibdevtesting.wsgi 
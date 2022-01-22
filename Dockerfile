# pull the official base image
FROM python:3.8.12-bullseye

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install django
RUN pip install django-clear-cache
RUN python -m pip install django-crispy-forms --default-timeout=1000
RUN python -m pip install transformers --default-timeout=1000
RUN python -m pip install torch --default-timeout=1000

# copy project
COPY . /usr/src/app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
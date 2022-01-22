# pull the official base image
FROM python:3.8.10-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install django
RUN pip install django-crispy-forms
RUN pip install sentencepiece
RUN pip install transformers
RUN pip install torch

# copy project
COPY . /usr/src/app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
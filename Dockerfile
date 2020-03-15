FROM python:3.8.0-alpine

RUN mkdir /code
WORKDIR /code
# set work directory

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOSTDOCKER="127.0.0.1 localhost [::1]"
ENV DEBUG=False
ENV SECRET_KEY="4-n!nq53u)+sr8pe#%4rzwx^9fmklasob_k*tm9!^)7@9o@@5i"

ENV EMAIL_HOST="smtp.yandex.ru"
ENV EMAIL_HOST_USER="denisdolmatov2020@yandex.ru"
ENV EMAIL_HOST_PASSWORD="DenVik37ww"

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt


# copy project
COPY . /code/
# base python 3 image
FROM python:3.8.1-alpine

# install psycopg2 dependencies
RUN apk update \
    && apk add gcc musl-dev postgresql-dev python3-dev

# installs and sets timezone for Brazil
RUN apk add --update tzdata
ENV TZ=America/Sao_Paulo

# sets work directory and copy all files to work directory
WORKDIR /app
COPY . /app

# set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# update pip and install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# exposes Flask port
EXPOSE 5000

# change permission and execute entrypoint
RUN chmod +x ./boot.sh
ENTRYPOINT ["./boot.sh"]
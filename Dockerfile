FROM python:3.7.16-slim-buster

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install git nodejs npm libpq-dev gcc build-essential -y --no-install-recommends

RUN pip install gunicorn==20.0.4

ADD requirements.txt /opt/requirements.txt
RUN pip3 install -r /opt/requirements.txt

COPY . /opt/app

WORKDIR /opt/app

RUN npm install
RUN npx gulp compile

RUN mkdir -p /opt/staticfiles
RUN python3 manage.py collectstatic --noinput

CMD ["gunicorn", "-b 0.0.0.0:8000", "moscowdjango.wsgi:application"]
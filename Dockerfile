FROM python:3.7.4-alpine

MAINTAINER Jonathan Sharpe <mail@jonrshar.pe>

RUN apk update
RUN apk add ca-certificates
RUN update-ca-certificates

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY setup.py /usr/src/app
COPY README.rst /usr/src/app
COPY /flash /usr/src/app/flash

RUN python3 setup.py develop

COPY /scripts /usr/src/app/scripts
COPY config.json /usr/src/app

EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD [ "./scripts/launch.py" ]

FROM python:3.7.4-alpine

MAINTAINER Jonathan Sharpe <mail@jonrshar.pe>

RUN apk update
RUN apk add ca-certificates
RUN update-ca-certificates

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt .
COPY setup.py .
COPY README.rst .
COPY /flash ./flash

RUN python setup.py install

COPY launch.py .
COPY config.json .

ENV PORT=5000
EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD [ "./launch.py" ]

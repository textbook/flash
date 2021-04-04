FROM python:3.9.2-alpine

LABEL maintainer="Jonathan Sharpe <mail@jonrshar.pe>"

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

ENV PORT=80
EXPOSE 80

ENTRYPOINT [ "python3" ]
CMD [ "./launch.py" ]

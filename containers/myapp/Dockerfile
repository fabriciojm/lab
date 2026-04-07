FROM ubuntu:24.04

RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY greet .

CMD ["./greet"]

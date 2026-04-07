FROM ubuntu:24.04
WORKDIR /app
COPY . .
RUN chmod u+x greet
ENV GREETING="Bonjour"
ENV NAME="le monde"
CMD ["./greet"]

FROM ubuntu:24.04

WORKDIR /app

COPY backup .
RUN chmod +x backup

# Hard-coded command
ENTRYPOINT ["./backup"]

# CMD is an argument
CMD ["list"]

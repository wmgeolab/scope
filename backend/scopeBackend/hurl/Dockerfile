FROM alpine:latest

RUN apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing hurl

# Set the working directory inside the container
WORKDIR /app

# Copy all Python files into the container
COPY *.py /app/

ENTRYPOINT ["/bin/sh", "-c", "hurl *.py --variable host=${HOST:-backend:8000}"]
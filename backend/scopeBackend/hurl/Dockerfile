# Start with the Hurl image
FROM ghcr.io/orange-opensource/hurl:latest

# Set the working directory inside the container
WORKDIR /app

# Copy all Python files into the container
COPY *.py /app/

ENTRYPOINT ["/bin/sh", "-c", "hurl *.py --variable host=${HOST:-backend:8000}"]
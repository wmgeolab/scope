FROM docker.io/library/node:22.9-slim

WORKDIR /app
RUN apt update && apt install -y curl && apt clean

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

# Add a startup script
COPY <<EOF /start.sh
#!/bin/sh
npm start -- --host 0.0.0.0
EOF

RUN chmod +x /start.sh
CMD ["/start.sh"]

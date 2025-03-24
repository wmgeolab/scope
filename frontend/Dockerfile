FROM docker.io/library/node:22.9-slim AS build

WORKDIR /app
RUN apt update && apt install -y curl && apt clean

COPY package*.json /app
RUN npm install

COPY . /app

EXPOSE 3000

CMD ["npm", "run", "start"]

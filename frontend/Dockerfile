FROM docker.io/library/node:21-slim AS build

ENV NODE_ENV=production

ENV NODE_OPTIONS=--openssl-legacy-provider

EXPOSE 3000

WORKDIR /app

COPY package.json /app/package.json
RUN npm install

COPY . /app

RUN npm run start

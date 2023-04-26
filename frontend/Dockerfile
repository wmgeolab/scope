FROM docker.io/library/node:18-slim AS build

ENV NODE_ENV=production

WORKDIR /app

COPY package.json /app/package.json
RUN npm install

COPY . /app
RUN npm run build

RUN npm install \
    && npm run build

FROM docker.io/library/nginx:latest

COPY --from=build /app/build /usr/share/nginx/html
FROM docker.io/library/node:22.9-slim AS build

WORKDIR /app

COPY package*.json /app
RUN npm install

COPY . /app

EXPOSE 3000

CMD ["npm", "run", "start"]

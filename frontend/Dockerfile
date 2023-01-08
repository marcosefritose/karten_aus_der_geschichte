
FROM node:19-alpine

WORKDIR /test-app

COPY ./package*.json ./

RUN npm ci
COPY . .
RUN npm run build

CMD npm rebuild esbuild && npm run dev -- --host
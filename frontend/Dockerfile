FROM node:19-alpine
ENV NODE_ENV development

RUN mkdir -p /home/node/app
WORKDIR /home/node/app

COPY ./package*.json ./
RUN npm install
#RUN npm ci
#COPY . .
#RUN npm run build

#CMD ["npm", "run", "dev"]
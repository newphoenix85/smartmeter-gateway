FROM node:current-slim

WORKDIR /srv/app
COPY package.json ./
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]

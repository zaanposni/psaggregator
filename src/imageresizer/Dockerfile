FROM node:20

WORKDIR /app
COPY package*.json ./

RUN npm install

COPY . ./

RUN npm run build

RUN rm -rf src

ENV NODE_ENV=production
ENV PORT=3000
EXPOSE 3000

CMD ["node", "dist/index.js"]

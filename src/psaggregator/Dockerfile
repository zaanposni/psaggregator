FROM node:20

WORKDIR /app
COPY package*.json ./

RUN npm install

COPY . ./

RUN npm run prismagenerate

RUN npm run build

EXPOSE 3000
ENV NODE_ENV=production
CMD npx prisma migrate deploy --schema ./src/config/schema.prisma && node build
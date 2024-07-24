FROM node:20-slim
RUN npm install -g http-server
WORKDIR /frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 80
CMD [ "http-server", "dist", "-p", "80", "-P", "http://localhost:80?" ]
# Stage 0, "build-stage", based on Node.js, to build and compile Angular
FROM node:14-alpine as build-stage
WORKDIR /app
COPY package*.json /app/
RUN npm install
COPY ./ /app/
RUN npm run build

# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:1.15-alpine
COPY --from=build-stage /app/dist/front/ /app/front/
COPY ./nginx-custom.conf /etc/nginx/conf.d/default.conf

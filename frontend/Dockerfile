FROM node:18-alpine as builder
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Segurança: Executar nginx sem root
RUN touch /var/run/nginx.pid &&     chown -R nginx:nginx /var/run/nginx.pid /usr/share/nginx/html /var/cache/nginx /var/log/nginx

USER nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

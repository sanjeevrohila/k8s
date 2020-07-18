FROM debian:stretch-slim

LABEL maintainer="Sanjeev Rohila <justsanjeev@gmail.com>"

# Install NGINX
RUN set -x \
 && apt-get update && apt-get install nginx -y

COPY default.conf /etc/nginx/conf.d

COPY nginx.conf /etc/nginx

EXPOSE 80

STOPSIGNAL SIGTERM

CMD ["nginx", "-g", "daemon off;"]

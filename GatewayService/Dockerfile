FROM nginx:latest

COPY ./nginx_reverse_proxy.conf /etc/nginx/conf.d/default.conf
COPY ./nginx_proxy_params.conf /etc/nginx/proxy_params

EXPOSE 80 

CMD ["nginx", "-g", "daemon off;"]

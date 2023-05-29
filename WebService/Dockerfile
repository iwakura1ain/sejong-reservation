# based on nginx image 
FROM nginx:1.23.4-alpine

#ENV NJS_VERSION   %%NJS_VERSION%%

# copy project into container at /vue-project
COPY /WebService/vue-project /vue-project

# copy nginx config into container at
COPY /WebService/nginx.conf /etc/nginx/nginx.conf

# Set the working directory to /dist
# NOTE: all the directives that follow in the Dockerfile will be executed in
# that directory.
WORKDIR /vue-project

# check nginx configs
RUN nginx -t

# nginx logs to stdout/stderr
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log  

# install nodejs and npm and icu data
RUN apk add nodejs npm=9.1.2-r0 icu-data-full=72.1-r1


# install npm dependencies from package.json
RUN npm install

# run tests
#RUN npm test

# build vue project
RUN npm run build

# expose port 80 
EXPOSE 80

# start nginx
CMD ["nginx-debug", "-g", "daemon off;"]






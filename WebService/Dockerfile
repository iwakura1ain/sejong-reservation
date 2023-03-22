FROM nginx:1.23.3-alpine 



# Copy the package.json and install dependencies
COPY WebApp /WebApp/
RUN npm install

WORKDIR /WebApp

# Build the project
RUN npm run build


FROM nginx:alpine as production-build
COPY nginx.conf /etc/nginx/nginx.conf

## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

# Copy from the stahg 1
COPY --from=builder /WebApp/dist /usr/share/nginx/html

EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]


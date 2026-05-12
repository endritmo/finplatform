FROM nginx:alpine

# Remove default nginx config
RUN rm -rf /usr/share/nginx/html/* /etc/nginx/conf.d/default.conf

# Copy all frontend static files
COPY . /usr/share/nginx/html

# Copy the nginx template — the official nginx:alpine image processes
# /etc/nginx/templates/*.conf.template with envsubst at container startup.
# It writes the result to /etc/nginx/conf.d/default.conf automatically.
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

EXPOSE 80
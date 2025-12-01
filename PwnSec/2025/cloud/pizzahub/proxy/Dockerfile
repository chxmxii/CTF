FROM nginx:1.29-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/nginx.conf

RUN chmod -R 644 /etc/nginx && \
    chown -R nginx:nginx /etc/nginx

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

FROM nginx:1.21
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
RUN rm -f /etc/nginx/conf.d/default.conf

COPY *.conf /etc/nginx/conf.d/

ENTRYPOINT ["entrypoint.sh"]
#!/bin/sh

sed -i "s/UPSTREAM_APP/$UPSTREAM_APP/g" /etc/nginx/conf.d/app.conf

if [ -z "$1" ]; then
  exec nginx -g 'daemon off;'
fi

exec "$@"

#!/bin/bash -xe
QUERY='select * from comments'
SERVICE=postgres
docker-compose run --rm $SERVICE bash -c "PGPASSWORD=\$POSTGRES_PASSWORD psql -h $SERVICE -U \$POSTGRES_USER \$POSTGRES_DB -c '$QUERY'"
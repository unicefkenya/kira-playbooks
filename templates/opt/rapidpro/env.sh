#!/bin/bash
export PRODUCTION=0
export DATABASE_URL="postgresql://{{ pgsql_user }}:{{ pgsql_password }}@{{ pgsql_host }}/{{ pgsql_db }}"
export REDIS_HOST=localhost
export REDIS_DATABASE=8
export TEMBA_HOST={{ nginx_server_name }}
export TEMBA_AUTH_TOKEN='{{ temba_auth_token}}'
export TWITTER_API_KEY='{{ twitter_api_key }}'
export TWITTER_API_SECRET='{{ twitter_api_secret }}'
export SEGMENTIO_WRITE_KEY=
export SENTRY_DSN=
export LIBRATO_EMAIL=
export LIBRATO_API_TOKEN=
exec "$@"

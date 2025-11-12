.PHONY: up down build logs api worker

build:
\tdocker compose build

up:
\tdocker compose up -d

down:
\tdocker compose down

logs:
\tdocker compose logs -f --tail=200

api:
\tdocker compose exec api bash

worker:
\tdocker compose exec worker bash
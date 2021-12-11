# Munibot API

## Running it locally

Run with Docker. First build it:

    docker build -t munibot-backend .

Then run it, mounting the main SQLite database as a volume: 

    docker run -d --name munibot-backend -p 80:80 -v /source/to/munibot.sqlite:/opt/munibot/munibot.sqlite munibot-backend

## Production setup

[Traefik](https://traefik.io/traefik/) acts as a reverse proxy, handling SSL automatically. Configured to run at https://api.munibot.amercader.net:

    docker-compose up -d

# Munibot API

Run with Docker. First build it:

    docker build -t munibot-backend .

Then run it, mounting the main SQLite database as a volume: 

    docker run -d --name munibot-backend -p 80:80 -v /source/to/munibot.sqlite:/opt/munibot/munibot.sqlite munibot-backend

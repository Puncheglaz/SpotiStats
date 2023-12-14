# SpotiStats

Spotify analytics and music data visualization service.

## Run

Requires docker and docker-compose.

You can customize some parameters in `src/.env` file.

To start services:

```bash
cd src
sudo docker-compose up -d
```

Web-service will be available at port WEB_PORT (see .env).

To stop:

```bash
sudo docker-compose down
```

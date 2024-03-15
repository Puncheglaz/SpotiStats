![spotistats_logo](https://github.com/TheTedLab/SpotiStats/assets/71270225/2fe17957-f07f-4e0b-80b6-2e27943d14d5)

## Table of contents
* [Introduction](https://github.com/TheTedLab/SpotiStats#introduction)
* [Contributors](https://github.com/TheTedLab/SpotiStats#contributors)
* [Setup](https://github.com/TheTedLab/SpotiStats#setup)
* [Screenshots](https://github.com/TheTedLab/SpotiStats#screenshots)

## Introduction
Spotify analytics and music data visualization service.

## Contributors
1. [TheTedLab](https://github.com/TheTedLab)
2. [Puncheglaz](https://github.com/Puncheglaz)
3. [Mephodio](https://github.com/Mephodio)

## Setup

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

## Screenshots
<img width="1458" alt="interface" src="https://github.com/TheTedLab/SpotiStats/assets/71270225/b53454a2-577e-41b0-bb22-256e8184d75c">

# apophis
A Discord bot

[![Build Status](https://travis-ci.org/PacketFire/apophis.svg?branch=master)](https://travis-ci.org/PacketFire/apophis)

## Dependencies
* Docker along with `docker-compose`
* Python 3.6+
* `ffmpeg`

## Installation
Make sure you have dependencies above installed in your system.

Rest of the steps can be summarized as:
```shell
$ git clone https://github.com/PacketFire/apophis
$ cd apophis
$ make setup
$ make pip-install
```

Initialize Docker containers which will install Postgres and Flyway DB
```shell
$ docker-compose up postgres
$ docker-compose run flyway-migrate
```

## Running
You need to get token for your Bot. [This](https://discordpy.readthedocs.io/en/rewrite/discord.html) might be useful.

Steps thereafter look similar to this:
```shell
$ docker-compose up postgres
$ source venv/bin/activate
$ BOT_TOKEN=<your_bot_token> python apophis
```
**NOTE**: Above steps assume that you are inside `apophis`'s root directory (one that contains `Makefile` and `Dockerfile`)

If everything is alright, your bot should be running. You can invoke some commands like `!define discord` to test it.

**NOTE**: If you are running the bot for the first time, please read instructions below.

When attempting to run commands like `!music`, you will be greeted with "Unauthorized".
For other commands like downloading `music` and adding other users to access list, you need to add yourself (your Discord ID to be precise) to list of authorized users.

To do so you will need your Discord ID which can be found by following [these](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-) steps.

Once that is out of the way, you need to connect to Postgres container, and add your Discord ID to `permissions` table. These steps can be summarized (and visualized as)
```shell
$ docker exec -it <your_containers_name> psql -U postgres
postgres=# \c apophis
postgres=# INSERT INTO permissions (username, level) VALUES (<your_discord_id>, 2);
```

You can find your container name under column named `NAMES` after running `docker ps`.

Aaaaannnd you are done!

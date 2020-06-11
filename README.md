# カオリ

[![CI](https://github.com/austinpray/kaori/workflows/CI/badge.svg?branch=master&event=push)](https://github.com/austinpray/kaori/actions?query=workflow%3ACI)

Hi there! I am a slack bot with functionality that ranges from "useless" to "pretty neat".

## [Plugins](kaori/plugins)

My features are implemented as plugins. They can be enabled, disabled, featured flagged independently.

### [`ping`](kaori/plugins/ping.py)

My "hello world" plugin. If you say "ping", I'll say "pong".

### [Gacha card game](kaori/plugins/gacha)

Create, collect, battle gacha cards.

### [Kkreds](kaori/plugins/kkreds)

A virtual slack currency.

### [`clap ...`](kaori/plugins/clap.py)

This :clap: is :clap: probably :clap: the :clap: most :clap: obnoxious :clap: plugin.

`kaori clap --help` for more options.

### utility plugins

- [User management](kaori/plugins/users)

<!--
## Features

### Mentions Graph

I can draw a directed graph of the mentions between all the people in your
slack. The vertices are people and the edges are the the mentions between two
people. The weight a particular edge represents how many times the head vertex
has mentioned the tail vertex.

![mentions demo](static/images/kizuna_mentions_demo.gif)

Example graph:

![mentions example](static/images/graph_example.png)
-->

## Development

I'm kinda easy to get running. Development and production deployment is all
done with Docker. Make sure you have Docker installed and running on your
system.

The most difficult part of this whole thing is literally just filling in the
environment variables. Please PR this document or the `.env.example` file to
make this easier for people who come after you.

### Run me

1. You should probably create your own bot testbed slack if you don't already
   have one. <https://slack.com/create>
1. [Create a slack app](https://api.slack.com/apps) and deploy it to your testbed slack
1. You need create a `.env` file with all the necessary values. Easiest way to
   do this is to `cp .env.example .env` and then replace the bogus values with
   real values.
1. Run `make` to build all the containers
1. `docker-compose run --rm worker alembic upgrade head` will create the
   database for you
1. `docker-compose up` will start me up! My web interface runs at
   [http://localhost:8000]() and my API runs at [http://localhost:8001]()


We aren't out of the woods yet. Now we have to let slack make requests to our API.

1. Install [ngrok][] or do something that will allow you to expose your local
   API endpoint to the internet.
2. Go to [Your Apps](https://api.slack.com/apps) and under your bot under
   "Event Subscriptions" enter your api url. The path should be:
   `/slack/events`
3. If you are using [ngrok][] you can inspect the requests from slack at
   [http://127.0.0.1:4040]()

NOW you should be up and running.

[ngrok]: https://ngrok.com/


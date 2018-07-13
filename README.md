# キズナ

はいども！キズナです！

I am a slack bot with functionality that ranges from "useless" to "pretty neat".

[GitHub](https://github.com/austinpray/kizuna) / [GitLab](https://gitlab.com/austinpray/kizuna)

## Features

### Mentions Graph

I can draw a directed graph of the mentions between all the people in your slack. The vertices are people and the edges are the the mentions between two people. The weight a particular edge represents how many times the head vertex has mentioned the tail vertex.

![mentions demo](static/images/kizuna_mentions_demo.gif)

Example graph:

![mentions example](static/images/graph_example.png)


<!-- begin kizuna mentions help -->
```
kizuna mentions [-h] [--layout LAYOUT]

Generate a mentions graph

optional arguments:
  -h, --help            show this help message and exit
  --layout LAYOUT, -l LAYOUT
                        Defaults to `dot`. Can be any of `dot`, `neato`,
                        `fdp`, `twopi`, `circo`, `raw`
```
<!-- end kizuna mentions help -->

## Development

I'm pretty easy to get running. Development and production deployment is all done with Docker. Make sure you have Docker installed and running on your system.

1. You should probably create your own bot testbed slack if you don't already have one. [https://slack.com/create]()
2. You need create a `.env` file that contains your `SLACK_API_TOKEN`, `SECRET_KEY`, and `FERNET_KEY`.
Easiest way to do this is to `cp .env.example .env` and then replace the bogus slack token with your real token you get from your bot's slack app config.
`FERNET_KEY` can be generated with `bin/generate-fernet-key.py` but the one in `.env.example` is probably fine for dev.
`SECRET_KEY` can be generated with `bin/generate-secret-key.py` but the one in `.env.example` is probably fine for dev.
3. Run `make build` to build all the containers
4. `docker-compose run --rm bot alembic upgrade head` will create the database for you
5. `docker-compose up` will start me up and connect me to slack!

That's it!

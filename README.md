# キズナ

はいども！キズナです！

I am a slack bot with functionality that ranges from "useless" to "pretty neat".

[GitHub](https://github.com/austinpray/kizuna) / [GitLab](https://gitlab.com/austinpray/kizuna)

## Features

### Mentions Graph

I can draw a directed graph of the mentions between all the people in your
slack. The vertices are people and the edges are the the mentions between two
people. The weight a particular edge represents how many times the head vertex
has mentioned the tail vertex.

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

I'm kinda easy to get running. Development and production deployment is all
done with Docker. Make sure you have Docker installed and running on your
system.

The most difficult part of this whole thing is literally just filling in the
environment variables. Please PR this document or the `.env.example` file to
make this easier for people who come after you.

### Run me

1. You should probably create your own bot testbed slack if you don't already
   have one. [https://slack.com/create]()
1. [Create a slack app](https://api.slack.com/apps) and deploy it to your testbed slack
1. You need create a `.env` file with all the necessary values. Easiest way to
   do this is to `cp .env.example .env` and then replace the bogus values with
   real values. You can ignore the AWS creds if you are not working on the
   image upload feature. `FERNET_KEY` can be generated with
   `bin/generate-fernet-key.py` but the one in `.env.example` is probably fine
   for dev. `SECRET_KEY` can be generated with `bin/generate-secret-key.py` but
   the one in `.env.example` is probably fine for dev.
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

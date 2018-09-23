FROM austinpray/kizuna/base

CMD ["dramatiq-gevent", "kizuna.worker", "-p", "2", "-t", "8"]

RUN apt-get update \
    && apt-get install -y --no-install-recommends graphviz \
    && rm -rf /var/lib/apt/lists/*

RUN pip install 'spacy==2.0.*'
RUN python -m spacy download en

# heavy deps
COPY . .
RUN pip install -e .[worker]

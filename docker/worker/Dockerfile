FROM austinpray/kizuna/base

CMD ["dramatiq-gevent", "kizuna.worker", "-p", "2", "-t", "8"]

COPY ./ ./
RUN pip install -e .

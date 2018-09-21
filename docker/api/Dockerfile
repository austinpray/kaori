FROM austinpray/kizuna/base

CMD ["gunicorn", "--config", "python:config.gunicorn_api", "kizuna.api"]

COPY ./ ./
RUN pip install -e .

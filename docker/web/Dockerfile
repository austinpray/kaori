FROM austinpray/kizuna/base

CMD ["gunicorn", "--config", "python:config.gunicorn_web", "kizuna.web"]

COPY ./ ./
RUN pip install -e .

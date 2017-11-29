FROM python:3.6-stretch

ENV workdir /kizuna

WORKDIR ${workdir}

RUN apt-get update \
    && apt-get install -y graphviz

COPY requirements.txt ${workdir}/requirements.txt
RUN pip install -r requirements.txt

COPY . ${workdir}

CMD ["python", "-u", "./bot.py"]

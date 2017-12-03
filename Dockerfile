FROM python:3.6-stretch

ENV workdir /kizuna

WORKDIR ${workdir}
ENV PYTHONPATH="${PYTHONPATH}:${workdir}"

CMD ["python", "-u", "./bot.py"]

RUN apt-get update \
    && apt-get install -y vim graphviz

COPY requirements.txt ${workdir}/requirements.txt
RUN pip install -r requirements.txt

COPY . ${workdir}

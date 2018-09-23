FROM austinpray/kizuna/base

RUN pip install 'spacy==2.0.*'
RUN python -m spacy download en

COPY . .
RUN pip install -e .[api,web,worker]

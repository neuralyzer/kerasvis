FROM python

# pandas is using numpy and it is compiled in setup.py - this is simpler
RUN pip install pandas

COPY . /app

WORKDIR /app

RUN python setup.py install

ENV FLASK_APP kerasvis.runserver

CMD flask run --host=0.0.0.0

EXPOSE 5000

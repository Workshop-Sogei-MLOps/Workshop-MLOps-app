FROM python:3.9

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip \
  && pip install --upgrade pipenv\
  && pip install --upgrade -r /app/requirements.txt

COPY . /app

EXPOSE 8000

ENTRYPOINT [ "python" ]

CMD [ "server.py" ]

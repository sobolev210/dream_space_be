FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY server/requirements.txt /code

RUN pip install -r requirements.txt

COPY server /code

#RUN python manage.py migrate

#CMD ["python",  "manage.py", "runserver"]

CMD ["sh", "docker-entrypoint.sh"]

FROM python:3-alpine3.17

WORKDIR /var/www

ADD ./requirements.txt .

RUN pip install -r requirements.txt

ADD . /var/www

# define the port number the container should expose
EXPOSE 5000

CMD ["python", "app/run.py"]

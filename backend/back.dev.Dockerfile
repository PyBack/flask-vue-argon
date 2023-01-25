FROM python:3.7.2

WORKDIR /www

ADD . .

RUN python3 -m pip install -U pip
RUN pip3 install -r requirements.txt

CMD ["python3",  "app.py"]

FROM python:3.7-alpine

RUN apk add --no-cache bash

WORKDIR /project
ADD . /project

RUN pip install -r requirements.txt

CMD ["python", "-u", "app.py"]
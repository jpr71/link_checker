FROM iron/python:2

WORKDIR /app
ADD . /app

ENTRYPOINT ["python", "link_checker.py"]
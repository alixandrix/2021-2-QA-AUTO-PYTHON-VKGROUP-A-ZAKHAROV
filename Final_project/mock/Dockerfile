FROM python:3.8

ADD requirements.txt /requrements.txt
RUN pip3.8 install -r /requrements.txt && rm -f /requrements.txt

ADD code /code
WORKDIR /code


CMD ["python3", "mock_server.py"]


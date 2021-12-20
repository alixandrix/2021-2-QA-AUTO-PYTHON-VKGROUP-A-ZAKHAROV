FROM python:3.8

ADD requirements.txt /requrements.txt
RUN pip3.8 install -r /requrements.txt && rm -f /requrements.txt

ADD source /source
WORKDIR /source
ENV PYTHONPATH="${PWD}/source"

CMD ["pytest", "-l", "-v", "--alluredir=/tmp/allure-report"]
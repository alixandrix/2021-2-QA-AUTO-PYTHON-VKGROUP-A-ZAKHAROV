FROM python:3.8

ADD requirements.txt /requrements.txt
RUN pip3.8 install -r /requrements.txt && rm -f /requrements.txt

ADD source /source
WORKDIR /source
ENV PYTHONPATH=~/PycharmProjects/2021-2-QA-AUTO-PYTHON-VKGROUP-A-ZAKHAROV/Final_project/tests/source


CMD ["pytest", "-s", "-l", "-v", "--alluredir=/tmp/allure-report"]
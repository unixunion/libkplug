#FROM ubuntu:20.04
FROM python:latest
ARG upload=0
WORKDIR /app
COPY . .
#RUN apt-get update && apt-get -y install python3-dev
#RUN apt-get -y install python3-pip
#RUN apt-get -y install git
RUN python3 -m pip install --upgrade pip setuptools wheel twine
RUN python3 -m pip install -r requirements.txt
RUN python3 setup.py bdist_wheel --universal
COPY .pypirc /root

RUN test "${upload}" -gt 0 && twine upload --repository pypi /app/dist/*.whl --verbose || echo "no upload arg passed"

ENTRYPOINT ["/bin/bash", "-c"]
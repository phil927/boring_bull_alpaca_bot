FROM amazonlinux:2.0.20210813.1
RUN yum install -y python37 && \
    yum install -y python3-pip && \
    yum install -y zip && \
    yum clean all
RUN python3.7 -m pip install --upgrade pip && \
    python3.7 -m pip install virtualenv

RUN python3.7 -m venv env && \
    source env/bin/activate

RUN pip install numpy && \
    pip install cython && \
    pip install alpaca-trade-api

COPY 

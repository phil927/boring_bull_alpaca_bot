FROM public.ecr.aws/lambda/python:3.8

# RUN yum install -y python3.8 && \
#     yum install -y python3-pip && \
#     yum install -y zip && \
#     yum clean all
RUN python3.8 -m pip install --upgrade pip && \
    python3.8 -m pip install virtualenv

RUN python3.8 -m venv env && \
    source env/bin/activate

RUN pip install numpy --upgrade --target "${LAMBDA_TASK_ROOT}"
RUN pip install cython --upgrade --target "${LAMBDA_TASK_ROOT}"
RUN pip install boto3 --upgrade --target "${LAMBDA_TASK_ROOT}"
RUN pip install alpaca-trade-api --upgrade --target "${LAMBDA_TASK_ROOT}"

COPY aws_sns.py ${LAMBDA_TASK_ROOT}
COPY handler.py ${LAMBDA_TASK_ROOT}

CMD ["handler.lambda_handler"]



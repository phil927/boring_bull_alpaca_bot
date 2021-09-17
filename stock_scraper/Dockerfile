FROM public.ecr.aws/lambda/python:3.8

RUN python3.8 -m pip install --upgrade pip

RUN pip3 install yahoo_fin --upgrade --target "${LAMBDA_TASK_ROOT}"
RUN pip install boto3 --upgrade --target "${LAMBDA_TASK_ROOT}"

COPY handler.py ${LAMBDA_TASK_ROOT}

CMD ["handler.lambda_handler"]



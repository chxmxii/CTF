FROM public.ecr.aws/lambda/python:3.9

RUN pip install --no-cache-dir boto3

COPY handler.py ${LAMBDA_TASK_ROOT}/

CMD ["handler.lambda_handler"]

# Use the official AWS Lambda Python 3.13 base image:
FROM public.ecr.aws/lambda/python:3.13

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt --target /var/task

COPY lambda_function.py /var/task

CMD [ "lambda_function.lambda_handler" ]

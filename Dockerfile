# Use the official AWS Lambda Python 3.13 base image:
#   public.ecr.aws/lambda/python:3.13
# OR you can use docker.io/amazon/aws-lambda-python:3.13 if you prefer DockerHub.
FROM public.ecr.aws/lambda/python:3.13

# (Optional) Copy your requirements.txt into the image
COPY requirements.txt ./

# Install dependencies into /var/task (the Lambda Task root)
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --target /var/task

# Copy your Lambda function code into /var/task
COPY lambda_function.py /var/task

# Lambda looks for the handler in "lambda_function.lambda_handler" by default
CMD [ "lambda_function.lambda_handler" ]
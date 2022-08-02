FROM public.ecr.aws/lambda/python:3.9

COPY app ${LAMBDA_TASK_ROOT}/app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN pip3 install -U descarteslabs>=1.11.0 --target "${LAMBDA_TASK_ROOT}"

ENV DESCARTESLABS_ENV=aws-production

RUN mkdir /tmp/models

# ENV MODEL_NAME=classifier.joblib
# ENV MODEL_S3_BUCKET=dl-aws-onboarding

CMD [ "app.dl_aws_lambda.run_model" ]
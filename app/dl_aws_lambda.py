from .model import get_field_class
import logging
import boto3
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
s3_bucket = os.environ["MODEL_S3_BUCKET"]
model_name = os.environ["MODEL_NAME"]

def run_model(event, context):
    
    logger.info(f"Recieved request: {event}")
    
    geom = event["geometry"]
    if "fid" in event.keys():
        fid = event["fid"]
    else:
        fid = ""
    
    return get_field_class(geom, fid, s3_bucket, model_name)
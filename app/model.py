import descarteslabs as dl

from .utils import get_ndvi_tseries
from joblib import load

import os
import os.path as osp
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_field_class(geom, fid, s3_bucket, model_name):
    
    if not osp.exists("/tmp/models"):
        os.makedirs("/tmp/models")

    temp_file_path = osp.join("/tmp/models", model_name)

    logger.info(f"Loading classifier: {model_name}")
    if not osp.exists(temp_file_path):
        s3 = boto3.client("s3")
        logger.info(f"Classifier not found locally at {temp_file_path}. Pulling from s3")
        # Download pickled model from S3 and unpickle
        s3.download_file(s3_bucket, model_name, temp_file_path)
        
    clf = load(temp_file_path)

    logger.info("Retrieving timeseries")
    ndvi_ts, ndvi_dates = get_ndvi_tseries(geom)

    
    result = {
        "class": clf.predict(ndvi_ts.reshape(1,-1))[0], 
        "fid": fid
    }
    
    return result